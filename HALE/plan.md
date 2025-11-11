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

4. **Maternal mortality ratio**
   - Important for understanding cases where gap is small due to high female mortality
   - Directly measurable and strongly impacts female life expectancy
   - Particularly relevant in lower-income countries

**Control variables:**
- Overall life expectancy (to control for general health level)
- GDP per capita (to control for economic development)




## Analysis Steps
<!-- Outline the steps you'll take -->

## Expected Outcomes
<!-- What do you hope to discover? -->

## Notes
<!-- Add any additional notes, ideas, or observations -->

