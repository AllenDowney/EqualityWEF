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
- ⚠️ Prepare framework for temporal analysis (Phase 2, future work) - Not yet implemented
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

### Implementation Notes

- **Primary Tools**: scikit-learn for model fitting (`Ridge`, `Lasso`, `ElasticNet`, `GridSearchCV`, `StandardScaler`)
- **Secondary Tools**: statsmodels for diagnostics if needed
- **Data Sources**: 
  - **WHO Global Health Observatory (GHO) API**: Use `who_data.py` for downloading WHO indicators via the GHO OData API (https://www.who.int/data/gho/info/gho-odata-api). Provides access to HALE, Life Expectancy, and various cause-specific mortality indicators.
  - **IHME Global Burden of Disease**: Data downloaded from IHME GBD Compare (https://vizhub.healthdata.org/gbd-compare/) as CSV files with separate male and female files. IHME data is used for indicators where it provides better temporal coverage than WHO (e.g., cardiovascular disease, diabetes, chronic respiratory disease, neoplasms, drug use disorders, unintentional injuries). The `load_ihme_indicator()` function in `eda.md` converts IHME format to WHO-compatible format for consistency.
- **Country Codes**: Use `oecd_codes` from `utils.py` for OECD country filtering
- **Target Variable**: HALE gap = Female HALE - Male HALE (difference, not ratio)
- **Focus**: Direct causal indicators only (mortality/health indicators), not indirect indicators like GDP



## Results

### Model 1: Elastic Net Regression for Life Expectancy Gap (OECD Countries, Pre-COVID Data)

**Model Summary:**

This first iteration of the Life Expectancy gender gap model (in `model2.md`) uses Elastic Net regression with cross-validation on OECD countries using pre-COVID data (2000-2019). The model includes 12 health indicators with Mid and Gap columns as predictors (Mid + Gap format, not separate Male/Female columns), plus 1 female-only indicator for maternal mortality.

**Data:**
- **Countries**: OECD countries with complete data (complete-case analysis)
- **Time Period**: Most recent available year per country/indicator (2000-2019, excluding 2020+ to avoid COVID-19 distortions)
- **Target Variable**: Life Expectancy gap = Female LE - Male LE (in years) - **Note**: `model2.md` analyzes Life Expectancy gap, not HALE gap
- **Predictors**: Age-standardized mortality/health indicators in Mid + Gap format:
  - Cardiovascular disease death rates
  - Chronic respiratory disease death rates
  - Suicide rates
  - Alcohol-attributable death rates
  - Poisoning rates
  - Road traffic death rates
  - Homicide rates
  - Maternal mortality ratio (female-only)
  - Under-five mortality rate
  - Diabetes death rates
  - Drug use disorder death rates
  - Unintentional injuries death rates

**Model Performance:**
- Model selected via 5-fold cross-validation with GridSearchCV
- Elastic Net chosen as primary model (combines Ridge and Lasso regularization)
- Cross-validation R² and RMSE calculated for model comparison



