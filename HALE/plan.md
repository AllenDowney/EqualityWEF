# HALE Differences Between Countries - Project Plan

## Project Overview
Exploring the causes of differences in Healthy Life Expectancy (HALE) between countries.

## Research Questions
In most countries, women live longer than men, as measured by raw life expectancy and HALE.
These differences are sometimes considered to be natural, but in some high-income countries, the differences are quite small, which suggests that the factors that cause differences can be mitigated.

The goal of this project is to see what part of the difference in HALE can be explained statistically by differences in various factors that are likely to contribute differentially to male and female life expectancy.

Background: https://ourworldindata.org/why-do-women-live-longer-than-men

## Style Guide

### Terminology

- **Never use "predictor indicator"** - Use either "predictor" or "indicator" as appropriate:
  - Use "predictor" when referring to variables used in models (e.g., "predictors in the Bayesian model", "predictor gaps", "predictor rates")
  - Use "indicator" when referring to data sources or measurements intended to quantify something in the world (e.g., "IHME indicators", "health indicators", "mortality indicators")
  - In most contexts, "predictor" is preferred when discussing variables used in statistical models

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

1. **HALE Data Retrieval** (`get_hale_data`): ✅ **Implemented**
   - Retrieves Healthy Life Expectancy (HALE) data by sex (Male, Female, Both sexes)
   - Uses indicator code `WHOSIS_000002` for HALE at birth
   - Returns data with columns: Country, CountryCode, Year, Sex, HALE_Years, HALE_Low, HALE_High
   - Supports filtering by specific years
   - This is the **primary target variable** for our analysis (gender gap = Female HALE - Male HALE)

2. **Life Expectancy Data Retrieval** (`get_life_expectancy_data`): ✅ **Implemented**
   - Retrieves Life Expectancy at birth data by sex (Male, Female, Both sexes)
   - Uses indicator code `WHOSIS_000001` for Life Expectancy at birth
   - Returns data with columns: Country, CountryCode, Year, Sex, LifeExpectancy_Years, LifeExpectancy_Low, LifeExpectancy_High
   - Supports filtering by specific years
   - This is the **secondary target variable** for our analysis (gender gap = Female LE - Male LE)
   - Data coverage: 12,936 records, 196 countries, 2000-2021 (matches HALE coverage)

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
le_df = client.get_life_expectancy_data(years=[2015, 2020, 2023])
cardio_df = client.get_cardiovascular_death_rates()
```

**Data Output:**
- Saves HALE data to `who_hale_data.csv` ✅
- Saves Life Expectancy data to `who_life_expectancy_data.csv` ✅
- Saves cardiovascular death rates to `who_cardiovascular_death_rates.csv`
- Includes both full datasets and recent-year filtered versions

**Relevance to Project:**
- Provides the **primary target variable** (HALE by sex) needed to calculate gender gaps ✅
- Provides the **secondary target variable** (Life Expectancy by sex) for comparative analysis ✅
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

**Notebook Organization:**
- **`eda.md`**: Contains Phase 1 (Data Preparation) and Phase 2 (Exploratory Data Analysis). This notebook loads all data, prepares predictors and both target variables (HALE gap and Life Expectancy gap), performs exploratory analysis, creates summary tables with correlations, and saves the final dataset to HDF5 for use in modeling. Summary tables are written to HTML files in `jb/tables/` for inclusion in the JupyterBook site.
- **`model2.md`**: Contains Phase 3 (Model Fitting), Phase 4 (Model Interpretation), and subsequent phases for **Life Expectancy gap analysis**. This notebook loads the saved data from `eda.md` and performs all modeling and analysis using `LifeExpectancy_gap` as the target variable. Uses Mid + Gap format for predictors (not separate Male/Female columns).
- **`life_expectancy_model.md`**: Copy of `model2.md` adapted for HALE gap analysis. Uses `HALE_gap` as the target variable instead of `LifeExpectancy_gap`. (Note: Currently `model2.md` analyzes Life Expectancy gap, so this would be the HALE gap version.)

### Phase 1: Data Preparation (OECD Countries, Most Recent Data)

**Step 1.1: Load and Prepare Data Using Existing Functions**
- Use existing functions from `eda.md`:
  - `load_and_inventory(filename)` - Loads WHO CSV files, filters to year 2000-2019 (excludes 2020+ to avoid COVID-19 pandemic distortions) and country-level data (CountryCode == "COUNTRY")
  - `compute_gender_gap(df, value_col, sexes)` - Computes separate columns for each sex and gap column
  - `summarize_gap(df, col, sexes=None)` - Computes gender gaps and selects most recent year per country
  - `get_oecd(df)` - Filters DataFrame to OECD countries using `oecd_codes` from `utils.py` (38 countries)

**Note on data years**: We exclude 2020 and later years to avoid COVID-19 pandemic distortions. The pandemic had significant impacts on mortality patterns that may not reflect underlying health factors. Using 2019 or earlier data provides a more stable baseline for understanding the HALE gender gap.

**Step 1.2: Download and Prepare Target Variables (HALE and Life Expectancy Gender Gaps)** ✅ **COMPLETE**
- **HALE data:** ✅ **Downloaded and implemented**
  - Load HALE data: `data/who_hale_data.csv`
  - Use `load_and_inventory()` to load and filter data
  - Map sex codes: `{'SEX_BTSX': 'Both', 'SEX_FMLE': 'Female', 'SEX_MLE': 'Male'}`
  - Use `summarize_gap(hale, 'HALE_Years', sexes=['Male', 'Female'])` to:
    - Compute separate columns: `HALE_Years_Male` and `HALE_Years_Female`
    - Select most recent year available for each country
    - Returns `hale_recent` DataFrame indexed by Country with male/female columns
  - Calculate target variable: `HALE_gap = HALE_Years_Female - HALE_Years_Male` (in years)
  - Filter to OECD countries using `get_oecd(hale_recent)`
- **Life Expectancy data:** ✅ **Downloaded and implemented**
  - ✅ **Data downloaded**: Life Expectancy data downloaded from WHO GHO API using indicator code `WHOSIS_000001`
  - ✅ **File created**: `data/who_life_expectancy_data.csv` (12,936 records, 196 countries, 2000-2021)
  - ✅ **Method added**: `get_life_expectancy_data()` method added to `who_data.py` with CLI support
  - Load life expectancy data: `data/who_life_expectancy_data.csv`
  - Use `load_and_inventory()` to load and filter data (same methodology as HALE)
  - Use `summarize_gap(le, 'LifeExpectancy_Years', sexes=['Male', 'Female'])` to:
    - Compute separate columns: `LifeExpectancy_Years_Male` and `LifeExpectancy_Years_Female`
    - Select most recent year available for each country
    - Returns `le_recent` DataFrame indexed by Country with male/female columns
  - Calculate target variable: `LifeExpectancy_gap = LifeExpectancy_Years_Female - LifeExpectancy_Years_Male` (in years)
  - Filter to OECD countries using `get_oecd(le_recent)`
  - ✅ **EDA updated**: Life Expectancy data loading and exploration added to `eda.md`
  - ✅ **HDF5 updated**: Both `target_hale` and `target_le` saved to HDF5 file for modeling

**Step 1.3: Download and Prepare Predictor Variables** ✅ **COMPLETE**
For each predictor, load data and use `summarize_gap()` to get most recent year per country. **Use Mid (midpoint) and Gap columns as predictors** (not separate Male/Female columns), except for female-only indicators (maternal mortality):

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
    - Note: NCD = Non-Communicable Disease. Combined indicator (cardiovascular, cancer, diabetes, chronic respiratory)

**Note on excluded indicators:**
- **Intimate Partner Violence (IPV) prevalence** - Excluded from the model because: (1) data is missing for some OECD countries, and (2) it is likely not a strong direct indicator of HALE gender gap (it affects morbidity/quality of life more than mortality, and the relationship to HALE gap is indirect and complex).

- **Smoking prevalence** - Excluded from the model because it is a long-lag cause of some of the immediate causes of death included in the analysis (e.g., cardiovascular disease, chronic respiratory disease). Including both smoking and its downstream effects would create redundancy and make it difficult to interpret which factors are most directly associated with the HALE gender gap.

- **NCD Mortality (30-70 years)** - Excluded from the model because it is a catch-all combined indicator (cardiovascular disease, cancer, diabetes, chronic respiratory disease) that is not something we can target with specific policies. The model uses the individual cause-specific indicators instead, which are more actionable and interpretable.

- **WHO Cardiovascular Disease** - Excluded from the model because it has been replaced with the IHME version (`cardiovascular_ihme_recent`), which has better temporal coverage (2000-2021 vs. only 2004 data for WHO).

- **WHO Diabetes** - Excluded from the model because it has been replaced with the IHME version (`diabetes_ihme_recent`), which has better temporal coverage (2000-2021 vs. only 2004 data for WHO).

- ✅ For each indicator:
  - Use `load_and_inventory()` to load and filter data
  - Use `summarize_gap()` to get most recent year per country (creates `Mid_` and `Gap_` columns)
  - Filter to OECD countries using `get_oecd()`
  - For indicators with both male and female data: keep both `Mid_` and `Gap_` columns (also keep `_Male` and `_Female` columns for counterfactual analysis)
  - For female-only indicators (maternal mortality): keep the `_Female` column
  - **Note**: The model uses `Mid_` and `Gap_` columns, while `_Male` and `_Female` columns are kept for counterfactual analysis but not used as predictors

**Step 1.4: Merge All Predictors into Single Dataset** ✅ **COMPLETE**
- ✅ Merge all predictor DataFrames (indexed by Country) into single country-level dataset
- ✅ Use outer merge to keep all countries, document which countries have missing data for which indicators
- ✅ Create missing data report showing coverage for each indicator across OECD countries
- ✅ The merged dataset has one row per country with columns for each predictor:
  - `Mid_{indicator}` and `Gap_{indicator}` columns for most indicators (used in modeling)
  - `{indicator}_Male` and `{indicator}_Female` columns (kept for counterfactual analysis)
  - `MaternalMortality_Female` for maternal mortality (female-only)

**Step 1.5: Handle Missing Data and Create Final Dataset** ✅ **COMPLETE**
- ✅ Since missing data is expected to be minimal for OECD countries, use complete-case analysis for primary model
- ✅ Document any countries excluded due to missing critical predictors
- ✅ Create final analysis dataset with:
  - **Target variables**: Both `HALE_gap` and `LifeExpectancy_gap` (Female - Male, in years)
  - Predictors: All `Mid_` and `Gap_` columns (used in modeling), plus `_Male` and `_Female` columns (kept for counterfactual analysis)
  - Index: Country codes (OECD countries only)
- ✅ Save final dataset to HDF5 file with both target variables for use in modeling notebooks


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

**Step 2.3: Extreme Values and Country Rankings**
- **For each indicator** (both male and female values):
  - Create table showing countries with highest and lowest values
  - Include: Country name, value, and rank
  - Show top 5 and bottom 5 countries for each indicator
  - This helps identify which countries drive variation in each predictor
- **For gender gaps** (computed gaps for each indicator):
  - Create table showing countries with largest and smallest gaps
  - Include: Country name, male value, female value, computed gap (Male - Female), and rank
  - Show top 5 and bottom 5 countries for each indicator gap
  - This helps identify which countries have the most extreme gender differences
- **For HALE gap** (target variable):
  - Create table showing countries with largest and smallest HALE gaps
  - Include: Country name, Male HALE, Female HALE, HALE gap (Female - Male), and rank
  - Show all countries ranked by HALE gap
  - This provides context for understanding the target variable distribution

**Step 2.4: Summary Statistics by Indicator** ✅ **COMPLETE**
- ✅ Created summary tables with one row per indicator showing:
  - Median, Min, and Max of midpoint values (rates) across countries
  - Median, Min, and Max of gender gaps across countries
  - Separate tables for predictor indicators and target variables (HALE and Life Expectancy)
  - All values formatted to 3 significant digits
  - Indicator kept as a column (not index) in all tables
- ✅ Added correlation columns to predictor tables:
  - Corr HALE: Correlation between predictor and HALE gap
  - Corr LE: Correlation between predictor and Life Expectancy gap
  - Color coding: highest correlation highlighted in green, lowest in pink/red
- ✅ Created rate-gap correlation table:
  - Shows correlation between Rate (Mid) and Gap for each indicator
  - Sorted by correlation magnitude
  - Formatted to 3 significant digits
- ✅ Created top 10 correlation tables:
  - Top 10 correlations (by magnitude) between rates and other rates
  - Top 10 correlations (by magnitude) between gaps and other gaps
  - Both tables show indicator pairs and their correlations
  - Formatted to 3 significant digits
- ✅ All tables written to HTML files in `jb/tables/` directory:
  - `predictor_rates.html` - Predictor indicators, rates (with correlation highlighting)
  - `predictor_gaps.html` - Predictor indicators, gaps (with correlation highlighting)
  - `target_rates.html` - Target variables (HALE, LE), rates
  - `target_gaps.html` - Target variables (HALE, LE), gaps
  - `rate_gap_correlation.html` - Correlation between Rate and Gap for each indicator
  - `rate_rate_correlation_top10.html` - Top 10 rate-rate correlations
  - `gap_gap_correlation_top10.html` - Top 10 gap-gap correlations
- ✅ Tables included in JupyterBook site (`jb/hale_gaps.md`) using MyST `{include}` directive


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

**Step 4.1: Coefficient Analysis** ✅ **COMPLETE** (for both Life Expectancy and HALE gaps)
- ✅ Extract coefficients from selected model (on standardized scale) - Done in `model_le.md` and `model_hale.md` "Extract Elastic Net Coefficients" section
- ✅ Calculate feature importance: `importance = |coefficient| × std(predictor)` - Done in "Calculate Feature Importance" section
- ✅ Rank predictors by importance to identify largest contributors to gap variation - Done, sorted by importance
- ✅ Calculate indicator-level importance (aggregating Mid and Gap predictors) - Done in "Importance by Indicator" section
- ✅ Counterfactual predictions implemented in Phase 5 (see below)

**Coefficient-Based Importances from ElasticNet**

| Indicator | Male Importance | Female Importance | Total Importance |
|-----------|----------------|-------------------|-------------------|
| AlcoholDeathRate | 62.78 | 14.83 | 77.60 |
| CardioDeathRate | 0.00 | 26.92 | 26.92 |
| ChronicRespiratoryDeathRate | 9.15 | 13.64 | 22.79 |
| UnintentionalInjuriesDeathRate | 0.00 | 3.10 | 3.10 |
| SuicideRate | 2.12 | 0.00 | 2.12 |
| MaternalMortalityRatio | — | 1.29 | 1.29 |
| RoadTrafficDeathRate | 0.93 | 0.07 | 1.00 |
| HomicideRate | 0.51 | 0.00 | 0.51 |
| DiabetesDeathRate | 0.00 | 0.10 | 0.10 |
| PoisoningRate | 0.00 | 0.00 | 0.00 |
| U5MR | 0.00 | 0.00 | 0.00 |
| DrugDisorderDeathRate | 0.00 | 0.00 | 0.00 |

**Summary of Coefficient-Based Importance Results:**

Ranked by total importance (sum of male and female importance):

1. **Alcohol-attributable deaths** (77.60) — Dominates the model, accounting for more than half of the total importance across all indicators. This is by far the most important predictor, consistent with permutation importance results.

2. **Cardiovascular disease death rates** (26.92) — Second most important indicator. The coefficient-based importance shows cardiovascular disease has a strong linear relationship with HALE gap, even though permutation importance ranked it lower.

3. **Chronic respiratory disease death rates** (22.79) — Third most important, showing that respiratory mortality patterns are a significant contributor to HALE gap variation.

4. **Unintentional injuries** (3.10) — Moderate importance, suggesting unintentional injury patterns contribute to HALE gap variation.

5. **Suicide rates** (2.12) — Low but non-zero importance.

6. **Maternal mortality** (1.29) — Very low importance, as expected given that maternal mortality is already very low in all OECD countries.

7. **Road traffic death rates** (1.00) — Very low importance.

8. **Homicide rates** (0.51) — Very low importance.

9. **Diabetes death rates** (0.10) — Near-zero importance.

10. **Zero importance indicators**: **PoisoningRate**, **U5MR**, and **DrugDisorderDeathRate** all have zero importance, suggesting they contribute little to explaining HALE gap variation in OECD countries.

**Key Findings:**
- The top three indicators (Alcohol, Cardiovascular, Chronic Respiratory) account for the vast majority of the model's explanatory power.
- **Alcohol-attributable deaths** is overwhelmingly the most important factor, suggesting that alcohol-related mortality is the primary driver of HALE gender gap variation in OECD countries.
- The male/female allocation within each indicator should be interpreted cautiously, as it may reflect statistical artifacts (collinearity, regularization) rather than substantive differences in how male vs. female rates contribute to the gap.

**Step 4.2: Model Diagnostics** ✅ **COMPLETE** (for both Life Expectancy and HALE gaps)
- ✅ Calculate R² (explained variance) - R² calculated via cross-validation in Phase 3 (CV_R2_Score)
- ✅ Residual analysis (check for patterns, outliers) - Done in `model_le.md` and `model_hale.md`:
  - Residual vs. predicted values plot
  - Histogram of residuals
  - Identification of outliers (residuals > 2 standard deviations)
  - Residuals by country table
  - Residuals vs. top predictors plots
- ⚠️ Check for influential observations (Cook's distance, leverage) - Not yet implemented (not needed for current analysis)

**Step 4.3: Feature Importance Visualization** ✅ **COMPLETE** (for both Life Expectancy and HALE gaps)
- ✅ Create bar chart showing coefficient magnitudes (standardized) - Done in `model_le.md` and `model_hale.md` "Visualize Predictor Importance" section (all predictors with non-zero coefficients)
- ✅ Highlight top contributors to gap variation - Done in predictor importance analysis
- ✅ Create indicator-level importance visualization - Done in "Visualize Indicator Importance" section
- ✅ Compare importance across different models (Ridge vs Lasso vs Elastic Net) - Coefficients extracted for all three models in Phase 3, with comparison tables created


### Phase 5: Counterfactual Analysis ✅ **COMPLETE** (for both Life Expectancy and HALE gaps)

**Step 5.1: Counterfactual Analysis Implementation** ✅ **COMPLETE**
- ✅ Counterfactual analysis implemented directly in `model_le.md` and `model_hale.md` (not in separate predict.md notebook)
- ✅ Uses data loading code from HDF5 file (predictors and target)
- ✅ Uses Elastic Net model trained in Phase 3

**Step 5.2: Gap Predictor Analysis Table** ✅ **COMPLETE**
- ✅ Created gap extremes table showing for each gap predictor:
  - Minimum gap value and country with minimum gap
  - Maximum gap value and country with maximum gap
- ✅ Implemented in `model_le.md` and `model_hale.md` as `gap_extremes` dictionary

**Step 5.3: Counterfactual Prediction Function** ✅ **COMPLETE**
- ✅ Created `counterfactual_predictions()` function that:
  - For each gap predictor, finds the best attainable gap:
    - If current gap is positive (Male > Female): finds country with minimum gap (smallest positive gap)
    - If current gap is negative (Female > Male): finds country with maximum gap (largest positive gap)
  - If the target gap has the opposite sign of the current gap, sets the target to zero
  - Adjusts Male or Female values to achieve the target gap:
    - If current gap is positive (Male > Female): bring men toward women's level
    - If current gap is negative (Female > Male): bring women toward men's level
  - Recomputes Mid and Gap values from adjusted Male/Female values
  - Generates counterfactual predictions using the adjusted values
- ✅ Created `counterfactuals_for_country()` function that generates counterfactual table with columns:
  - Indicator
  - Current gap
  - Target gap
  - Target Country (or "" if target has been set to zero)
  - Change in LE/HALE gap (predicted gap change)
- ✅ Tables sorted by importance (descending) and formatted with spaces in column names
- ✅ Results exported to HTML tables: `counterfactuals_usa_le.html` and `counterfactuals_usa_hale.html`
- ✅ Aggregate effects calculated: sum of gap-closing indicators and gap-widening indicators

### Phase 6: Documentation and Reporting

**Step 6.1: Document Findings** ✅ **COMPLETE**
- ✅ Summary tables created in `eda.md` showing indicator statistics and correlations
- ✅ JupyterBook site created (`jb/hale_gaps.md`) with summary tables included
- ✅ Summarize which factors explain largest portions of gap variation - Done for both Life Expectancy and HALE in `model_le.md` and `model_hale.md`
- ✅ Document model performance (R², cross-validation scores) - Done for both Life Expectancy and HALE
- ✅ Report counterfactual insights (which factors would have largest impact) - Complete for both LE and HALE, documented in `hale_gaps.md`

**Step 6.2: Prepare for Future Analysis**
- ✅ Document data limitations and coverage - Done in `eda.md` (missing data reports, year coverage)
- ✅ Note any countries excluded and reasons - Done in `eda.md` (complete-case analysis)
- ✅ Framework for temporal analysis defined - See Phase 9: Temporal Analysis (future work)
- ⚠️ Prepare framework for larger country set analysis (future work) - Not yet implemented

**Step 6.3: JupyterBook Site** ✅ **COMPLETE**
- ✅ Created JupyterBook site structure in `jb/` directory:
  - `myst.yml` - JupyterBook 2 configuration (replaced `_config.yml` and `_toc.yml`)
  - `hale_gaps.md` - Main document with summary tables
  - `Makefile` - Commands to build and deploy the site
- ✅ Summary tables included using MyST `{include}` directive:
  - Target variables (HALE and Life Expectancy) rates and gaps
  - Predictor indicators rates and gaps (with correlation highlighting)
  - Rate-gap correlation table
  - Top rate-rate and gap-gap correlation tables
- ✅ Tables formatted with 3 significant digits and color coding for correlations
- ✅ Vocabulary updated: "midpoint" → "overall rate" (with explanation on first use)
- ✅ Clarified "median" means "median across countries" on first use

**Step 6.4: Export Model Results to JupyterBook** ✅ **COMPLETE**
- ✅ Export Life Expectancy model results from `model_le.md` as HTML tables:
  - Model performance summary (R², MAE, cross-validation scores) → `model_comparison_le.html`
  - Feature importance table (predictor-level) → `predictor_importance_le.html`
  - Indicator-level importance table → `indicator_importance_le.html`
  - Coefficient comparison table (Elastic Net vs OLS) → `elasticnet_ols_coefficient_comparison_le.html`
  - Performance comparison table → `performance_comparison_le.html`
  - Country-level predictions and residuals → `predictions_comparison_le.html`, `residuals_by_country_le.html`
  - Counterfactual analysis table → `counterfactuals_usa_le.html`
- ✅ Export HALE model results from `model_hale.md` as HTML tables (same format as Life Expectancy, with `_hale` suffix)
- ✅ All figures exported to `jb/figs/` directory with appropriate suffixes (`_le` or `_hale`)
- ✅ Incorporate Life Expectancy results into `hale_gaps.md` - Complete with full sections for model performance, feature importance, diagnostics, and counterfactual analysis
- ✅ Incorporate HALE results into `hale_gaps.md` - Complete with parallel sections mirroring LE structure
- ✅ Added comparison section summarizing differences between LE and HALE results
- ✅ Report follows style guide: level 2 and 3 headings, moderate formatting, Allen Downey writing style
- ✅ Added contextual explanations for findings (e.g., cardiovascular disease and age, neoplasms and smoking history)

### Phase 8: Life Expectancy Gender Gap Analysis

**Overview:**
Perform the same analysis (Phases 3-5, 6) using period life expectancy as the target variable instead of HALE. This allows comparison of which factors explain the gender gap in overall life expectancy versus healthy life expectancy. The life expectancy data is already prepared in Phase 1 (Step 1.2) and saved to the HDF5 data file alongside HALE data. See "Recommendations for Life Expectancy Gender Gap Model" section (lines 242-333) for detailed discussion of predictor selection and model structure.

**Step 8.1: Create Life Expectancy Model Notebook** ✅ **COMPLETE**
- ✅ **Note**: `model_le.md` (renamed from `model2.md`) performs Life Expectancy gap analysis (uses `target_le` / `LifeExpectancy_gap` as target variable)
- ✅ Loads the same HDF5 data file created in Phase 1 (which contains both target variables)
- ✅ Uses the same predictor variables (Mid + Gap format, not separate Male/Female columns)
- ✅ **HALE gap model notebook created**: `model_hale.md` created by copying `model_le.md` and adapting it to use `HALE_gap` as the target variable

**Step 8.2: Model Fitting for Life Expectancy** ✅ **COMPLETE** (in `model_le.md` and `model_hale.md`)
- ✅ Fit Ridge, Lasso, and Elastic Net models with cross-validation for both LE and HALE
- ✅ Use 5-fold cross-validation for model selection
- ✅ Compare model performance (R², MAE) across models
- ✅ Selected Elastic Net as primary model for both LE and HALE (consistent with methodology)

**Step 8.3: Model Interpretation for Life Expectancy** ✅ **COMPLETE** (in `model_le.md` and `model_hale.md`)
- ✅ Extract coefficients and calculate feature importance for both LE and HALE
- ✅ Rank predictors by importance for both life expectancy gap and HALE gap
- ✅ Calculate indicator-level importance (aggregating Mid and Gap predictors) for both models
- ✅ Create visualizations of predictor importance for both models (all non-zero coefficients)
- ✅ Perform model diagnostics (residual analysis, outlier identification) for both models
- ✅ **Compare with HALE results**: Comparison section added to `hale_gaps.md` summarizing differences between LE and HALE results

**Step 8.4: Counterfactual Analysis for Life Expectancy** ✅ **COMPLETE**
- ✅ Repeat Phase 5 analysis for both LE and HALE:
  - ✅ Create counterfactual prediction function for both life expectancy gap and HALE gap
  - ✅ Generate gap predictor analysis table (gap extremes) for both models
  - ✅ Test counterfactual scenarios for United States (example country)
  - ✅ Calculate aggregate effects (sum of gap-closing and gap-widening indicators)
- ✅ **Compare with HALE counterfactuals**: Comparison documented in `hale_gaps.md` showing which factors have larger/smaller impact on life expectancy gap vs HALE gap
- ✅ Counterfactual results exported to HTML tables and included in report

**Step 8.5: Export and Document Results** ✅ **COMPLETE**
- ✅ **Export Life Expectancy model results** (from `model_le.md`) as HTML tables:
  - Model performance summary (R², MAE, cross-validation scores) → `model_comparison_le.html`
  - Feature importance table (predictor-level) → `predictor_importance_le.html`
  - Indicator-level importance table → `indicator_importance_le.html`
  - Coefficient comparison table (Elastic Net vs OLS) → `elasticnet_ols_coefficient_comparison_le.html`
  - Performance comparison table → `performance_comparison_le.html`
  - Country-level predictions and residuals table → `predictions_comparison_le.html`, `residuals_by_country_le.html`
  - Counterfactual analysis table → `counterfactuals_usa_le.html`
- ✅ **Incorporate Life Expectancy results into `hale_gaps.md`**:
  - ✅ Added comprehensive section for Life Expectancy model results
  - ✅ Included exported HTML tables using MyST `{include}` directive
  - ✅ Added figures using MyST `{figure}` directive
- ✅ **Create HALE gap model notebook**:
  - ✅ Created `model_hale.md` by copying `model_le.md` and adapting to use `HALE_gap` as target variable
  - ✅ Ran model fitting, interpretation, and diagnostics
- ✅ **Export HALE model results** as HTML tables (same format as Life Expectancy, with `_hale` suffix)
- ✅ **Incorporate HALE results into `hale_gaps.md`**:
  - ✅ Added comprehensive section for HALE model results (mirroring LE structure)
  - ✅ Included exported HTML tables and figures
- ✅ **Compare HALE vs Life Expectancy Results:**
  - ✅ Added comparison section in `hale_gaps.md` summarizing differences
  - ✅ Side-by-side comparison of feature importance rankings
  - ✅ Compare which indicators explain more/less of each gap
  - ✅ Compare counterfactual predictions (which factors would have larger impact on each gap)
  - ✅ Document differences in model performance (R², MAE)
  - ✅ Identify indicators that are more important for one gap vs the other
- ✅ **Document Findings:**
  - ✅ Summarize which factors explain largest portions of life expectancy gap variation
  - ✅ Compare with HALE findings to identify common vs unique drivers
  - ✅ Report counterfactual insights for both life expectancy gap and HALE gap
  - ✅ Document substantial differences between HALE and life expectancy models
  - ✅ Added contextual explanations (e.g., cardiovascular disease and age, neoplasms and smoking history)
  - ✅ Clarified terminology (e.g., "Cardiovascular disease" instead of "Cardiovascular")
  - ✅ Added note explaining difference between importance (general effectiveness) and counterfactual results (country-specific impact)

**Key Differences from HALE Analysis:**
- **Target Variable**: Life expectancy gap (Female - Male) instead of HALE gap
- **Predictor Set**: Same predictors as HALE model (see "Recommendations for Life Expectancy Gender Gap Model" section)
- **Focus**: Life expectancy captures all years lived (healthy and unhealthy), while HALE focuses on healthy years only
- **Expected Similarities**: Both are calculated from birth, so both should be affected by the same mortality patterns (adult mortality, infant/child mortality, etc.)
- **Expected Differences**: The relative importance of early-life vs adult mortality may differ, and factors affecting morbidity but not mortality may be less relevant for life expectancy

**Implementation Notes:**
- Life expectancy data is already prepared in Phase 1 (Step 1.2) and saved to the HDF5 data file
- ✅ `model_le.md` (renamed from `model2.md`) uses `LifeExpectancy_gap` as the target variable
- ✅ **HALE gap model created**: `model_hale.md` created by copying `model_le.md` and adapting it to use `HALE_gap` as the target variable
- ✅ Reused the same data preparation code, changed the target variable reference
- ✅ Maintained consistency in model fitting and interpretation approaches to enable direct comparison
- ✅ All output files (tables and figures) use `_le` or `_hale` suffixes to distinguish between models

### Phase 9: Temporal Analysis (Future Work)

**Overview:**
Repeat the analysis (Phases 1-5) at multiple time points to understand how the HALE and Life Expectancy gender gaps, and their predictors, have changed over time. This temporal analysis will help identify:
- Whether the gender gap is narrowing or widening over time
- Which predictors have become more or less important over time
- How changes in specific indicators (e.g., smoking rates, alcohol consumption) have affected the gender gap
- Whether the relative importance of different factors has shifted

**Step 9.1: Replace WHO Indicators with IHME Indicators for Consistency** ✅ **COMPLETE**

**Rationale**: Many IHME indicators have better temporal coverage (1990-2023) than their WHO counterparts, and using IHME data consistently will provide:
- More uniform temporal coverage across indicators
- Consistent methodology and data sources
- Ability to analyze longer time periods (starting from 1990 instead of 2000)

**Indicators Replaced**:
1. ✅ **Alcohol-attributable death rates**: Replaced WHO `SA_0000001832` (2019 only) with IHME `B.7.1 Alcohol use disorders` (1990-2023)
2. ✅ **Suicide rates**: Replaced WHO `MH_12` (2000-2021) with IHME `B.7.3 Self-harm` (1990-2023)
3. ✅ **Homicide rates**: Replaced WHO `VIOLENCE_HOMICIDERATE` (2000-2021) with IHME `B.7.4 Interpersonal violence` (1990-2023)
4. ✅ **Road traffic crash death rates**: Replaced WHO `SA_0000001459` (2019 only) with IHME `Road injuries` (1990-2023)
5. ✅ **Cardiovascular disease death rates**: Using IHME `B.2 Cardiovascular diseases` (replaces WHO 2004-only data)
6. ✅ **Diabetes death rates**: Using IHME `B.8.1.2 Diabetes mellitus type 2` (replaces WHO 2004-only data)
7. ✅ **Chronic respiratory disease death rates**: Using IHME `B.3 Chronic respiratory diseases`
8. ✅ **Unintentional injuries death rates**: Using IHME `Unintentional injuries`
9. ✅ **Neoplasms death rates**: Using IHME `B.1 Neoplasms`
10. ✅ **Drug use disorders**: Using IHME `B.7.5 Drug use disorders` (replaces WHO Poisoning)

**Indicators Removed**:
- ✅ **WHO Poisoning**: Removed in favor of IHME Drug Use Disorders (better temporal coverage, more comprehensive)
- ✅ **Maternal mortality**: Removed due to counterintuitive positive coefficient (higher female mortality associated with larger gap, contrary to expected mechanism)
- ✅ **Under-five mortality rate (Childhood)**: Removed due to very low importance (0.0558 in LE model, not in top 10 for HALE) and limited temporal coverage. The IHME alternative (All-Cause Deaths Under 5, per 100,000 population) is confounded with age structure and fertility rates, making it methodologically inappropriate. Removing it simplifies the model without sacrificing meaningful predictive power.

**Indicators Added**:
- ✅ **Liver Disease**: Added IHME `B.7.2 Cirrhosis and other chronic liver diseases` (1990-2023) - captures all liver disease deaths (alcoholic and non-alcoholic)

**Indicators Kept from WHO** (no IHME equivalent or WHO has better coverage):
- **HALE and Life Expectancy**: Keep WHO data (primary target variables)
- ~~**Under-five mortality rate**: Keep WHO `MDG_0000000007` (excellent coverage: 1932-2023, per 1,000 live births)~~ → **REMOVED** (see validation experiment #8)

**Implementation**:
- ✅ Updated `eda.md` to load IHME versions of alcohol, suicide, homicide, road injuries, and other indicators
- ✅ Updated data loading code to use IHME indicators where they provide better temporal coverage
- ✅ All IHME indicators use the same `load_ihme_indicator()` function for consistency
- ✅ Documented which indicators are from IHME vs WHO in the data inventory
- ✅ Updated `column_name_mapping` in `utils.py` to map IHME indicator names to consistent short names (e.g., `AlcoholUseDisordersDeathRate` → `Alcohol`)
- ✅ Added comparison section in `eda.md` showing side-by-side scatter plots comparing WHO and IHME indicators where both are available

**Validation: Summary of Experiments Completed** ✅ **COMPLETE**

A comprehensive validation process was completed, replacing indicators one at a time and comparing results to identify any major changes. All experiments are documented in `validation.md`. Summary of findings:

**1. Alcohol: WHO → IHME** ✅ **COMPLETE**
- **Major Finding**: Alcohol importance dropped dramatically (87% reduction) due to definitional differences
  - WHO: "Alcohol-attributable all-cause deaths" (includes all deaths where alcohol is a contributing factor)
  - IHME: "Alcohol use disorders" (only direct alcohol use disorder deaths)
- **Impact**: Alcohol dropped from #1 to #4 (LE) and #2 to #5 (HALE)
- **Model Performance**: Improved (R² +2.6% for LE, +6.3% for HALE)
- **Conclusion**: Definitional differences are substantial; IHME definition is more restrictive

**2. Suicide: WHO → IHME** ✅ **COMPLETE**
- **Major Finding**: Suicide importance increased (+139% for LE, +42% for HALE)
- **Impact**: Suicide moved into top 4-5 indicators
- **Model Performance**: Improved (R² +2.9% for LE, +6.4% for HALE)
- **Conclusion**: IHME data may capture suicide-related mortality more effectively

**3. Homicide: WHO → IHME** ✅ **COMPLETE**
- **Major Finding**: Homicide dropped out of Life Expectancy model entirely (not selected by Elastic Net)
- **Impact**: Homicide importance decreased for HALE (-28%)
- **Model Performance**: Unchanged (same as suicide replacement)
- **Conclusion**: IHME homicide data less predictive than WHO data, or other indicators (Suicide) capture same variance

**4. Road Traffic: WHO → IHME** ✅ **COMPLETE**
- **Major Finding**: RoadTraffic has very low importance in both models (0.111 for LE, 0.633 for HALE)
- **Impact**: RoadTraffic ranked #8-9, not a major factor
- **Model Performance**: Improved (R² +2.2% for LE, +10.8% for HALE)
- **Conclusion**: Road traffic deaths not a major predictive factor for gender gaps

**5. Poisoning (WHO) → Drug Disorders (IHME)** ✅ **COMPLETE**
- **Major Finding**: Neither indicator was selected by Elastic Net (importance = 0)
- **Impact**: No impact on model performance
- **Conclusion**: Drug-related mortality does not contribute significantly to explaining gender gaps

**6. Adding Liver Disease Indicator** ✅ **COMPLETE**
- **Major Finding**: Liver Disease has moderate importance (2.12 for LE ranked #4, 2.39 for HALE ranked #6)
- **Impact**: Higher importance than Alcohol in both models
- **Model Performance**: Small changes (R² +0.8% for LE, -5.9% for HALE)
- **Conclusion**: Liver Disease captures broader set of alcohol-related mortality than narrow IHME "alcohol use disorders" definition

**7. Removing Maternal Mortality** ✅ **COMPLETE**
- **Major Finding**: Maternal Mortality had counterintuitive positive coefficient (higher female mortality associated with larger gap)
- **Impact**: 
  - Cardiovascular gained substantial importance in HALE model (+111%, moved from #4 to #2)
  - Homicide gained substantial importance in HALE model (+60%, moved from #8 to #5)
  - Homicide newly selected for Life Expectancy model
- **Model Performance**: Minimal impact (R² -0.6% for LE, +2.5% for HALE)
- **Conclusion**: Maternal Mortality was capturing spurious associations related to general healthcare quality; removal improves model interpretability

**8. Removing Childhood Indicator (Under-Five Mortality)** ✅ **COMPLETE**
- **Major Finding**: Childhood indicator had very low importance (0.0558 in LE model, not in top 10 for HALE) and limited temporal coverage. The IHME alternative (All-Cause Deaths Under 5, per 100,000 population) is confounded with age structure and fertility rates, making it methodologically inappropriate.
- **Impact**: 
  - Homicide gained substantial importance in both models (+70% for LE, +29% for HALE)
  - Neoplasms strengthened in HALE model (+19%)
  - Cardiovascular decreased in HALE model (-24%)
  - Some redistribution of importance to other indicators
- **Model Performance**: Minimal impact (R² +0.8% for LE, -0.3% for HALE)
- **Conclusion**: Removing Childhood simplifies the model without sacrificing meaningful predictive power. The very low importance and lack of a suitable alternative (IHME version is confounded) justify removal.

**Overall Validation Results**:
- ✅ All indicator replacements completed and validated
- ✅ Model performance generally improved with IHME data
- ✅ Definitional differences between WHO and IHME indicators documented
- ✅ Counterintuitive associations identified and addressed (Maternal Mortality removed)
- ✅ Final model uses consistent IHME data sources with better temporal coverage
- ✅ Comprehensive documentation in `validation.md` with detailed comparisons for each experiment



**Step 9.2: Select Time Points for Analysis** ⚠️ **TO DO**

**Recommended Time Points**:
- **1990**: Early time point, before many health interventions and policy changes
- **2000**: Baseline for many health indicators, start of WHO data for many indicators
- **2010**: Mid-point, allows assessment of changes over a decade
- **2019**: Pre-COVID baseline, most recent year before pandemic distortions
- **Optional: 2015**: Additional mid-point if needed for finer temporal resolution

**Considerations**:
- Use the same time point across all indicators (complete-case analysis per time point)
- Some indicators may not have data for all time points (document missing data)
- Focus on time points where most indicators have data available
- Exclude 2020+ to avoid COVID-19 pandemic distortions

**Step 9.3: Prepare Data for Each Time Point** ⚠️ **TO DO**

**For each selected time point**:
- Load all predictor indicators for that specific year (not most recent year)
- Filter to OECD countries with complete data for that year
- Compute gender gaps (Mid and Gap columns) for each indicator at that time point
- Prepare target variables (HALE gap and Life Expectancy gap) for that time point
- Create separate datasets for each time point, saved to HDF5 files (e.g., `hale_analysis_data_1990.h5`, `hale_analysis_data_2000.h5`, etc.)

**Implementation**:
- Modify `load_and_inventory()` function to accept a specific year parameter
- Modify `summarize_gap()` function to select a specific year instead of most recent year
- Create a loop or function to process all time points systematically
- Document which countries are included at each time point (coverage may vary)

**Step 9.4: Fit Models for Each Time Point** ✅ **COMPLETED**

**Completed Work**:
- Modified `eda.md`, `model_le.md`, and `model_hale.md` to accept a `cutoff_year` parameter
- Updated all output filenames (HTML tables, figures, HDF5 data files) to include the cutoff year
- Fit Elastic Net models for multiple cutoff years: 2019, 2015, 2010, 2005, 2000
- Used same cross-validation approach (5-fold CV) for model selection at each time point
- Extracted coefficients and calculated feature importance for each cutoff year
- Calculated model performance metrics (R², MAE) for each cutoff year
- Generated output files with cutoff year in filenames to enable temporal comparison

**Implementation Details**:
- Each analysis uses the most recent year of data available for each country up to the cutoff year
- Model results stored in separate output files for each cutoff year (e.g., `model_comparison_le_2019.html`, `indicator_importance_hale_2015.html`)
- All analyses exclude 2020+ data to avoid COVID-19 pandemic distortions
- Results enable comparison of model performance, feature importance, and counterfactual effects across time periods

**Step 9.5: Analyze Temporal Changes** ✅ **COMPLETED**

**Completed Work**:
- Created `temporal.md` document to summarize and compare results across different cutoff years
- Documented results chronologically (2000 → 2005 → 2010 → 2015 → 2019) to show evolution over time
- Reframed analysis to focus on understanding how health patterns have changed over time, rather than choosing a cutoff year

**Key Analyses Completed**:

1. **Feature Importance Trends**:
   - Documented how indicator importance has changed from 2000 to 2019
   - Identified major shifts: rise of Neoplasms (280% increase in HALE model), decline of Cardiovascular (64% decrease in HALE model)
   - Compared HALE vs. Life Expectancy importance trends across time periods
   - Identified which indicators have gained or lost importance over two decades

2. **Model Performance Trends**:
   - Compared R² and MAE metrics across cutoff years (2000, 2005, 2010, 2015, 2019)
   - Documented how model performance varies with different time periods
   - Assessed whether models explain more or less variance over time

3. **Counterfactual Analysis Trends**:
   - Documented how counterfactual effects have evolved over time
   - Identified shifting intervention priorities (e.g., Suicide prevention becoming top priority)
   - Tracked net gap reduction potential over time (increased from -0.858 to -1.298 years for LE, -0.986 to -1.755 years for HALE)

4. **Temporal Evolution Interpretation**:
   - Interpreted changes as real health pattern evolution, not just modeling artifacts
   - Identified what changes indicate about health evolution (e.g., cancer becoming dominant, cardiovascular improvements)
   - Provided policy implications based on temporal trends

**Documentation**:
- Results organized chronologically with "Changes from Previous Period" sections
- Comprehensive summary section interpreting temporal evolution of health patterns
- Focus on understanding how health indicators and their relationships to gender gaps have evolved over two decades

**Step 9.6: Document Temporal Findings** ⚠️ **TO DO**

**Documentation**:
- Create summary tables showing:
  - Gap values and trends by country and time point
  - Predictor values and trends by indicator and time point
  - Model coefficients and importance rankings by time point
  - Model performance metrics by time point
- Create visualizations:
  - Time series plots for gaps, predictors, and coefficients
  - Heatmaps showing importance rankings over time
  - Country-level gap trends
- Update JupyterBook site with temporal analysis results
- Compare findings with existing literature on gender gap trends

**Implementation Notes**:
- Create new notebook `temporal_analysis.md` for this phase
- Reuse functions from `eda.md` and `model_le.md`/`model_hale.md` where possible
- Export temporal analysis results to HTML tables and figures
- Include temporal analysis section in `hale_gaps.md` JupyterBook site

**Expected Insights**:
- Understanding of how the gender gap has evolved over time
- Identification of which factors have driven changes in the gap
- Assessment of whether policy interventions have been effective
- Comparison of HALE vs. Life Expectancy gap trends

**Step 9.7: Create Trends Visualization Notebook** ✅ **COMPLETED**

**Purpose**:
Create a dedicated notebook that visualizes trends over time using all available temporal data. This notebook will provide comprehensive time series visualizations of how health indicators, gender gaps, and model results have evolved across the analysis period.

**Notebook Structure**:
- ✅ Create new notebook `time_series.md` 
- ✅ Load temporal data directly from source data files
- ✅ Create comprehensive time series plots for all indicators and outcomes that are used in the model (mid and gap)

**Visualizations to Include**:

1. **Target Variable Trends**:
   - ✅ Time series plots of HALE gap and Life Expectancy gap over time (by country and OECD average)
   - ✅ Time series plots of HALE and Life Expectancy values over time (by country and OECD average)
   - ✅ Multi-panel plots showing gap trends for selected countries
   - ✅ Tables showing value and gap changes from 2000 to 2019 for each country
   - ✅ Summary tables with superlatives (highest/lowest values and slopes)

2. **Indicator Trends**:
   - ✅ Time series plots for each indicator showing:
     - Overall rates (Mid values) over time
     - Gender gaps (Gap values) over time
   - ✅ Summary tables with superlatives for each indicator (highest/lowest means and slopes)

**Deliverables**:
- ✅ Notebook: `md/time_series.md` with all visualizations and analysis
- ✅ Report: `jb/time_series_report.md` explaining methodology and summarizing results
- ✅ All figures saved to `jb/figs/`
- ✅ All tables saved to `jb/tables/`
- ✅ Report integrated into JupyterBook site (`myst.yml` and `index.md` updated)

### Phase 10: Panel Data Modeling (In Progress)

**Overview:**
Extend the analysis to leverage both temporal variation (2000-2019) and cross-country variation simultaneously. This panel data approach will provide more statistical power and allow us to model how relationships between indicators and gender gaps evolve over time, while accounting for country-specific characteristics.

**Context:**
We now have:
- A fully validated cross-sectional model for 2019 (and earlier cutoff years)
- Temporal analysis notebooks (Phase 9)
- Indicators harmonized onto IHME definitions
- A clear understanding of how indicator importance changes over time

**Primary Goal:**
Determine whether the same predictors that matter cross-sectionally also matter within countries over time. Specifically:
- Does alcohol matter because countries differ from each other, or because countries that reduce alcohol mortality see their gaps narrow?
- Do predictors (e.g., cardiovascular mortality) predict gaps within a country over time?

**Recommended Approach:**
Implement a **Bayesian hierarchical model with country-level random intercepts and shared slopes** as the primary next step. This approach:
- Uses both within-country and between-country variation (unlike fixed effects)
- Controls for time-invariant country-level factors (culture, baseline health systems, risk environments)
- Retains interpretability of coefficients (β has clear meaning across countries)
- Preserves ability to run counterfactuals in a fully Bayesian framework
- Handles unbalanced data naturally
- Does not require large within-country variation (unlike fixed-effects models)
- Avoids overcomplication of random slopes (which require more data per country than available)

**Step 10.1: Data Preparation for Panel Analysis**

**Data Structure:**
- Transform from country-level (one row per country) to panel structure (one row per country-year)
- Include all years 2000-2019 for each country
- Maintain predictor variables (Mid and Gap columns) for each country-year
- Maintain target variables (HALE gap and Life Expectancy gap) for each country-year
- **Note**: There is no missing data in the panel dataset

**Implementation:**
- Make a version of the `summarize_gap()` function that returns all years (not just most recent)
- Create panel dataset with MultiIndex (Country, Year) or long format (Country, Year as columns)
- Columns needed:
  - `HALE_gap` (or `LE_gap`) - target variable
  - All predictors (Mid + Gap columns)
  - `Country` - country code
  - `Year` - year (2000-2019)
- Save panel dataset to HDF5 file for modeling notebooks

**Standardization Strategy:**

**1. Predictors (Standardize - Full Z-Scores):**
- For each predictor `X_j` (both Mid and Gap versions):
  - Compute mean `X̄_j` and standard deviation `s_j` across **all country-year observations** in the panel (OECD, 2000-2019)
  - Transform to z-scores: `X*_{ijt} = (X_{ijt} - X̄_j) / s_j`
- **Important**: 
  - Do **not** standardize within country or within year
  - Use a **single global transformation** for the entire panel (2000-2019)
  - This preserves genuine level differences between countries and across time, which are part of the signal
- **Benefits**:
  - Priors are coherent: `β_j ~ N(0, 1)` means "1-SD change in predictor → ~1 year change in gap"
  - Coefficients are directly comparable across predictors
  - Indicator-level importance is straightforward: `|β_j|` in standardized space
  - Consistent with cross-sectional Elastic Net approach (time-extended version)

**2. Targets (Center Only, Do Not Scale):**
- For HALE_gap and LE_gap separately:
  - Compute global mean across all country-years: `ȳ = mean(y_{it})`
  - Center (but do not scale): `y*_{it} = y_{it} - ȳ`
  - Keep units in **years** (not standardized)
- **Why center but not scale**:
  - **Interpretability**: Effects remain in "years" (e.g., "1-SD reduction in alcohol → 0.6-year reduction in gap")
  - **Numerical behavior**: Gap scale is modest (0-8 years), no scaling needed for numerical stability
  - **Priors**: With standardized predictors and unscaled (centered) target:
    - `β_j ~ N(0, 1)` is sensible: most effects within ±2 years per 1-SD change
    - `σ ~ HalfNormal(1)` reflects ~1 year unexplained variation
  - If scaled, would need to rescale priors to SD-of-gap scale (less transparent)
- **Predictions**: When converting back to original scale, add `ȳ` back: `ŷ_{it} = ŷ*_{it} + ȳ`


**Step 10.2: Recommended Model Specification (First Implementation)**

**Model Structure:**
Bayesian hierarchical model with country-level random intercepts and shared slopes (no random slopes initially).

**Notation:**
- `y_{it}` = HALE gap (or LE gap) for country i in year t (centered: `y*_{it} = y_{it} - ȳ`)
- `X*_{it}` = vector of standardized predictors (Mid + Gap columns, z-scores across full panel)
- `α_i` = country-specific random intercept
- `β` = shared slope coefficients (same across all countries)
- `t` ∈ 2000–2019

**Model:**
```
y*_{it} ~ N(α_i + X*_{it}β, σ)
α_i ~ N(0, σ_α)
```

**Priors:**
- `β ~ N(0, 1)` - Regularizing prior on coefficients (1-SD change in predictor → ~1 year change in gap)
- `α_i ~ N(0, σ_α)` - Country intercepts centered at zero (since target is centered)
- `σ_α ~ HalfNormal(1)` - Prior on between-country intercept variation
- `σ ~ HalfNormal(1)` - Prior on residual standard deviation (~1 year unexplained variation)

**Why This Model:**
1. **Answers the primary scientific question**: Does alcohol matter because countries differ from each other, or because countries that reduce alcohol mortality see their gaps narrow? This model can answer both.
2. **Seamlessly extends the cross-sectional Elastic Net model**: Provides posterior distributions for β instead of penalized point estimates, with natural interpretation as global "effect size" averaged over space and time, and shrinkage through hierarchical priors (like Bayesian ridge regression).
3. **Preserves counterfactual framework**: Produces posterior predictive distributions for country-level counterfactuals, changes through time, and uncertainty bands for temporal counterfactuals.
4. **Computationally feasible**: With ≈ 38 countries × 20 years ≈ 760 observations, a hierarchical linear model with 12–18 predictors runs well in PyMC. No need for variational inference yet, and parallel chains are reasonable on commodity hardware.

**Why Not Fixed Effects:**
- Fixed-effects models eliminate all between-country variation, which we know is large and informative
- Uses only within-country variation (changes over time), discarding valuable cross-country information

**Why Not Random Slopes (Initially):**
- Random slopes require much more data per country than available (≈20 years × OECD ≈ 38 countries)
- Estimating slope variance would be unstable and will obscure interpretation
- Can be added later if needed (see Step 10.4)

**Step 10.3: Implementation in PyMC**

**Software:**
- Use `PyMC` (Python) for Bayesian inference
- Leverage existing PyMC experience from cross-sectional analysis

**Implementation Steps:**
1. Load panel dataset (country-year structure)
2. **Standardize predictors**:
   - For each predictor (Mid and Gap columns):
     - Compute mean and SD across all country-year observations
     - Transform to z-scores: `X*_{ijt} = (X_{ijt} - X̄_j) / s_j`
     - Store transformation parameters (mean, SD) for later use in counterfactuals
   - Use single global transformation for entire panel (2000-2019)
3. **Center targets**:
   - For HALE_gap (or LE_gap):
     - Compute global mean: `ȳ = mean(y_{it})` across all country-years
     - Center: `y*_{it} = y_{it} - ȳ`
     - Store `ȳ` for converting predictions back to original scale
4. Set up PyMC model with:
   - Country index for random intercepts
   - Shared slope coefficients for all standardized predictors
   - Priors as specified above (β ~ N(0, 1), α_i ~ N(0, σ_α), etc.)
5. Run MCMC sampling (4 chains, appropriate number of draws)
6. Check convergence diagnostics (R-hat, effective sample size)
7. Extract posterior distributions for all parameters
8. **Convert predictions back to original scale**:
   - For predictions: `ŷ_{it} = ŷ*_{it} + ȳ`
   - For counterfactuals: apply inverse standardization to predictors, then add `ȳ` to predictions

**Computational Considerations:**
- With ≈ 760 observations and 12–18 predictors, model should run efficiently
- Use parallel chains for faster sampling
- Monitor sampling efficiency and adjust if needed
- No missing data handling needed (complete panel)

**Step 10.4: Predictor selection** ✅ **COMPLETED**

After implementing the basic random-intercept model, consider these extensions:

**(A) Predictor Selection Based on Correlations:** ✅ **COMPLETED**
- **Initial Analysis**: ✅ COMPLETED - Removing all Mid predictors dramatically improved model fit (ΔWAIC ≈ -234 to -280)
- **Baseline Model**: Model uses only Gap predictors (10 predictors), which eliminated multicollinearity issues from high correlations (r ≈ -0.9 to -1.0) between Mid and Gap predictors for indicators like Homicide, Alcohol, Liver Disease, Road Traffic, and Suicide
- **Selective Re-introduction Experiments**: ✅ **COMPLETED** - Systematically tested four Mid predictors with low/negative correlations:
  1. **Mid_Cardiovascular** (r = -0.804): Tested - worsened fit (ΔWAIC +51.3 HALE, +62.5 LE)
  2. **Mid_Diabetes** (r = -0.325): Tested - worsened fit (ΔWAIC +3.1 HALE, +2.18 LE)
  3. **Mid_ChronicRespiratory** (r = -0.0787): Tested - worsened fit (ΔWAIC +20.8 HALE, +24.1 LE)
  4. **Mid_UnintentionalInjury** (r = 0.0346): Tested - worsened fit (ΔWAIC +79.3 HALE, +91.1 LE)
- **Final Conclusion**: ✅ **All experiments completed** - Baseline model with Gap predictors only is optimal. All four Mid predictors tested worsened model fit regardless of correlation strength. The competing risks interpretation for negative Gap coefficients (Cardiovascular, Diabetes) remains robust without Mid predictors.
- **Final Model Specification**: 10 Gap predictors only (no Mid predictors)
- **Documentation**: Complete results documented in `bayesian_model_report.md` with detailed analysis of all four experiments

- **Approach: Selective Re-introduction of Mid Predictors** ✅ **COMPLETED**
  - **Rationale**: Mid predictors with low or negative correlations to Gap predictors provide independent information about overall (midpoint) levels that varies between countries and over time, which the model currently doesn't see
  - **Strategy**: Add back Mid predictors selectively, starting with those that have the lowest correlations with their corresponding Gap predictors
  - **Correlation Data** (from `eda.md`, table: `rate_gap_correlation_2019.html`):
    - **High positive correlations** (r > 0.9): Homicide (0.999), Alcohol (0.982), RoadTraffic (0.971), DrugDisorder (0.957), LiverDisease (0.955), Suicide (0.9) - **DO NOT add back** (multicollinearity risk)
    - **Moderate positive**: Neoplasms (0.685) - **Consider later** if needed
    - **Low/zero correlation**: UnintentionalInjury (0.0346) - **Good candidate**
    - **Negative correlations**: ChronicRespiratory (-0.0787), Diabetes (-0.325), Cardiovascular (-0.804) - **Excellent candidates** (provide independent information)

- **Testing Order** (✅ **COMPLETED** - all four candidates tested):
  1. ✅ **Mid_Cardiovascular** (r = -0.804 with Gap_Cardiovascular) - **Result**: Worsened fit (ΔWAIC +51.3 HALE, +62.5 LE)
  2. ✅ **Mid_Diabetes** (r = -0.325 with Gap_Diabetes) - **Result**: Worsened fit (ΔWAIC +3.1 HALE, +2.18 LE)
  3. ✅ **Mid_ChronicRespiratory** (r = -0.0787 with Gap_ChronicRespiratory) - **Result**: Worsened fit (ΔWAIC +20.8 HALE, +24.1 LE)
  4. ✅ **Mid_UnintentionalInjury** (r = 0.0346 with Gap_UnintentionalInjury) - **Result**: Worsened fit (ΔWAIC +79.3 HALE, +91.1 LE)

- **Implementation Strategy** (✅ **COMPLETED** - Manual, Iterative Approach):
  - ✅ Baseline model established (Gap predictors only, WAIC = 75.7 HALE, -7.44 LE)
  - ✅ Each candidate tested individually (not cumulatively, since none improved fit)
  - ✅ Results evaluated after each experiment (WAIC/LOO comparison, coefficient stability, posterior correlations)
  - ✅ All experiments documented in `bayesian_model_report.md` with detailed analysis

- **Final Results**:
  - ✅ **All four Mid predictors worsened model fit** regardless of correlation strength
  - ✅ **Baseline model (Gap predictors only) confirmed as optimal**
  - ✅ **Competing risks interpretation remains robust** - negative coefficients for Gap_Cardiovascular and Gap_Diabetes are not artifacts requiring Mid predictors
  - ✅ **Final model specification**: 10 Gap predictors only (no Mid predictors)
  - ✅ **Documentation**: Complete results documented in `bayesian_model_report.md` with detailed analysis of all four experiments

**(B) Year Fixed Effects (Gaussian Random Walk) - ✅ COMPLETED:**
- Add `γ_t` to model: `y*_{it} = α_i + γ_t + X*_{it}β + ε_{it}`
- Controls for global temporal trends (e.g., global health improvements affecting all countries)
- **Implementation**: Use Gaussian Random Walk (GRW) for year effects:
  - `γ_1 ~ N(0, σ_γ₀)` (initial year effect)
  - `γ_t ~ N(γ_{t-1}, σ_γ)` for t > 1 (random walk)
  - Creates smooth temporal trends with only 2 parameters (vs. 20 for categorical year effects)
- **Rationale**: GRW balances flexibility (can capture non-linear trends) with parsimony (only 2 parameters) and smoothness (natural for gradual health improvements)
- **Results**: Year effects were tested but **do not improve model fit**:
  - HALE Gap: ΔWAIC = +97.7 (worse), ΔLOO = +97.1 (worse)
  - Life Expectancy Gap: ΔWAIC = +110.85 (worse), ΔLOO = +110.22 (worse)
  - Effective parameters increased by ~12-15 without improving predictive performance
- **Conclusion**: Model **without year effects is preferred** (better WAIC/LOO, simpler)
- **Conditional implementation**: Controlled by global variable `INCLUDE_YEAR_EFFECTS` (default: False)
- **Output filenames**: Include "yesgrw" or "nogrw" suffix along with "yesmid"/"nomid" suffix

**Model Version Output Files:**
- **Files with `_nomid` suffix (no additional suffix)**: Model with Gap predictors only, NO year effects
  - Example: `beta_coefficients_hale_nomid.html`, `model_comparison_metrics_nomid.html`
  - Configuration: `INCLUDE_MID_PREDICTORS = False`, `INCLUDE_YEAR_EFFECTS = False`
- **Files with `_nomid_yesgrw` suffix**: Model with Gap predictors only, WITH year effects (GRW)
  - Example: `beta_coefficients_hale_nomid_yesgrw.html`, `model_comparison_metrics_nomid_yesgrw.html`
  - Configuration: `INCLUDE_MID_PREDICTORS = False`, `INCLUDE_YEAR_EFFECTS = True`
- **Note**: Both versions exclude Turkey (controlled by `COUNTRIES_TO_EXCLUDE = ['TUR']`)
- **Comparison**: Compare WAIC/LOO between `_nomid` and `_nomid_yesgrw` files to assess whether year effects improve model fit




**Decision Framework:**
- Compare models using WAIC or LOO cross-validation
- Add extensions only if they meaningfully improve model fit or provide substantive insights
- Avoid overcomplicating the model without clear benefit


**Step 10.5: Importance Measures and Counterfactual Analysis**

**(A) Importance Measures on Original Scale:** ✅ **COMPLETED**
- **Current approach**: Using standardized coefficients (β in years per standard deviation)
  - Allows direct comparison across predictors
  - Interpretable as "1-SD change in predictor → β years change in gap"
  - But doesn't reflect the natural scale or typical variation of each predictor
- **Proposed addition**: Compute importance measure on original scale
  - **Importance measure** (|β_standardized| × SD_original) - **Matches Elastic Net approach**
    - Interpretation: Total contribution when predictor varies by 1 SD in its original units
    - Formula: importance = |β_standardized| × SD_original
    - Units: years (total effect size)
    - Useful for: Ranking predictors by their total contribution, accounting for both effect size and typical variation
    - Example: If Gap_Alcohol has β_standardized = 0.158 and SD_original = 2.5, then importance = 0.158 × 2.5 = 0.395 years
    - This matches what was used in the Elastic Net models: `importance = abs(coef) * std_original`
- **Implementation**: 
  - Extract SD values used for standardization from `data["meta"]["X_std"]` (stored in `prepare_panel_data`)
  - For each predictor, compute from posterior distributions:
    - importance = |β_standardized| × SD_original (mean, 94% HDI)
  - Create comparison table showing:
    - Predictor name
    - Standardized coefficient (mean, 94% HDI) - current
    - SD_original (for reference)
    - Importance measure (mean, 94% HDI) - sorted by importance (descending)
  - Save table to HTML for inclusion in report
- **Interpretation**: 
  - **Standardized coefficients**: Which predictors matter most when all are on the same scale? (current approach)
  - **Importance measure**: Which predictors contribute most given their typical variation (1 SD)? (matches Elastic Net, units: years)
- **Why this matters**: A predictor with a large standardized coefficient might have small importance if its SD is small, or vice versa. The importance measure accounts for both effect size and typical variation, providing a better ranking for policy interventions.

**(B) Counterfactual Analysis:** ⏳ **TO DO** (Next Step)
- Extend counterfactual analysis:
  - Predict effect of reducing alcohol mortality in a given country in a given year
  - Predict effect of long-term trends (e.g., gradual reduction over 10 years)
  - Provide uncertainty bands for temporal counterfactuals
- ⏳ Export counterfactual results: `counterfactuals_panel_usa_hale.html`



**Step 10.6: Comparison with Cross-Sectional Model**

**Key Comparisons:**
1. **Coefficient Estimates**: Compare posterior means of β to Elastic Net coefficients
   - Which predictors survive in a temporal context?
   - Do effect sizes shrink or expand?
   - Do importance patterns shift?

2. **Feature Importance**: Compare indicator importance rankings
   - Which indicators are more/less important in panel vs. cross-sectional model?
   - Does temporal variation change which factors matter most?

3. **Uncertainty Quantification**: Compare credible intervals (Bayesian) to confidence intervals (Elastic Net)
   - How does uncertainty change with more data?
   - Are relationships more or less certain in panel model?

4. **Model Performance**: Compare R², RMSE, cross-validation scores
   - Does panel model explain more variance?
   - How does predictive performance compare?

**Interpretation:**
- Discuss which predictors are robust across both modeling approaches
- Identify predictors that matter more in temporal vs. cross-sectional context
- Explain differences in importance patterns between models

**Step 10.6: Deliverables (Recommended Sequence)**

**Deliverable 1 (High Priority):**
- ✅ Implement Bayesian random-intercept model in PyMC
- ✅ Implemented for both HALE gap and Life Expectancy gap
- ✅ Created notebook: `md/bayesian_model.md`
- ✅ Used `prepare_panel_data()` function to standardize predictors and center targets
- ✅ Used `build_random_intercept_panel_model()` function with proper PyMC structure:
  - `pm.Data` objects for explicit dependency graph
  - `pm.Deterministic` for `mu` (linear predictor)
  - `nuts_sampler='nutpie'` for efficient MCMC sampling

**Deliverable 2:**
- ✅ Report posterior means and credible intervals for β (predictor coefficients)
- ✅ Report posterior for α (country-specific intercepts)
- ✅ Report posterior for σ_α (degree of between-country heterogeneity)
- ✅ Create visualizations of posterior distributions:
  - Forest plots for β coefficients (`posterior_forest_beta_hale.png`, `posterior_forest_beta_le.png`)
  - Forest plots for α intercepts (`posterior_forest_alpha_hale.png`, `posterior_forest_alpha_le.png`)
- ✅ Export results to HTML tables:
  - `tables/beta_coefficients_hale.html`, `tables/beta_coefficients_le.html`
  - `tables/alpha_coefficients_hale.html`, `tables/alpha_coefficients_le.html`
- ✅ Posterior predictive checks (PPCs):
  - Distribution comparison plots (overlay of observed vs posterior predictive)
  - Q-Q plots comparing observed vs posterior predictive quantiles
  - Test statistics comparison (mean, std, min, max) with p-values
  - Figures: `figs/ppc_hale.png`, `figs/ppc_le.png`, `figs/ppc_test_stats_hale.png`, `figs/ppc_test_stats_le.png`

**Deliverable 3:**
- ✅ Export Elastic Net coefficients from cross-sectional models:
  - Modified `model_hale.md` and `model_le.md` to save coefficients to CSV
  - Files: `data/elasticnet_coefficients_hale_2019.csv`, `data/elasticnet_coefficients_le_2019.csv`
- ✅ Compare coefficients to cross-sectional Elastic Net model:
  - Load Elastic Net coefficients in Bayesian model notebook
  - Create comparison visualizations showing posterior distributions vs. Elastic Net point estimates
  - Figures: `figs/bayesian_elasticnet_comparison_hale.png`, `figs/bayesian_elasticnet_comparison_le.png`
- ✅ Compute and analyze posterior correlations:
  - Top 10 correlations among β coefficients (predictor slopes)
  - Top 10 correlations among α coefficients (country intercepts)
  - Export to HTML: `tables/beta_correlations_top10_hale.html`, `tables/alpha_correlations_top10_hale.html`, etc.
- ✅ Document findings in report:
  - Which predictors survive in a temporal context
  - Whether effect sizes shrink or expand
  - Whether importance patterns shift
  - Interpretation of posterior correlations



**Deliverable 5:**
- ✅ Integrate panel model results into JupyterBook site
- ✅ Created comprehensive report: `jb/bayesian_model_report.md`
- ✅ Document model specification, priors, and interpretation
- ✅ Include comparison with cross-sectional model
- ✅ Include posterior correlation analysis and interpretation
- ✅ Updated JupyterBook configuration (`myst.yml`) and index (`index.md`) to include report
- ⏳ Include counterfactual analysis results (pending Deliverable 4)

**Future Work (After Initial Implementation):**
- ✅ Implemented same model for Life Expectancy gap
- ✅ Compute model fit metrics (WAIC, LOO-CV) for current full model:
  - WAIC and LOO-CV computation for both HALE and Life Expectancy models
  - Pointwise contribution plots
  - Identification of influential observations
  - Model comparison summary table
  - Figures: `figs/waic_loo_hale.png`, `figs/waic_loo_le.png`
  - Tables: `tables/influential_observations_hale.html`, `tables/influential_observations_le.html`, `tables/model_comparison_metrics.html`
  - Fixed log-likelihood computation for nutpie sampler
  - Created helper functions to reduce code duplication
- ⏳ Test simplified model by removing all Mid predictors:
  - Model 1: Include all Mid predictors (current model)
  - Model 2: Exclude all Mid predictors (keep only Gap predictors)
  - Compare fit metrics (WAIC, LOO-CV) to determine if simplification improves model
  - Update output filenames to include "yesmid" or "nomid" suffix for comparison
- ⏳ Test model extensions (year fixed effects, AR(1), random slopes)
- ✅ Posterior predictive checks (see Deliverable 2)
- ⏳ Counterfactual analysis with uncertainty quantification


## Neoplasms (Cancer) Drilldown Analysis

Neoplasms are the largest single driver of the gender gap in Life Expectancy and HALE. This analysis aims to "look under the hood" of the neoplasms category to identify which specific cancers and risk factors are responsible for this gap.

### Objective
Identify the specific types of cancer that contribute most to the male-female mortality difference and determine the extent to which these gaps are associated with behavioral, metabolic, or environmental risk factors.

### Data
- **Source**: IHME Global Burden of Disease (2023)
- **Scope**: United States (as a representative high-income country case study)
- **Variables**: Deaths and Death Rates (per 100,000) for ~30 specific cancer types, further disaggregated by:
    - **Behavioral risks** (e.g., smoking, diet, alcohol)
    - **Metabolic risks** (e.g., high BMI, high blood pressure)
    - **Environmental/occupational risks** (e.g., air pollution, workplace carcinogens)

### Analysis Steps
1. **Compute Gender Gaps by Cancer Type**:
   - Calculate the absolute difference in death rates: $Gap_{cancer} = Rate_{Male} - Rate_{Female}$
2. **Rank Contributors**:
   - Rank cancer types by their absolute contribution to the total neoplasm gap.
   - For example, how much of the total neoplasm gap is explained specifically by lung cancer?
3. **Risk Factor Attribution**:
   - For each cancer type, calculate the portion of the gap attributable to behavioral vs. metabolic vs. environmental risks.
   - This will help distinguish between gaps driven by lifestyle choices (behavioral) versus biological or environmental factors.
4. **Visualization**:
   - Create a stacked bar chart showing the total neoplasm gap, broken down by specific cancer types.
   - Create a second visualization showing the risk-factor breakdown for the top contributing cancers.




