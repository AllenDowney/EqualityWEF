"""Utility functions for Bayesian counterfactual analysis.

This module provides reusable functions for counterfactual analysis that work
for both HALE and Life Expectancy gap models.
"""

import numpy as np
import pandas as pd
import arviz as az
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from utils import decorate, AIBM_COLORS, code_to_who_country


def compute_gap_extremes(panel_df):
    """
    Compute minimum and maximum gap values for each gap predictor across all country-years.
    
    Parameters
    ----------
    panel_df : pd.DataFrame
        Panel dataset with gap predictor columns (starting with 'Gap_')
        
    Returns
    -------
    dict
        Dictionary mapping gap predictor names to dictionaries with:
        - 'min_gap': minimum gap value
        - 'min_country': country code with minimum gap
        - 'min_year': year with minimum gap
        - 'max_gap': maximum gap value
        - 'max_country': country code with maximum gap
        - 'max_year': year with maximum gap
    """
    # Get all gap predictor columns
    gap_predictors = [col for col in panel_df.columns if col.startswith('Gap_')]
    
    # Compute extremes for each gap predictor
    gap_extremes = {}
    for gap_pred in gap_predictors:
        gap_data = panel_df[gap_pred].dropna()
        if len(gap_data) > 0:
            min_val = gap_data.min()
            max_val = gap_data.max()
            min_idx = gap_data.idxmin()
            max_idx = gap_data.idxmax()
            
            # Get country-year for extremes
            min_row = panel_df.loc[min_idx]
            max_row = panel_df.loc[max_idx]
            
            gap_extremes[gap_pred] = {
                'min_gap': min_val,
                'min_country': min_row['country'],
                'min_year': int(min_row['Year']),
                'max_gap': max_val,
                'max_country': max_row['country'],
                'max_year': int(max_row['Year']),
            }
    
    return gap_extremes


def counterfactual_predictions_bayesian(
    country, year, gap_predictor, trace, metadata, panel_df, gap_extremes, 
    country_to_idx, year_to_idx
):
    """
    Generate counterfactual prediction by adjusting a gap predictor to best attainable value.
    
    Parameters
    ----------
    country : str
        Country code (e.g., 'USA', 'GBR')
    year : int
        Year (e.g., 2019)
    gap_predictor : str
        Name of the gap predictor column (e.g., 'Gap_Alcohol')
    trace : arviz.InferenceData
        Posterior trace from MCMC sampling
    metadata : dict
        Metadata dictionary with transformation parameters
    panel_df : pd.DataFrame
        Panel dataset with all predictor values
    gap_extremes : dict
        Dictionary with gap extremes for each predictor (from compute_gap_extremes)
    country_to_idx : dict
        Dictionary mapping country codes to indices
    year_to_idx : dict
        Dictionary mapping years to indices
        
    Returns
    -------
    dict
        Dictionary with counterfactual results including:
        - country, year, indicator: identifiers
        - current_gap, target_gap: gap values
        - target_country, target_year: target country-year
        - original_prediction: posterior distribution of original prediction
        - counterfactual_prediction: posterior distribution of counterfactual prediction
        - change: posterior distribution of change (counterfactual - original)
        - original_summary, counterfactual_summary, change_summary: dicts with mean and 94% HDI
    """
    # Get current country-year row
    country_year_mask = (panel_df['country'] == country) & (panel_df['Year'] == year)
    if not country_year_mask.any():
        raise ValueError(f"No data found for {country} in year {year}")
    
    current_row = panel_df[country_year_mask].iloc[0]
    
    # Extract indicator name from gap predictor (e.g., 'Gap_Alcohol' -> 'Alcohol')
    indicator_name = gap_predictor.replace('Gap_', '')
    
    # Get current gap value
    current_gap = current_row[gap_predictor]
    
    # Determine target gap based on current gap sign
    if current_gap > 0:
        # Positive gap: find minimum gap (best case: smallest positive gap)
        target_gap = gap_extremes[gap_predictor]['min_gap']
        target_country = gap_extremes[gap_predictor]['min_country']
        target_year = gap_extremes[gap_predictor]['min_year']
    else:
        # Negative gap: find maximum gap (best case: largest positive gap)
        target_gap = gap_extremes[gap_predictor]['max_gap']
        target_country = gap_extremes[gap_predictor]['max_country']
        target_year = gap_extremes[gap_predictor]['max_year']
    
    # If target gap has opposite sign of current gap, set target to zero
    if (current_gap > 0 and target_gap < 0) or (current_gap < 0 and target_gap > 0):
        target_gap = 0.0
        target_country = ""
        target_year = None
    
    # Reconstruct current Male/Female from Mid and Gap
    mid_col = f'Mid_{indicator_name}'
    if mid_col not in current_row.index:
        raise ValueError(f"Mid column {mid_col} not found for {indicator_name}")
    
    current_mid = current_row[mid_col]
    current_male = current_mid + current_gap / 2
    current_female = current_mid - current_gap / 2
    
    # Adjust Male/Female to achieve target gap
    if current_gap > 0:
        # Positive gap: bring men toward women's level
        adjusted_male = current_female + target_gap
        adjusted_female = current_female
    else:
        # Negative gap: bring women toward men's level
        adjusted_male = current_male
        adjusted_female = current_male - target_gap
    
    # Recompute Mid and Gap from adjusted Male/Female
    adjusted_mid = (adjusted_male + adjusted_female) / 2
    adjusted_gap = adjusted_male - adjusted_female
    
    # Get all current predictor values (standardized)
    X_mean = np.array(metadata['X_mean'])
    X_std = np.array(metadata['X_std'])
    y_mean = metadata['y_mean']
    predictors = metadata['predictors']
    countries = np.array(metadata['countries'])
    years = np.array(metadata['years'])
    
    # Get country and year indices
    country_idx = country_to_idx[country]
    year_idx = year_to_idx[year]
    
    # Build original predictor vector (standardized)
    X_original = np.array([current_row[p] for p in predictors])
    X_original_std = (X_original - X_mean) / X_std
    
    # Build counterfactual predictor vector (standardized)
    X_counterfactual = X_original.copy()
    # Update the gap predictor
    gap_idx = predictors.index(gap_predictor)
    X_counterfactual[gap_idx] = adjusted_gap
    # Update the mid predictor if it exists
    if mid_col in predictors:
        mid_idx = predictors.index(mid_col)
        X_counterfactual[mid_idx] = adjusted_mid
    X_counterfactual_std = (X_counterfactual - X_mean) / X_std
    
    # Extract posterior samples
    beta_samples = trace.posterior['beta'].values.reshape(-1, len(predictors))  # (n_samples, n_predictors)
    alpha_samples = trace.posterior['alpha'].values.reshape(-1, len(countries))  # (n_samples, n_countries)
    
    # Compute predictions for each posterior sample
    # Original: y* = α_i + X* β
    alpha_i_samples = alpha_samples[:, country_idx]
    original_pred_centered = alpha_i_samples + np.dot(X_original_std, beta_samples.T)
    original_pred = original_pred_centered + y_mean
    
    # Counterfactual: y* = α_i + X*_cf β
    counterfactual_pred_centered = alpha_i_samples + np.dot(X_counterfactual_std, beta_samples.T)
    counterfactual_pred = counterfactual_pred_centered + y_mean
    
    # Compute change
    change = counterfactual_pred - original_pred
    
    # Compute summary statistics (mean and 94% HDI)
    def compute_summary(samples):
        mean = np.mean(samples)
        hdi = az.hdi(samples, hdi_prob=0.94)
        return {
            'mean': mean,
            'hdi_3%': hdi[0],
            'hdi_97%': hdi[1],
        }
    
    return {
        'country': country,
        'year': year,
        'indicator': indicator_name,
        'current_gap': current_gap,
        'target_gap': target_gap,
        'target_country': target_country,
        'target_year': target_year,
        'original_prediction': original_pred,
        'counterfactual_prediction': counterfactual_pred,
        'change': change,
        'original_summary': compute_summary(original_pred),
        'counterfactual_summary': compute_summary(counterfactual_pred),
        'change_summary': compute_summary(change),
    }


def compute_importance_summary(trace, metadata):
    """
    Compute importance measures from posterior samples.
    
    Parameters
    ----------
    trace : arviz.InferenceData
        Posterior trace from MCMC sampling
    metadata : dict
        Metadata dictionary with transformation parameters
        
    Returns
    -------
    pd.DataFrame
        DataFrame with importance measures sorted by importance (descending)
    """
    predictors = metadata['predictors']
    
    # Extract posterior samples for beta coefficients
    beta_samples = trace.posterior['beta'].values.reshape(-1, len(predictors))
    
    # Get SD values used for standardization
    X_std = np.array(metadata['X_std'])
    
    # Compute importance measure: |β_standardized| × SD_original
    importance_samples = np.abs(beta_samples) * X_std[np.newaxis, :]
    
    # Create importance summary
    importance_summary = pd.DataFrame({
        'Predictor': predictors,
        'Importance_mean': importance_samples.mean(axis=0),
        'Importance_hdi_3%': np.percentile(importance_samples, 3, axis=0),
        'Importance_hdi_97%': np.percentile(importance_samples, 97, axis=0),
    })
    
    # Sort by importance (descending)
    importance_summary = importance_summary.sort_values('Importance_mean', ascending=False)
    
    return importance_summary


def _prepare_viz_dataframe(counterfactual_results):
    """Helper function to prepare visualization DataFrame."""
    return pd.DataFrame({
        'Indicator': [r['indicator'] for r in counterfactual_results],
        'Change_mean': [r['change_summary']['mean'] for r in counterfactual_results],
        'Change_lower': [r['change_summary']['hdi_3%'] for r in counterfactual_results],
        'Change_upper': [r['change_summary']['hdi_97%'] for r in counterfactual_results],
    })


def plot_counterfactual_forest(
    counterfactual_results, 
    output_prefix='counterfactual_effects_usa_2019',
    target_name='HALE gap'
):
    """
    Create forest plot of counterfactual effects (all indicators).
    
    Parameters
    ----------
    counterfactual_results : list
        List of counterfactual result dictionaries from counterfactual_predictions_bayesian
    output_prefix : str
        Prefix for output filenames (e.g., 'counterfactual_effects_usa_2019_hale')
    target_name : str
        Name of target variable for labels (e.g., 'HALE gap' or 'Life Expectancy gap')
        
    Returns
    -------
    str
        Path to saved figure file
    """
    # Create DataFrame with full results
    viz_df = _prepare_viz_dataframe(counterfactual_results)
    
    # Sort by mean change
    viz_df = viz_df.sort_values('Change_mean')
    
    # Forest plot (all indicators)
    fig, ax = plt.subplots(figsize=(10, 8))
    
    y_pos = np.arange(len(viz_df))
    colors = [AIBM_COLORS['crimson'] if x < 0 else AIBM_COLORS['blue'] 
              for x in viz_df['Change_mean']]
    
    # Plot error bars (94% HDI)
    for i, (idx, row) in enumerate(viz_df.iterrows()):
        ax.errorbar(row['Change_mean'], i, 
                    xerr=[[row['Change_mean'] - row['Change_lower']], 
                          [row['Change_upper'] - row['Change_mean']]],
                    fmt='o', color=colors[i], capsize=5, capthick=2, 
                    markersize=8, elinewidth=2)
    
    # Add vertical line at zero
    ax.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    
    # Set labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(viz_df['Indicator'])
    ax.set_xlabel(f'Change in {target_name} (years)', fontsize=12)
    ax.set_title(f'Counterfactual Effects: United States (2019)\n94% Credible Intervals', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add legend
    legend_elements = [
        Patch(facecolor=AIBM_COLORS['crimson'], label='Gap-Closing (reduces gap)'),
        Patch(facecolor=AIBM_COLORS['blue'], label='Gap-Widening (increases gap)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    filename = f'jb/figs/{output_prefix}_bayesian.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    return filename


def plot_counterfactual_by_type(
    counterfactual_results, 
    output_prefix='counterfactual_effects_usa_2019',
    target_name='HALE gap'
):
    """
    Create two-panel plot of counterfactual effects (gap-closing vs gap-widening).
    
    Parameters
    ----------
    counterfactual_results : list
        List of counterfactual result dictionaries from counterfactual_predictions_bayesian
    output_prefix : str
        Prefix for output filenames (e.g., 'counterfactual_effects_usa_2019_hale')
    target_name : str
        Name of target variable for labels (e.g., 'HALE gap' or 'Life Expectancy gap')
        
    Returns
    -------
    str
        Path to saved figure file
    """
    # Create DataFrame with full results
    viz_df = _prepare_viz_dataframe(counterfactual_results)
    
    # Two-panel plot (by type)
    gap_closing_viz = viz_df[viz_df['Change_mean'] < 0].copy().sort_values('Change_mean', ascending=True)
    gap_widening_viz = viz_df[viz_df['Change_mean'] > 0].copy().sort_values('Change_mean', ascending=False)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gap-closing indicators (left panel)
    if len(gap_closing_viz) > 0:
        y_pos1 = np.arange(len(gap_closing_viz))
        for i, (idx, row) in enumerate(gap_closing_viz.iterrows()):
            ax1.errorbar(row['Change_mean'], i, 
                        xerr=[[row['Change_mean'] - row['Change_lower']], 
                              [row['Change_upper'] - row['Change_mean']]],
                        fmt='o', color=AIBM_COLORS['crimson'], capsize=5, capthick=2, 
                        markersize=8, elinewidth=2)
        ax1.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
        ax1.set_yticks(y_pos1)
        ax1.set_yticklabels(gap_closing_viz['Indicator'])
        ax1.set_xlabel(f'Change in {target_name} (years)', fontsize=11)
        ax1.set_title('Gap-Closing Indicators\n(Reduce Gap)', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='x')
        ax1.invert_xaxis()  # Invert so negative values go left
    
    # Gap-widening indicators (right panel)
    if len(gap_widening_viz) > 0:
        y_pos2 = np.arange(len(gap_widening_viz))
        for i, (idx, row) in enumerate(gap_widening_viz.iterrows()):
            ax2.errorbar(row['Change_mean'], i, 
                        xerr=[[row['Change_mean'] - row['Change_lower']], 
                              [row['Change_upper'] - row['Change_mean']]],
                        fmt='o', color=AIBM_COLORS['blue'], capsize=5, capthick=2, 
                        markersize=8, elinewidth=2)
        ax2.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
        ax2.set_yticks(y_pos2)
        ax2.set_yticklabels(gap_widening_viz['Indicator'])
        ax2.set_xlabel(f'Change in {target_name} (years)', fontsize=11)
        ax2.set_title('Gap-Widening Indicators\n(Increase Gap)', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
    
    plt.suptitle(f'Counterfactual Effects by Type: United States (2019)\n94% Credible Intervals', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    filename = f'jb/figs/{output_prefix}_by_type_bayesian.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    return filename


def plot_counterfactual_bar(
    counterfactual_results, 
    output_prefix='counterfactual_effects_usa_2019',
    target_name='HALE gap'
):
    """
    Create bar chart of counterfactual effects (sorted by magnitude).
    
    Parameters
    ----------
    counterfactual_results : list
        List of counterfactual result dictionaries from counterfactual_predictions_bayesian
    output_prefix : str
        Prefix for output filenames (e.g., 'counterfactual_effects_usa_2019_hale')
    target_name : str
        Name of target variable for labels (e.g., 'HALE gap' or 'Life Expectancy gap')
        
    Returns
    -------
    str
        Path to saved figure file
    """
    # Create DataFrame with full results
    viz_df = _prepare_viz_dataframe(counterfactual_results)
    
    # Bar chart (sorted by magnitude)
    viz_df_abs = viz_df.copy()
    viz_df_abs['Abs_change'] = viz_df_abs['Change_mean'].abs()
    viz_df_abs = viz_df_abs.sort_values('Abs_change', ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    y_pos = np.arange(len(viz_df_abs))
    colors = [AIBM_COLORS['crimson'] if x < 0 else AIBM_COLORS['blue'] 
              for x in viz_df_abs['Change_mean']]
    
    # Create horizontal bar chart
    bars = ax.barh(y_pos, viz_df_abs['Change_mean'], color=colors, alpha=0.7)
    
    # Add error bars
    for i, (idx, row) in enumerate(viz_df_abs.iterrows()):
        ax.errorbar(row['Change_mean'], i, 
                    xerr=[[row['Change_mean'] - row['Change_lower']], 
                          [row['Change_upper'] - row['Change_mean']]],
                    fmt='none', color='black', capsize=3, capthick=1, 
                    elinewidth=1, alpha=0.6)
    
    # Add vertical line at zero
    ax.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    
    # Set labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(viz_df_abs['Indicator'])
    ax.set_xlabel(f'Change in {target_name} (years)', fontsize=12)
    ax.set_title(f'Counterfactual Effects: United States (2019)\nSorted by Effect Magnitude (94% Credible Intervals)', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add legend
    legend_elements = [
        Patch(facecolor=AIBM_COLORS['crimson'], label='Gap-Closing (reduces gap)'),
        Patch(facecolor=AIBM_COLORS['blue'], label='Gap-Widening (increases gap)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    filename = f'jb/figs/{output_prefix}_bar_bayesian.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    return filename


def create_counterfactual_visualizations(
    counterfactual_results, 
    output_prefix='counterfactual_effects_usa_2019',
    target_name='HALE gap'
):
    """
    Create three visualization plots for counterfactual analysis results.
    
    This is a convenience function that calls all three individual plot functions.
    For displaying figures in notebooks, use the individual functions in separate cells.
    
    Parameters
    ----------
    counterfactual_results : list
        List of counterfactual result dictionaries from counterfactual_predictions_bayesian
    output_prefix : str
        Prefix for output filenames (e.g., 'counterfactual_effects_usa_2019_hale')
    target_name : str
        Name of target variable for labels (e.g., 'HALE gap' or 'Life Expectancy gap')
        
    Returns
    -------
    dict
        Dictionary with paths to saved figure files
    """
    saved_files = {}
    saved_files['forest'] = plot_counterfactual_forest(counterfactual_results, output_prefix, target_name)
    saved_files['by_type'] = plot_counterfactual_by_type(counterfactual_results, output_prefix, target_name)
    saved_files['bar'] = plot_counterfactual_bar(counterfactual_results, output_prefix, target_name)
    return saved_files


def format_counterfactual_table(
    counterfactual_results, 
    importance_summary, 
    code_to_country_dict=code_to_who_country,
    target_name='gap'
):
    """
    Format counterfactual results into a table DataFrame.
    
    Parameters
    ----------
    counterfactual_results : list
        List of counterfactual result dictionaries
    importance_summary : pd.DataFrame
        DataFrame with importance measures
    code_to_country_dict : dict
        Dictionary mapping country codes to country names
    target_name : str
        Name of target variable for column header (e.g., 'HALE gap' or 'Life Expectancy gap')
        
    Returns
    -------
    tuple
        (formatted_df, full_df) where formatted_df is for display and full_df has all columns
    """
    results = []
    
    for result in counterfactual_results:
        indicator_name = result['indicator']
        gap_pred = f'Gap_{indicator_name}'
        
        # Get importance for this predictor
        importance_row = importance_summary[importance_summary['Predictor'] == gap_pred]
        if len(importance_row) > 0:
            importance = importance_row['Importance_mean'].iloc[0]
        else:
            importance = 0.0
        
        # Get country name for target country
        target_country_code = result['target_country']
        if target_country_code:
            target_country_name = code_to_country_dict.get(target_country_code, target_country_code)
            if result['target_year']:
                target_info = f"{target_country_name} ({result['target_year']})"
            else:
                target_info = target_country_name
        else:
            target_info = ""
        
        # Format change with uncertainty
        change_mean = result['change_summary']['mean']
        change_lower = result['change_summary']['hdi_3%']
        change_upper = result['change_summary']['hdi_97%']
        change_str = f"{change_mean:.3f} [{change_lower:.3f}, {change_upper:.3f}]"
        
        results.append({
            'Indicator': indicator_name,
            'Current gap': result['current_gap'],
            'Target gap': result['target_gap'],
            'Target Country-Year': target_info,
            f'Change in {target_name} (years)': change_str,
            'Change mean': change_mean,  # For sorting
            'Importance': importance,  # For sorting
        })
    
    df = pd.DataFrame(results)
    # Sort by importance (descending), then by absolute change (descending)
    df['Abs_change'] = df['Change mean'].abs()
    df = df.sort_values(['Importance', 'Abs_change'], ascending=False)
    df = df.drop('Abs_change', axis=1)  # Remove temporary column
    
    # Select columns for output (exclude sorting columns)
    change_col = f'Change in {target_name} (years)'
    df_output = df[['Indicator', 'Current gap', 'Target gap', 'Target Country-Year', change_col]].copy()
    
    return df_output, df


def plot_predicted_vs_actual_over_time(
    country, trace, metadata, panel_df, country_to_idx, 
    target_name='HALE gap', target_col='HALE_gap', output_filename=None
):
    """
    Plot predicted vs actual gap over time for a specific country.
    
    Parameters
    ----------
    country : str
        Country code (e.g., 'USA')
    trace : arviz.InferenceData
        Posterior trace from Bayesian model
    metadata : dict
        Model metadata with X_mean, X_std, y_mean, predictors, countries
    panel_df : pd.DataFrame
        Panel dataset with country, Year, and target_col columns
    country_to_idx : dict
        Mapping from country codes to indices
    target_name : str
        Name of target variable for labels (e.g., 'HALE gap' or 'Life Expectancy gap')
    target_col : str
        Column name in panel_df for target variable (e.g., 'HALE_gap' or 'LE_gap')
    output_filename : str or Path, optional
        Filename to save the figure. If None, figure is not saved.
        
    Returns
    -------
    fig, ax : matplotlib figure and axes
    """
    # Get data for this country
    country_data = panel_df[panel_df['country'] == country].copy()
    country_data = country_data.sort_values('Year')
    
    if len(country_data) == 0:
        raise ValueError(f"No data found for country: {country}")
    
    # Get transformation parameters
    X_mean = np.array(metadata['X_mean'])
    X_std = np.array(metadata['X_std'])
    y_mean = metadata['y_mean']
    predictors = metadata['predictors']
    countries = np.array(metadata['countries'])
    
    # Get country index
    country_idx_val = country_to_idx[country]
    
    # Extract posterior samples
    beta_samples = trace.posterior['beta'].values.reshape(-1, len(predictors))
    alpha_samples = trace.posterior['alpha'].values.reshape(-1, len(countries))
    alpha_i_samples = alpha_samples[:, country_idx_val]
    
    # Compute predictions for each year
    years = country_data['Year'].values
    actual_values = country_data[target_col].values
    predicted_means = []
    predicted_lower = []
    predicted_upper = []
    
    for idx, row in country_data.iterrows():
        # Build predictor vector (standardized)
        X_current = np.array([row[p] for p in predictors])
        X_current_std = (X_current - X_mean) / X_std
        
        # Compute predictions for each posterior sample
        pred_centered = alpha_i_samples + np.dot(X_current_std, beta_samples.T)
        pred_original = pred_centered + y_mean
        
        # Compute summary
        pred_mean = np.mean(pred_original)
        pred_hdi = az.hdi(pred_original, hdi_prob=0.94)
        
        predicted_means.append(pred_mean)
        predicted_lower.append(pred_hdi[0])
        predicted_upper.append(pred_hdi[1])
    
    predicted_means = np.array(predicted_means)
    predicted_lower = np.array(predicted_lower)
    predicted_upper = np.array(predicted_upper)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot actual values
    ax.plot(years, actual_values, 'o-', color=AIBM_COLORS['crimson'], 
            label='Actual', linewidth=2, markersize=8, zorder=3)
    
    # Plot predicted values with uncertainty bands
    ax.plot(years, predicted_means, 's-', color=AIBM_COLORS['blue'], 
            label='Predicted (mean)', linewidth=2, markersize=6, zorder=3)
    ax.fill_between(years, predicted_lower, predicted_upper, 
                     color=AIBM_COLORS['blue'], alpha=0.2, 
                     label='Predicted (94% HDI)', zorder=1)
    
    # Formatting
    country_name = code_to_who_country.get(country, country)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel(f'{target_name} (years)', fontsize=12)
    ax.set_title(f'Predicted vs Actual {target_name}: {country_name} ({country})', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Add statistics text box
    residuals = actual_values - predicted_means
    mae = np.mean(np.abs(residuals))
    rmse = np.sqrt(np.mean(residuals**2))
    r2 = 1 - np.sum(residuals**2) / np.sum((actual_values - np.mean(actual_values))**2)
    
    stats_text = f'MAE: {mae:.3f} years\nRMSE: {rmse:.3f} years\nR²: {r2:.3f}'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if output_filename:
        plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    
    plt.show()
    
    return fig, ax

