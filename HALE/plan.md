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

## Data Collection Summary

### Smoking/Tobacco Use Indicators (Downloaded)

Three smoking prevalence indicators have been downloaded from WHO GHO API:

1. **M_Est_smk_curr_std** - Age-standardized current tobacco smoking prevalence (%)
   - **Records**: 5,181 (includes projections)
   - **Years**: 2000-2030 (observed: 2000, 2005, 2007, 2010, 2015, 2018, 2020, 2021, 2022; projected: 2025, 2030)
   - **Countries**: 172
   - **Sex categories**: Both sexes, Female, Male
   - **File**: `data/who_smoking_data.csv`
   - **Status**: ✅ Recommended - age-standardized, good temporal coverage
   - **Note**: Years 2025 and 2030 are projections (marked in Comments field). Filter these out for analysis of observed data only.

2. **M_Est_cig_curr_std** - Age-standardized current cigarette smoking prevalence (%)
   - **Records**: 4,950 (likely includes projections)
   - **Years**: 2000-2030 (includes projected years 2025, 2030)
   - **Countries**: 165
   - **Sex categories**: Both sexes, Female, Male
   - **File**: `data/who_smoking_cigarette_std.csv`
   - **Status**: ✅ Good - cigarette-specific, age-standardized
   - **Note**: Check Comments field to identify projected vs. observed data

3. **Adult_curr_tob_smoking** - Current tobacco smoking among adults (%)
   - **Records**: 570
   - **Years**: 2001-2022
   - **Countries**: 190 (most countries)
   - **Sex categories**: Both sexes, Female, Male
   - **File**: `data/who_smoking_adult.csv`
   - **Status**: ✅ Good country coverage but fewer records and shorter time span

**Recommendation**: Use `M_Est_smk_curr_std` as the primary smoking predictor - it has the best combination of temporal coverage, age-standardization, and sufficient country coverage.

### Suicide Rate Indicators (Identified)

Five suicide-related indicators have been identified from WHO GHO API:

1. **MH_12** - Age-standardized suicide rates (per 100,000 population)
   - **Records**: 12,936
   - **Years**: 2000-2021
   - **Countries**: 196
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ✅ Recommended - age-standardized, excellent country coverage, good temporal coverage
   - **Note**: Age-standardized rates are preferred for HALE analysis since HALE is also age-standardized

2. **SDGSUICIDE** - Crude suicide rates (per 100,000 population)
   - **Records**: 19,041
   - **Years**: 2000-2021
   - **Countries**: 196
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ✅ Good - crude rates, excellent country coverage
   - **Note**: Crude rates may be less comparable across countries with different age structures

3. **SDG_SH_STA_SCIDEN** - Number of suicide deaths
   - **Status**: ⚠️ Less useful - absolute numbers rather than rates

4. **PRISON_D3_DEATHS_SUICIDE_MRATE** - In-prison suicide mortality rate
   - **Status**: ⚠️ Not relevant - prison-specific, not general population

5. **PRISON_B16_SUICIDERISK** - In-prison standardized protocol for suicide
   - **Status**: ⚠️ Not relevant - protocol indicator, not a rate

**Recommendation**: Use `MH_12` as the primary suicide rate predictor - it has age-standardized rates (matching HALE methodology), excellent country coverage (196 countries), gender breakdowns, and good temporal coverage (2000-2021).

### Alcohol-Attributable Death Rate Indicators (Identified)

Multiple alcohol-related death rate indicators have been identified from WHO GHO API:

1. **SA_0000001832** - Alcohol-attributable all-cause deaths per 100,000, age standardized
   - **Records**: 540
   - **Years**: 2019
   - **Countries**: 180
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ✅ Recommended - age-standardized, good country coverage, most recent data available
   - **Note**: Age-standardized rates match HALE methodology. This indicator captures all alcohol-attributable deaths (not just alcohol use disorders), providing a broader measure of alcohol's impact on mortality. Only has data for 2019, which limits temporal analysis but provides a good snapshot for cross-country comparison.

2. **SA_0000001437** - Age-standardized death rates, alcohol use disorders, per 100,000
   - **Records**: 714
   - **Years**: 2002, 2004 (only 2 years)
   - **Countries**: 186
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ⚠️ Limited temporal coverage - only 2 years of data, older years (2002, 2004)
   - **Note**: More specific than SA_0000001832 (focuses on alcohol use disorders rather than all alcohol-attributable deaths), but limited temporal coverage makes it less useful for analysis.

3. **SA_0000001833** - Alcohol-attributable DALYs per 100,000 people (age standardized)
   - **Years**: 2019
   - **Countries**: 182
   - **Records**: 1,092
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ✅ Good - DALYs (Disability-Adjusted Life Years) provide a measure of both mortality and morbidity, but death rates are more directly comparable to HALE

4. **SA_0000001457_AA** - Liver cirrhosis, alcohol-attributable, age-standardized death rates
   - **Years**: 2019
   - **Countries**: 180
   - **Records**: 1,080
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ✅ Good - specific cause of death, but narrower scope than all-cause alcohol-attributable deaths

**Recommendation**: Use `SA_0000001832` as the primary alcohol-attributable death rate predictor - it has age-standardized rates (matching HALE methodology), good country coverage (180 countries), gender breakdowns, and captures all alcohol-attributable deaths (providing a comprehensive measure of alcohol's impact on mortality). The limitation is that it only has data for 2019, but this provides a good cross-sectional snapshot for the analysis.

### Unintentional Poisoning Mortality Rate Indicators (Identified)

Multiple unintentional poisoning-related indicators have been identified from WHO GHO API:

1. **SDGPOISON** - Mortality rate attributed to unintentional poisoning (per 100,000 population)
   - **Records**: 12,936
   - **Years**: 2000-2021 (22 years)
   - **Countries**: 196
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ✅ Recommended - excellent temporal coverage, excellent country coverage, gender breakdowns, includes confidence intervals
   - **Note**: This is a crude rate (not explicitly age-standardized), but has excellent temporal and country coverage. Unintentional poisoning includes accidental poisonings from chemicals, drugs, and other substances, which can contribute to the gender gap in mortality. Men often have higher rates of accidental deaths, including poisonings.

2. **SA_0000001450** - Age-standardized death rates, poisoning, per 100,000
   - **Records**: 731
   - **Years**: 2002, 2004 (only 2 years)
   - **Countries**: 185
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ⚠️ Limited temporal coverage - only 2 years of data, older years (2002, 2004)
   - **Note**: Age-standardized rates are preferred for HALE analysis, but limited temporal coverage makes it less useful than SDGPOISON.

3. **SA_0000001458** - Age-standardized death rates (15+ years), poisoning, per 100,000
   - **Years**: 2002, 2004 (only 2 years)
   - **Status**: ⚠️ Limited temporal coverage - similar to SA_0000001450 but for ages 15+

4. **SA_0000001837** - Alcohol poisoning deaths, per 100,000 population
   - **Status**: ⚠️ Narrow scope - only alcohol-related poisonings, not all unintentional poisonings

**Recommendation**: Use `SDGPOISON` as the primary unintentional poisoning mortality rate predictor - it has excellent temporal coverage (2000-2021), excellent country coverage (196 countries), gender breakdowns, and includes confidence intervals. While it's not explicitly age-standardized, the comprehensive temporal and country coverage make it more valuable for analysis than the age-standardized indicators with only 2 years of data. Unintentional poisoning is relevant to the gender gap as men often have higher rates of accidental deaths.

### Road Traffic Crash Death Rate Indicators (Identified)

Multiple road traffic-related death rate indicators have been identified from WHO GHO API:

1. **SA_0000001459** - Road traffic crash deaths, age-standardized death rates (15+), per 100,000 population
   - **Records**: 1,080
   - **Years**: 2019
   - **Countries**: 180
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ✅ Recommended - age-standardized, good country coverage, gender breakdowns, recent data (2019)
   - **Note**: Age-standardized rates for ages 15+ match HALE methodology (HALE is also age-standardized). Road traffic deaths are a major contributor to the gender gap in mortality, as men typically have much higher rates due to higher exposure to driving (including occupational exposure), occupational hazards, and potentially risk-taking behaviors. The limitation is that it only has data for 2019, but this provides a good cross-sectional snapshot for the analysis.

2. **RS_198** - Estimated road traffic death rate (per 100,000 population)
   - **Years**: 2021 (only 1 year)
   - **Countries**: 204
   - **Sex categories**: None (no gender breakdown)
   - **Status**: ⚠️ Not suitable - no gender breakdown available

3. **SA_0000001452** - Age-standardized death rates, road traffic accidents, per 100,000
   - **Years**: 2002, 2004 (only 2 years)
   - **Countries**: 192
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ⚠️ Limited temporal coverage - only 2 years of older data (2002, 2004)

4. **SA_0000001459_AA** - Road traffic crash deaths, alcohol-attributable, age-standardized death rates
   - **Years**: 2019
   - **Countries**: 180
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ⚠️ Narrow scope - only alcohol-attributable road traffic deaths, not all road traffic deaths

**Recommendation**: Use `SA_0000001459` as the primary road traffic crash death rate predictor - it has age-standardized rates (matching HALE methodology), good country coverage (180 countries), gender breakdowns, and captures all road traffic crash deaths (not just alcohol-attributable). The limitation is that it only has data for 2019, but this provides a good cross-sectional snapshot for the analysis. Road traffic deaths are highly relevant to the gender gap as men typically have 2-4 times higher rates than women in most countries.

### Maternal Mortality Ratio Indicators (Identified)

Multiple maternal mortality indicators have been identified from WHO GHO API:

1. **MDG_0000000026** - Maternal mortality ratio (per 100,000 live births)
   - **Records**: 7,878 (full dataset), 4,848 (2000-2023)
   - **Years**: 1985-2023 (excellent temporal coverage)
   - **Countries**: 202
   - **Sex categories**: N/A (inherently female-specific)
   - **Status**: ✅ Recommended - excellent temporal coverage, excellent country coverage, most comprehensive dataset
   - **Note**: Maternal mortality is inherently female-specific (deaths during pregnancy, childbirth, or within 42 days of termination of pregnancy). This indicator is critical for understanding cases where the HALE gender gap is small due to high female mortality, especially in lower-income countries. High maternal mortality can significantly reduce female life expectancy, explaining why some countries have smaller gender gaps.

2. **MDG_0000000032** - Maternal mortality ratio (per 100,000 live births) - Country reported estimates
   - **Years**: 1987, 2000, 2002-2009 (limited temporal coverage)
   - **Countries**: 169
   - **Status**: ⚠️ Limited temporal coverage - only 10 years of data, older years, fewer countries than MDG_0000000026

3. **MORT_MATERNALNUM** - Number of maternal deaths
   - **Status**: ⚠️ Less useful - absolute numbers rather than rates (rates are more comparable across countries)

**Recommendation**: Use `MDG_0000000026` as the primary maternal mortality ratio predictor - it has excellent temporal coverage (1985-2023), excellent country coverage (202 countries), and is the most comprehensive dataset available. Maternal mortality is a critical factor for understanding female mortality patterns, especially in lower-income countries where high maternal mortality can significantly reduce the HALE gender gap by lowering female life expectancy.

### Homicide Rate Indicators (Identified)

Two homicide-related indicators have been identified from WHO GHO API:

1. **VIOLENCE_HOMICIDERATE** - Estimates of rates of homicides per 100,000 population
   - **Records**: 12,936
   - **Years**: 2000-2021 (excellent temporal coverage)
   - **Countries**: 196
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ✅ Implemented - excellent temporal coverage, excellent country coverage, gender breakdowns, includes confidence intervals
   - **Note**: This is a crude rate (not explicitly age-standardized), but has excellent temporal and country coverage. Homicide rates are typically much higher in men than women across most countries, making it a major contributor to the gender gap in mortality. Homicide reflects violence, conflict, and social factors that differentially affect men and women.

2. **VIOLENCE_HOMICIDENUM** - Estimates of number of homicides
   - **Years**: 2000-2019 (slightly less recent than rate indicator)
   - **Countries**: 194
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ⚠️ Less useful - absolute numbers rather than rates (rates are more comparable across countries), and has less recent data (up to 2019 vs 2021)

**Recommendation**: Use `VIOLENCE_HOMICIDERATE` as the primary homicide rate predictor - it has excellent temporal coverage (2000-2021), excellent country coverage (196 countries), gender breakdowns, and includes confidence intervals. ✅ **Implemented** - Data download functionality added to `who_data.py`. While it's not explicitly age-standardized, the comprehensive temporal and country coverage make it very valuable for analysis. Homicide is highly relevant to the gender gap as men typically have much higher rates than women in most countries, making it a major contributor to the gender gap in mortality.

### Intimate Partner Violence (IPV) Indicators (Identified)

Multiple intimate partner violence indicators have been identified from WHO GHO API. Note: IPV is a **prevalence indicator** (percentage of women experiencing violence), not a direct death rate. It affects women's health and mortality indirectly through mental health, injuries, and other health consequences.

1. **SDGIPV** - Proportion of ever-partnered women and girls aged 15-49 years subjected to physical and/or sexual violence by a current or former intimate partner in the previous 12 months
   - **Records**: 577
   - **Years**: 2000-2017
   - **Countries**: 126
   - **Sex categories**: Female (inherently female-specific)
   - **Status**: ✅ Implemented - good temporal coverage, good country coverage, matches SDG indicator 5.2.1
   - **Note**: This is a prevalence indicator (percentage), not a death rate. IPV affects women's health indirectly through mental health impacts, injuries, and other health consequences. It may contribute to the gender gap in HALE through its effects on women's physical and mental health, though the relationship is complex and indirect.

2. **SDGIPV12M** - Proportion of ever-partnered women and girls aged 15–49 years subjected to physical and/or sexual violence by a current or former intimate partner in the previous 12 months
   - **Years**: 2018 (only 1 year)
   - **Countries**: 163
   - **Status**: ⚠️ Limited temporal coverage - only 2018 data, but good country coverage

3. **SDGIPVLT** - Proportion of ever-partnered women and girls aged 15–49 years subjected to physical and/or sexual violence by a current or former intimate partner in their lifetime
   - **Years**: 2018 (only 1 year)
   - **Countries**: 158
   - **Status**: ⚠️ Limited temporal coverage - only 2018 data, lifetime prevalence (broader than 12-month)

4. **RHR_IPV** - Intimate partner violence prevalence among ever partnered women (%)
   - **Years**: 2010 (only 1 year)
   - **Countries**: 29
   - **Status**: ⚠️ Very limited coverage - only 2010, only 29 countries

5. **SA_0000001455** - Age-standardized death rates, violence, per 100,000
   - **Years**: 2002, 2004 (only 2 years)
   - **Countries**: 192
   - **Sex categories**: Both sexes, Female, Male
   - **Status**: ⚠️ Limited temporal coverage - only 2 years, but age-standardized and has gender breakdowns. This captures all violence-related deaths (not just IPV), which may include homicide and other forms of violence.

**Recommendation**: Use `SDGIPV` as the primary intimate partner violence indicator - it has the best temporal coverage (2000-2017) and good country coverage (126 countries). ✅ **Implemented** - Data download functionality added to `who_data.py`. However, note that IPV is a prevalence indicator affecting women's health indirectly, not a direct cause of death. It may be less directly relevant to HALE gender gap analysis than direct mortality indicators, but could be useful for understanding broader health impacts on women. Consider whether the indirect relationship to mortality makes it suitable for the regression analysis, or if it should be analyzed separately.

### Infant and Child Mortality Indicators (Explored)

Multiple indicators related to infant, neonatal, and under-five mortality have been identified from WHO GHO API. Note: These indicators measure mortality in early life (birth to age 5), which may be less directly relevant to HALE gender gap analysis since HALE focuses on adult health outcomes. However, early-life mortality patterns can reflect underlying health disparities and may be relevant for understanding population-level gender differences.

#### Infant Mortality Indicators (with gender breakdowns):

1. **imr** - Infant mortality rate (deaths per 1000 live births)
   - **Years**: 1932-2023 (excellent temporal coverage)
   - **Countries**: 249
   - **Sex categories**: Both sexes, Female, Male
   - **Total records**: 43,513
   - **Status**: ✅ Excellent coverage - has gender breakdowns, very long temporal coverage, comprehensive country coverage

2. **MDG_0000000001** - Infant mortality rate (probability of dying between birth and age 1 per 1000 live births)
   - **Years**: 1932-2023 (excellent temporal coverage)
   - **Countries**: 249
   - **Sex categories**: Both sexes, Female, Male
   - **Total records**: 43,513
   - **Status**: ✅ Excellent coverage - similar to `imr`, has gender breakdowns, very long temporal coverage

3. **CM_02** - Number of infant deaths
   - **Years**: 1951-2023
   - **Countries**: 249
   - **Sex categories**: Both sexes, Female, Male
   - **Total records**: 42,716
   - **Status**: ⚠️ Less useful - absolute numbers rather than rates (rates are more comparable across countries), and has less recent historical data (starts 1951 vs 1932)

#### Under-Five Mortality Indicators (with gender breakdowns):

1. **u5mr** - Under-five mortality rate (deaths per 1000 live births)
   - **Years**: 1932-2023 (excellent temporal coverage)
   - **Countries**: 249
   - **Sex categories**: Both sexes, Female, Male
   - **Total records**: 63,070
   - **Status**: ✅ Excellent coverage - has gender breakdowns, very long temporal coverage, comprehensive country coverage

2. **MDG_0000000007** - Under-five mortality rate (probability of dying by age 5 per 1000 live births)
   - **Years**: 1932-2023 (excellent temporal coverage)
   - **Countries**: 249
   - **Sex categories**: Both sexes, Female, Male
   - **Total records**: 63,070 (30,648 with sex dimension when filtered)
   - **Status**: ✅ **Implemented** - Recommended and data download functionality added to `who_data.py`. Excellent coverage with clean gender breakdowns (5,976 Male, 5,976 Female records). Much better data quality than `u5mr` when filtered for sex dimension.

**Recommendation**: 

**For HALE gender gap analysis**: These indicators **SHOULD be considered** for inclusion in the regression model because:
1. **HALE is calculated from birth** - HALE (Healthy Life Expectancy) measures expected years of healthy life at birth, so it includes all mortality from birth to death. If infant/child mortality differs by gender, it directly affects the HALE calculation and contributes to the gender gap.
2. **Goal is to explain the gap** - The purpose of the model is to estimate what portion of the HALE gender gap is explainable by each factor. If infant/child mortality contributes to the gap, it should be included to properly attribute its contribution.
3. **Gender differences exist** - Infant mortality is typically higher in males, and this gender difference will affect HALE calculations. Under-five mortality also shows gender differences that should be accounted for.

**However**, note that:
- **Relative contribution may be smaller** - In most countries, adult mortality patterns (smoking, cardiovascular disease, accidents, violence) likely contribute more to the HALE gender gap than infant/child mortality, especially in high-income countries. But the relative contribution should be determined empirically, not assumed.
- **More important in lower-income countries** - In countries with high infant/child mortality rates, these factors may contribute more substantially to the HALE gender gap.
- **Different causal pathways** - Early-life mortality is driven by different factors (infectious diseases, malnutrition, birth complications) than adult mortality (chronic diseases, accidents, violence, lifestyle factors), so including both provides a more complete picture.

**Recommendation for HALE model**: 
- **Include infant mortality rate (male vs. female difference or ratio)** - Use `imr` or `MDG_0000000001` as a predictor to quantify its contribution to the HALE gender gap.
- **Include under-five mortality rate** - Use `MDG_0000000007` (not `u5mr`) as the predictor. ✅ **Implemented** - Data download functionality added to `who_data.py`.
  - **Why MDG_0000000007 over u5mr**: While both indicators have similar metadata (249 countries, 1932-2023), `MDG_0000000007` provides much better data quality when filtered for sex dimension:
    - `MDG_0000000007`: 30,648 records with sex dimension (5,976 Male, 5,976 Female, 18,696 Both sexes), clean structure with proper gender breakdowns
    - `u5mr`: Only 724 records with sex dimension, many records have other dimension types (age groups, regions, wealth quintiles) mixed in, making the data messy and harder to work with
    - Both have the same temporal and country coverage, but `MDG_0000000007` has cleaner, more usable data for gender gap analysis
- Infant and under-five mortality are correlated, so test both to see which provides better explanatory power or include both if they capture different aspects.
- The rate indicators (`imr`, `MDG_0000000007`) are preferable to absolute number indicators for cross-country comparison.

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

## Promising Indicators Checklist

Based on the [WHO GHO Indicators Index](https://www.who.int/data/gho/data/indicators/indicators-index), the following indicators are most relevant for analyzing HALE gender gaps. They are likely to differ between men and women and are related to causes of death.

### Already Implemented ✅
- [x] **HALE (Healthy Life Expectancy)** - Target variable (WHOSIS_000002)
- [x] **Cardiovascular disease death rates** - Age-standardized, by gender
- [x] **Smoking prevalence** - Age-standardized tobacco smoking, by gender (M_Est_smk_curr_std)
- [x] **Suicide rates** - Age-standardized, by gender (MH_12)
- [x] **Alcohol-attributable death rates** - Age-standardized, by gender (SA_0000001832)
- [x] **Unintentional poisoning mortality rates** - By gender (SDGPOISON)
- [x] **Road traffic crash death rates** - Age-standardized (15+), by gender (SA_0000001459)
- [x] **Maternal mortality ratio** - Per 100,000 live births, female-specific (MDG_0000000026)
- [x] **Homicide rates** - By gender (VIOLENCE_HOMICIDERATE)
- [x] **Intimate partner violence prevalence** - Female-specific, prevalence indicator (SDGIPV)
- [x] **Under-five mortality rate** - By gender (MDG_0000000007) - Note: MDG_0000000007 chosen over u5mr for better data quality

### High Priority - To Investigate
- [ ] **Tuberculosis deaths** - May have gender differences; TB deaths (excluding HIV)
- [ ] **HIV/AIDS mortality rates** - Can have gender differences, especially in certain regions
- [ ] **Diabetes death rates** - Age-standardized, by gender
- [ ] **Chronic respiratory disease death rates** - Age-standardized, by gender (COPD, asthma, etc.)
- [ ] **Liver disease/cirrhosis death rates** - Age-standardized, by gender (alcohol-related and other)
- [ ] **Kidney disease death rates** - Age-standardized, by gender
- [ ] **Cancer death rates (specific types)** - Lung cancer, liver cancer, etc. (gender-specific patterns)

### Medium Priority - To Investigate
- [ ] **Air pollution attributable death rates** - May have gender differences due to occupational exposure
- [ ] **Occupational injury death rates** - Likely much higher in men
- [ ] **Drowning death rates** - May have gender differences
- [ ] **Fire/burn death rates** - May have gender differences
- [ ] **Falls death rates** - May have gender differences, especially in elderly
- [ ] **Ischemic heart disease death rates** - More specific than general cardiovascular
- [ ] **Stroke death rates** - Age-standardized, by gender

### Lower Priority - May Be Useful
- [ ] **Adult mortality rate (15-60 years)** - Probability of dying, by gender
- [ ] **Adolescent mortality rate** - May show early gender differences
- [ ] **Underweight prevalence (adults)** - BMI < 18.5, may affect mortality differently by gender
- [ ] **Obesity prevalence** - May have different mortality implications by gender

**Notes:**
- Focus on indicators with age-standardized rates when available (matches HALE methodology)
- Prioritize indicators with gender breakdowns (Male, Female, Both sexes)
- Consider temporal coverage - indicators with multiple years are preferred
- Some indicators may need to be searched by alternative names or codes

## Analysis Steps
<!-- Outline the steps you'll take -->

## Expected Outcomes
<!-- What do you hope to discover? -->

## Notes
<!-- Add any additional notes, ideas, or observations -->

