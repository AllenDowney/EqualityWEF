# HALE Differences Between Countries - Project Plan

## Project Overview
Exploring the causes of differences in Healthy Life Expectancy (HALE) between countries.

## Research Questions
In most countries, women live longer than men, as measured by raw life expectancy and HALE.
These differences are sometimes considered to be natural, but in some high-income countries, the differences are quite small, which suggests that the factors that cause differences can be mitigated.

The goal of this project is to see what part of the difference in HALE can be explained statistically by differences in various factors that are likely to contribute differentially to male and female life expectancy.

Background: https://ourworldindata.org/why-do-women-live-longer-than-men

## Background Information

### Summary of Factors Contributing to the HALE Gender Gap

Based on research from Our World in Data and related studies, the gender gap in Healthy Life Expectancy (HALE) and life expectancy is influenced by multiple factors:

#### 1. **Smoking and Tobacco Use**
- Historically, men have had significantly higher smoking rates than women
- Smoking is a major contributor to cardiovascular disease, lung cancer, and respiratory diseases
- As smoking rates have declined and converged between genders in some countries, the life expectancy gap has narrowed
- This suggests smoking is one of the most important modifiable factors

#### 2. **Cardiovascular Disease**
- Men typically have higher rates of cardiovascular disease and heart attacks
- This contributes significantly to the gender gap in mortality
- Risk factors include smoking, diet, and potentially biological differences

#### 3. **Occupational Hazards**
- Men are more likely to work in dangerous occupations (construction, mining, manufacturing)
- Higher rates of workplace accidents, injuries, and exposure to hazardous materials
- These occupational risks directly impact mortality and morbidity

#### 4. **Violence and Accidents**
- Men have higher rates of death from violence, homicide, and accidents
- Higher rates of risky behaviors (dangerous driving, substance use)
- Suicide rates are typically higher among men in most countries

#### 5. **Health-Seeking Behaviors**
- Women are generally more likely to seek preventive healthcare and regular check-ups
- Men may delay seeking medical care, leading to later diagnosis and treatment
- This can affect both mortality and morbidity (healthy years lived)

#### 6. **Alcohol Consumption**
- Men typically have higher rates of alcohol consumption and alcohol-related diseases
- Alcohol contributes to liver disease, accidents, and various health conditions

#### 7. **Biological Factors**
- Some biological differences exist (hormonal, genetic) but research suggests these are smaller contributors
- The fact that the gap varies significantly across countries and has changed over time suggests behavioral and environmental factors are more important

#### Key Insight
The variation in the gender gap across countries (with smaller gaps in some high-income countries) suggests that many of these factors are modifiable through policy, healthcare access, and cultural changes. This makes them important targets for statistical analysis to understand which factors explain the most variation in HALE differences.

NOTE: In some cases, the gap has closed as male health has improved more quickly than female health. For example, in Nigeria the gap is small, but that might be because maternal mortality is quite high. So we should include maternal mortality in the analysis as well as other factors that might lower female life expectancy.


## Data Sources

We'll start with data from Our World in Data and branch out to other sources later.

Articles on using OWID data API: 

* https://ourworldindata.org/easier-to-reuse-our-data

* https://www.allendowney.com/blog/2024/11/24/download-the-world-in-data/

### Summary of OWID API Access Methods

**Our World in Data API Overview:**
OWID provides multiple ways to access their data programmatically:

1. **Public Chart API**: 
   - Provides access to curated charts and underlying data in CSV and JSON formats
   - Accessible via HTTP requests in any programming language
   - Primarily provides time series data by time (year) and entity (country)
   - Data can be accessed by constructing URLs with specific query parameters
   - Example: `https://ourworldindata.org/grapher/[dataset-name].csv?v=1&csvType=filtered&useColumnShortNames=true&country=USA`

2. **Metadata Access**:
   - Metadata for datasets can be retrieved as JSON
   - Example: `https://ourworldindata.org/grapher/[dataset-name].metadata.json`
   - Metadata includes information about the dataset structure, variables, and available countries

3. **ETL Data Catalog API**:
   - Provides access to a larger data catalog with additional dimensions (age group, gender breakdowns, etc.)
   - Currently accessed through a Python client
   - Offers more extensive data for in-depth analysis

**Allen Downey's Guide (Download the World in Data):**
- Provides practical Python examples for accessing OWID data
- Demonstrates how to construct API requests to retrieve specific datasets
- Shows how to process CSV data using pandas
- Includes examples of data manipulation and analysis workflows
- Can be adapted to access HALE-related data by identifying appropriate dataset names and parameters

**Key Benefits:**
- Programmatic access eliminates manual downloads
- Can retrieve filtered data for specific countries or time periods
- Supports automated data updates and reproducible workflows
- Enables efficient integration into analysis pipelines

### WHO Global Health Observatory (GHO) API Client

**File: `who_data.py`**

A Python client class (`WHOGHOClient`) for accessing data from the WHO Global Health Observatory API. This provides access to health indicators that are relevant for the HALE gender gap analysis.

Documentation of the API: https://www.who.int/data/gho/info/gho-odata-api

**Key Features:**

1. **HALE Data Retrieval** (`get_hale_data`):
   - Retrieves Healthy Life Expectancy (HALE) data by sex (Male, Female, Both sexes)
   - Uses indicator code `WHOSIS_000002` for HALE at birth
   - Returns data with columns: Country, CountryCode, Year, Sex, HALE_Years, HALE_Low, HALE_High
   - Supports filtering by specific years
   - This is the **target variable** for our analysis (gender gap = Female HALE - Male HALE)

2. **Cardiovascular Disease Death Rates** (`get_cardiovascular_death_rates`):
   - Retrieves age-standardized cardiovascular disease death rates by gender
   - Tries multiple indicator codes to find available data
   - Returns data with columns: Country, Year, Sex, DeathRate, DeathRate_Low, DeathRate_High
   - This is one of our **key predictors** (cardiovascular disease contributes significantly to the gender gap)

3. **Indicator Search** (`search_indicators`):
   - Allows searching for indicators by name/keyword
   - Useful for discovering available data sources

4. **Countries List** (`get_countries_list`):
   - Retrieves list of available countries/regions in the WHO database

**API Base URL:** `https://ghoapi.azureedge.net/api`

**Usage Example:**
```python
client = WHOGHOClient()
hale_df = client.get_hale_data(years=[2015, 2020, 2023])
cardio_df = client.get_cardiovascular_death_rates()
```

**Data Output:**
- Saves HALE data to `who_hale_data.csv`
- Saves cardiovascular death rates to `who_cardiovascular_death_rates.csv`
- Includes both full datasets and recent-year filtered versions

**Relevance to Project:**
- Provides the **target variable** (HALE by sex) needed to calculate gender gaps
- Provides **cardiovascular disease death rates** as a predictor variable
- Can be extended to retrieve other relevant indicators (smoking, suicide rates, maternal mortality, etc.)


## Methodology

Linear regression (possible sklearn RidgeRegression) with the HALE gender gap as target variable.

Possible predictors:

1. **Smoking prevalence (male vs. female difference or ratio)**
   - Identified as one of the most important modifiable factors
   - Strong evidence that gap narrows as smoking rates converge
   - Readily available in health datasets

2. **Cardiovascular disease death rates (male vs. female difference or ratio)**
   - Major contributor to the gender gap in mortality
   - Directly measurable from cause-of-death data
   - May capture effects of smoking and other risk factors

3. **Suicide rates (male vs. female difference or ratio)**
   - Typically higher in men across most countries
   - Directly measurable and strongly linked to mortality
   - Reflects mental health and social factors

4. **Alcohol-attributable death rates (male vs. female difference or ratio)**
   - Typically higher in men across most countries
   - Directly measurable and strongly linked to mortality
   - Captures both direct alcohol-related deaths and alcohol-attributable deaths from other causes
   - Age-standardized rates available for cross-country comparison

5. **Unintentional poisoning mortality rates (male vs. female difference or ratio)**
   - Typically higher in men across most countries
   - Directly measurable and strongly linked to mortality
   - Includes accidental poisonings from chemicals, drugs, and other substances
   - Reflects occupational hazards and risk-taking behaviors
   - Excellent temporal coverage (2000-2021) and country coverage (196 countries)

6. **Road traffic crash death rates (male vs. female difference or ratio)**
   - Typically 2-4 times higher in men across most countries
   - Directly measurable and strongly linked to mortality
   - Major contributor to the gender gap in mortality
   - Reflects higher exposure to driving (including occupational exposure), occupational hazards, and potentially risk-taking behaviors
   - Age-standardized rates available for ages 15+ (matching HALE methodology)
   - Good country coverage (180 countries) for 2019

7. **Maternal mortality ratio** (per 100,000 live births)
   - Critical for understanding cases where gap is small due to high female mortality
   - Directly measurable and strongly impacts female life expectancy
   - Inherently female-specific (deaths during pregnancy, childbirth, or within 42 days)
   - Particularly relevant in lower-income countries where maternal mortality is high
   - Excellent temporal coverage (1985-2023) and country coverage (202 countries)
   - High maternal mortality can significantly reduce the HALE gender gap by lowering female life expectancy

8. **Homicide rates (male vs. female difference or ratio)**
   - Typically much higher in men across most countries
   - Directly measurable and strongly linked to mortality
   - Major contributor to the gender gap in mortality
   - Reflects violence, conflict, and social factors that differentially affect men and women
   - Excellent temporal coverage (2000-2021) and country coverage (196 countries)
   - Includes confidence intervals for uncertainty quantification

9. **Infant mortality rate (male vs. female difference or ratio)**
   - HALE is calculated from birth, so infant mortality directly affects HALE calculations
   - Typically higher in males (biological vulnerability + some behavioral factors)
   - Directly measurable and contributes to the gender gap in HALE
   - Excellent temporal coverage (1932-2023) and country coverage (249 countries)
   - More important in lower-income countries with high infant mortality
   - Use `imr` or `MDG_0000000001` indicator

10. **Under-five mortality rate (male vs. female difference or ratio)** (optional - may overlap with infant mortality)
   - Captures early childhood mortality (ages 1-5) in addition to infant mortality
   - May provide more comprehensive coverage than infant mortality alone
   - Excellent temporal coverage (1932-2023) and country coverage (249 countries)
   - Use `MDG_0000000007` indicator (not `u5mr` - see recommendation section for explanation of why MDG_0000000007 has better data quality)
   - ✅ **Implemented** - Data download functionality added to `who_data.py`
   - Consider testing both infant and under-five mortality to see which provides better explanatory power

11. **Diabetes death rates (male vs. female difference or ratio)**
   - Age-standardized death rates, diabetes mellitus, per 100,000
   - Directly measurable and linked to mortality
   - Age-standardized rates match HALE methodology
   - Good country coverage (191 countries)
   - ✅ **Implemented** - Data download functionality added to `who_data.py`
   - **Limitation**: Only has data for 2004 (similar to cardiovascular disease indicators), which limits temporal analysis but provides a good cross-sectional snapshot
   - Diabetes mortality can contribute to the HALE gender gap, though the relative importance may vary by country and healthcare access

**Control variables:**
- Overall life expectancy (to control for general health level)
- GDP per capita (to control for economic development)

## Recommendations for Life Expectancy Gender Gap Model

Since life expectancy includes all years lived (not just healthy years), the model should include both early-life and adult mortality factors. Note: Both HALE and life expectancy are calculated from birth, so both models should include infant/child mortality predictors. The relative importance of early-life vs. adult mortality may differ between the two outcomes.

The following recommendations are organized by priority and relevance:

### High Priority Predictors (Essential for Life Expectancy Model):

1. **All HALE predictors listed above (including infant/child mortality)** - These remain highly relevant because:
   - Adult mortality is still the primary driver of life expectancy gender gaps in most countries
   - Smoking, cardiovascular disease, accidents, violence, and alcohol-related deaths affect overall life expectancy
   - Infant and child mortality also directly affect life expectancy at birth
   - **Recommendation**: Include all 10 predictors from the HALE model (8 adult mortality + 2 early-life mortality)

2. **Infant mortality rate (male vs. female difference or ratio)** - `imr` or `MDG_0000000001`
   - **Equally relevant for both HALE and life expectancy** - Both are calculated from birth, so infant mortality directly affects both
   - Typically higher in males (biological vulnerability + some behavioral factors)
   - Excellent temporal coverage (1932-2023) and country coverage (249 countries)
   - Has gender breakdowns
   - **Recommendation**: Include as a predictor (already included in HALE model above)

3. **Under-five mortality rate (male vs. female difference or ratio)** - `MDG_0000000007` (not `u5mr` - see HALE model section for explanation)
   - Captures early childhood mortality (ages 1-5) in addition to infant mortality
   - May be more comprehensive than infant mortality alone
   - Excellent temporal coverage (1932-2023) and country coverage (249 countries)
   - Has gender breakdowns
   - ✅ **Implemented** - Data download functionality added to `who_data.py`
   - **Recommendation**: Consider including (already included as optional in HALE model above), but may be redundant with infant mortality - choose one or test both

### Medium Priority Predictors (Important but may have overlap):

4. **Chronic respiratory disease death rates (male vs. female difference or ratio)** - COPD, asthma, etc.
   - Strongly linked to smoking (already captured by smoking prevalence)
   - May provide additional information on downstream effects
   - **Recommendation**: Include if available, but smoking prevalence may capture most of the effect

5. **Liver disease/cirrhosis death rates (male vs. female difference or ratio)**
   - Strongly linked to alcohol (already captured by alcohol-attributable death rates)
   - May provide additional specificity
   - **Recommendation**: Include if available, but alcohol-attributable death rates may capture most of the effect

6. **Lung cancer death rates (male vs. female difference or ratio)**
   - Strongly linked to smoking (already captured by smoking prevalence)
   - More specific than general cancer rates
   - **Recommendation**: Include if available, but smoking prevalence may capture most of the effect

### Control Variables for Life Expectancy Model:

- **GDP per capita** - Economic development affects overall health infrastructure and access to care
- **Overall life expectancy** - To control for general health level (but note: this is the target variable, so use with caution or exclude)
- **Healthcare access indicators** (if available) - Universal health coverage, healthcare spending, etc.

### Variables Less Relevant for Life Expectancy (vs HALE):

- **Intimate partner violence prevalence** - Less directly linked to mortality than to morbidity/healthy years
  - **Recommendation**: May still be useful but lower priority than for HALE

### Key Differences from HALE Model:

1. **Similar predictor set** - Both HALE and life expectancy models should include the same predictors since both are calculated from birth. The HALE model now includes infant/child mortality (see Methodology section above).
2. **Broader scope** - Life expectancy captures all mortality (healthy and unhealthy years), while HALE focuses on healthy years. However, both are affected by the same mortality patterns.
3. **Less focus on morbidity** - For life expectancy, factors that affect quality of life but not mortality are less relevant than for HALE (though HALE also focuses on mortality patterns).
4. **Maternal mortality remains critical** - Still important for understanding female life expectancy, especially in lower-income countries.
5. **Relative importance may differ** - The relative contribution of early-life vs. adult mortality may differ between HALE and life expectancy, but this should be determined empirically.

### Recommended Model Structure:

**Primary predictors (same as HALE model):**
- Smoking prevalence (male vs. female difference/ratio)
- Cardiovascular disease death rates (male vs. female difference/ratio)
- Suicide rates (male vs. female difference/ratio)
- Alcohol-attributable death rates (male vs. female difference/ratio)
- Unintentional poisoning mortality rates (male vs. female difference/ratio)
- Road traffic crash death rates (male vs. female difference/ratio)
- Maternal mortality ratio
- Homicide rates (male vs. female difference/ratio)
- Infant mortality rate (male vs. female difference/ratio) ← Also in HALE model
- Under-five mortality rate (male vs. female difference/ratio) ← Also in HALE model (optional)
- Diabetes death rates (male vs. female difference/ratio) ← Also in HALE model

**Control variables:**
- GDP per capita
- Overall life expectancy (use with caution - may create circularity)

**Optional additional predictors (if data available):**
- Chronic respiratory disease death rates
- Liver disease/cirrhosis death rates
- Lung cancer death rates
- Tuberculosis death rates
- HIV/AIDS mortality rates
- Diabetes death rates


## Analysis Steps

### Phase 1: Data Preparation (OECD Countries, Most Recent Data)

**Step 1.1: Load and Prepare Data Using Existing Functions**
- Use existing functions from `hale.md`:
  - `load_and_inventory(filename)` - Loads WHO CSV files, filters to year 2000-2019 (excludes 2020+ to avoid COVID-19 pandemic distortions) and country-level data (CountryCode == "COUNTRY")
  - `compute_gender_gap(df, value_col, sexes)` - Computes separate columns for each sex and gap column
  - `summarize_gap(df, col, sexes=None)` - Computes gender gaps and selects most recent year per country
  - `get_oecd(df)` - Filters DataFrame to OECD countries using `oecd_codes` from `utils.py` (38 countries)

**Note on data years**: We exclude 2020 and later years to avoid COVID-19 pandemic distortions. The pandemic had significant impacts on mortality patterns that may not reflect underlying health factors. Using 2019 or earlier data provides a more stable baseline for understanding the HALE gender gap.

**Step 1.2: Download and Prepare Target Variable (HALE Gender Gap)**
- Load HALE data: `data/who_hale_data.csv`
- Use `load_and_inventory()` to load and filter data
- Map sex codes: `{'SEX_BTSX': 'Both', 'SEX_FMLE': 'Female', 'SEX_MLE': 'Male'}`
- Use `summarize_gap(hale, 'HALE_Years', sexes=['Male', 'Female'])` to:
  - Compute separate columns: `HALE_Years_Male` and `HALE_Years_Female`
  - Select most recent year available for each country
  - Returns `hale_recent` DataFrame indexed by Country with male/female columns
- Calculate target variable: `HALE_gap = HALE_Years_Female - HALE_Years_Male` (in years)
- Filter to OECD countries using `get_oecd(hale_recent)`

**Step 1.3: Download and Prepare Predictor Variables**
For each predictor, load data and use `summarize_gap()` to get most recent year per country. **Use separate male and female values as predictors** (not gaps), except for female-only indicators (maternal mortality):

1. **Smoking prevalence** - `data/who_smoking_data.csv`
   - Column: `SmokingPrevalence`
   - Results: `SmokingPrevalence_Male`, `SmokingPrevalence_Female` (%)

2. **Cardiovascular disease death rates** - `data/who_cardiovascular_death_rates.csv`
   - Column: `DeathRate`
   - Results: `DeathRate_Male`, `DeathRate_Female` (per 100,000)

3. **Suicide rates** - `data/who_suicide_rates.csv`
   - Column: `SuicideRate`
   - Results: `SuicideRate_Male`, `SuicideRate_Female` (per 100,000)

4. **Alcohol-attributable death rates** - `data/who_alcohol_death_rates.csv`
   - Column: `AlcoholDeathRate`
   - Results: `AlcoholDeathRate_Male`, `AlcoholDeathRate_Female` (per 100,000)

5. **Unintentional poisoning rates** - `data/who_poisoning_rates.csv`
   - Column: `PoisoningRate`
   - Results: `PoisoningRate_Male`, `PoisoningRate_Female` (per 100,000)

6. **Road traffic crash rates** - `data/who_road_traffic_death_rates.csv`
   - Column: `RoadTrafficDeathRate`
   - Results: `RoadTrafficDeathRate_Male`, `RoadTrafficDeathRate_Female` (per 100,000)

7. **Homicide rates** - `data/who_homicide_rates.csv`
   - Column: `HomicideRate`
   - Results: `HomicideRate_Male`, `HomicideRate_Female` (per 100,000)

8. **Maternal mortality ratio** - `data/who_maternal_mortality_ratio.csv`
   - Column: `MaternalMortalityRatio`
   - Use `summarize_gap(maternal, 'MaternalMortalityRatio', sexes=['Female'])`
   - Results: `MaternalMortalityRatio_Female` (per 100,000 live births, female-specific)

9. **Under-five mortality rates** - `data/who_u5mr.csv`
   - Column: `U5MR`
   - Results: `U5MR_Male`, `U5MR_Female` (per 1,000 live births)

10. **Diabetes death rates** - `data/who_diabetes_death_rates.csv`
    - Column: `DiabetesDeathRate`
    - Results: `DiabetesDeathRate_Male`, `DiabetesDeathRate_Female` (per 100,000)

11. **NCD Mortality (30-70 years)** - `data/who_ncd_mortality_30_70.csv`
    - Column: `NCDMortality30_70`
    - Results: `NCDMortality30_70_Male`, `NCDMortality30_70_Female` (%)
    - Note: Combined indicator (cardiovascular, cancer, diabetes, chronic respiratory)

**Note on excluded indicators:**
- **Intimate Partner Violence (IPV) prevalence** - Excluded from the model because: (1) data is missing for some OECD countries, and (2) it is likely not a strong direct indicator of HALE gender gap (it affects morbidity/quality of life more than mortality, and the relationship to HALE gap is indirect and complex).

- For each indicator:
  - Use `load_and_inventory()` to load and filter data
  - Use `summarize_gap()` to get most recent year per country
  - Filter to OECD countries using `get_oecd()`
  - For indicators with both male and female data: extract both `_Male` and `_Female` columns (exclude `_Gap` columns to avoid collinearity)
  - For female-only indicators (maternal mortality): keep the `_Female` column

**Step 1.4: Merge All Predictors into Single Dataset**
- Merge all predictor DataFrames (indexed by Country) into single country-level dataset
- Use outer merge to keep all countries, document which countries have missing data for which indicators
- Create missing data report showing coverage for each indicator across OECD countries
- The merged dataset will have one row per country with columns for each predictor (male and female separately for most indicators, female-only for maternal mortality)

**Step 1.5: Handle Missing Data and Create Final Dataset**
- Since missing data is expected to be minimal for OECD countries, use complete-case analysis for primary model
- Document any countries excluded due to missing critical predictors
- Create final analysis dataset with:
  - Target variable: `HALE_gap` (Female - Male, in years)
  - Predictors: All `_Male` and `_Female` columns from Step 1.3 (plus `MaternalMortalityRatio_Female`)
  - Index: Country codes (OECD countries only)


### Phase 2: Exploratory Data Analysis

**Step 2.1: Descriptive Statistics**
- Summary statistics for HALE gap and all predictors
- Distribution plots for HALE gap across OECD countries
- Identify outliers or influential observations

**Step 2.2: Correlation Analysis**
- Correlation matrix of all predictors
- Visualize correlations (heatmap)
- Identify highly correlated predictors (e.g., smoking ↔ cardiovascular disease)
- This confirms need for Ridge/Lasso regularization


### Phase 3: Model Fitting

**Step 3.1: Model Selection Setup**
- Split data: Use all OECD countries (no train/test split for initial analysis due to small sample size)
- Alternative: Use cross-validation for model selection
- Prepare standardized predictors and target variable

**Step 3.2: Fit Multiple Models**
Fit three models for comparison:
1. **Ridge Regression** - Handles multicollinearity, keeps all predictors
2. **Lasso Regression** - Automatic feature selection, identifies most important factors
3. **Elastic Net** - Combines Ridge and Lasso benefits

For each model:
- Use cross-validation (e.g., 5-fold or 10-fold) to select optimal regularization parameter(s)
- For Elastic Net: optimize both α (Lasso/Ridge mix) and λ (regularization strength)
- Use `GridSearchCV` or `RidgeCV`/`LassoCV` from scikit-learn

**Step 3.3: Model Comparison**
- Compare cross-validation scores (R², RMSE) across models
- Compare coefficient patterns
- Select primary model (likely Ridge for counterfactual analysis, or Elastic Net for feature selection)

### Phase 4: Model Interpretation

**Step 4.1: Coefficient Analysis** ✅ **COMPLETE**
- ✅ Extract coefficients from selected model (on standardized scale) - Done in `hale.md` "Extract Elastic Net Coefficients" section
- ✅ Calculate feature importance: `importance = |coefficient| × std(predictor)` - Done in "Calculate Feature Importance" section
- ✅ Rank predictors by importance to identify largest contributors to HALE gap variation - Done, sorted by importance
- ✅ Calculate indicator-level importance (aggregating male and female predictors) - Done in "Importance by Indicator" section
- ✅ Calculate counterfactual predictions (predicted change in HALE gap if male = female for each indicator) - Done in "Summary: Indicator Analysis and Counterfactual Predictions" section

**Step 4.2: Model Diagnostics** ⚠️ **PARTIAL**
- ✅ Calculate R² (explained variance) - R² calculated via cross-validation in Phase 3 (CV_R2_Score)
- ❌ Residual analysis (check for patterns, outliers) - Not yet implemented
- ❌ Check for influential observations (Cook's distance, leverage) - Not yet implemented

**Step 4.3: Feature Importance Visualization** ✅ **COMPLETE**
- ✅ Create bar chart showing coefficient magnitudes (standardized) - Done in "Visualize Predictor Importance" section (top 15 predictors)
- ✅ Highlight top contributors to HALE gap variation - Done in "Top Contributors to HALE Gap" section
- ✅ Create indicator-level importance visualization - Done in "Visualize Indicator Importance" section
- ⚠️ Compare importance across different models (Ridge vs Lasso vs Elastic Net) - Coefficients extracted for all three models in Phase 3, but importance visualization only done for Elastic Net (selected as primary model)

### Phase 5: Counterfactual Analysis

**Note**: Some counterfactual analysis has been completed in Phase 4 (see "Summary: Indicator Analysis and Counterfactual Predictions" section in `hale.md`), which calculates predicted changes in HALE gap if male values equal female values for each indicator. Phase 5 focuses on more systematic country-to-country counterfactual scenarios.

**Step 5.1: Create Counterfactual Function**
Develop function to calculate impact of changing predictor values (male, female, or both):
```python
def counterfactual_impact(model, country_data, predictor_name, new_male_value=None, new_female_value=None):
    """
    Calculate how much HALE gap would change if predictor value(s) changed.
    
    Parameters:
    - model: Fitted regression model
    - country_data: Dictionary/Series of current predictor values for a country
    - predictor_name: Base name of predictor to change (e.g., 'SmokingPrevalence', 'MaternalMortalityRatio')
    - new_male_value: New value for male predictor (standardized), None to keep original
    - new_female_value: New value for female predictor (standardized), None to keep original
    
    Returns:
    - ΔHALE_gap: Change in predicted HALE gap (in years)
    """
    # Create modified data with new predictor value(s)
    # Predict HALE gap with original and modified data
    # Return difference
```

**Step 5.2: Run Counterfactual Scenarios**
- Select country pairs of interest (e.g., US vs Netherlands, US vs other OECD countries)
- For each pair, systematically change each predictor from country A to country B's values
  - Can change male value, female value, or both
  - Example: Change US male smoking to Netherlands male smoking value
  - Example: Change both US male and female smoking to Netherlands values
  - Example: Change US maternal mortality to Netherlands maternal mortality
- Calculate predicted change in HALE gap for each counterfactual
- Identify which factors (and which gender) would have largest impact on closing the gap

**Step 5.3: Summarize Counterfactual Results**
- Create table/matrix showing counterfactual impacts
- Visualize which factors would have largest impact for specific country comparisons
- Identify most actionable factors (e.g., if reducing overdose rates would have large impact)

### Phase 6: Sensitivity Analysis

**Step 6.1: Robustness Checks**
- Test model with different predictor combinations (e.g., exclude highly correlated predictors)
- Test sensitivity to outliers (remove influential observations, refit model)
- Test sensitivity to missing data (impute vs complete-case analysis)

**Step 6.2: Alternative Specifications**
- Test models with different predictor transformations (e.g., ratios instead of differences)
- Compare results across Ridge, Lasso, and Elastic Net models
- Document any substantial differences in conclusions

### Phase 7: Documentation and Reporting

**Step 7.1: Document Findings**
- Summarize which factors explain largest portions of HALE gap variation
- Document model performance (R², cross-validation scores)
- Report counterfactual insights (which factors would have largest impact)

**Step 7.2: Prepare for Future Analysis**
- Document data limitations and coverage
- Note any countries excluded and reasons
- Prepare framework for temporal analysis (Phase 2, future work)
- Prepare framework for larger country set analysis (future work)

### Implementation Notes

- **Primary Tools**: scikit-learn for model fitting (`Ridge`, `Lasso`, `ElasticNet`, `GridSearchCV`, `StandardScaler`)
- **Secondary Tools**: statsmodels for diagnostics if needed
- **Data Sources**: Use `who_data.py` for downloading WHO indicators
- **Country Codes**: Use `oecd_codes` from `utils.py` for OECD country filtering
- **Target Variable**: HALE gap = Female HALE - Male HALE (difference, not ratio)
- **Focus**: Direct causal indicators only (mortality/health indicators), not indirect indicators like GDP

## Expected Outcomes
<!-- What do you hope to discover? -->

## Notes
<!-- Add any additional notes, ideas, or observations -->

