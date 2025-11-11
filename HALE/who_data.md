# WHO Global Health Observatory (GHO) API Documentation

## Overview

The WHO GHO API provides programmatic access to health statistics through an OData-compliant REST API. The base URL is:
```
https://ghoapi.azureedge.net/api/
```

## API Structure

### Key Endpoints

1. **Indicator Endpoint**: `/Indicator`
   - Lists all available health indicators
   - Supports OData filtering (e.g., `$filter=contains(IndicatorName,'search_term')`)

2. **Specific Indicator Data**: `/{INDICATOR_CODE}`
   - Retrieves data for a specific indicator
   - Example: `/WHOSIS_000002` (HALE data)

3. **Dimension Values**: `/DIMENSION/{DIMENSION_TYPE}/DimensionValues`
   - Lists available values for dimensions (e.g., countries, years)
   - Example: `/DIMENSION/COUNTRY/DimensionValues`

## OData Filtering

The API supports OData query syntax for filtering data at the API level, which is more efficient than downloading all data and filtering locally.

### Year Filtering

Use the `$filter` parameter with `TimeDim` to filter by years:

- **Single year**: `$filter=TimeDim eq 2020`
- **Year range**: `$filter=TimeDim ge 2015 and TimeDim le 2023`
- **Multiple specific years**: `$filter=(TimeDim eq 2015 or TimeDim eq 2020 or TimeDim eq 2023)`

### Example URL
```
https://ghoapi.azureedge.net/api/WHOSIS_000002?$filter=TimeDim ge 2000 and TimeDim le 2021
```

## Data Structure

Each data record contains:
- `SpatialDim`: Country code
- `SpatialDimType`: Country dimension type
- `TimeDim`: Year
- `Dim1`: Sex dimension (SEX_MLE, SEX_FMLE, SEX_BTSX)
- `NumericValue`: The actual data value
- `Low`: Lower bound (if available)
- `High`: Upper bound (if available)
- `IndicatorName`: Name of the indicator
- `DataSourceDim`: Data source
- `Comments`: Additional comments

## Key Indicators for HALE Gender Gap Analysis

### HALE (Healthy Life Expectancy)
- **Indicator Code**: `WHOSIS_000002`
- **Available Years**: 2000-2021
- **Sex Categories**: Male, Female, Both sexes
- **Coverage**: 196 countries
- **Status**: ✅ Good coverage, multiple years

### Cardiovascular Disease Death Rates

Several indicators are available, but most have limited year coverage:

1. **WHS2_161** - Age-standardized mortality rate by cause (Cardiovascular)
   - **Available Years**: Limited (appears to have data but query returned empty)
   - **Status**: ⚠️ May require specific filtering

2. **SA_0000001444** - Age-standardized death rates, ischaemic heart disease
   - **Available Years**: 2004 only
   - **Coverage**: 191 countries
   - **Sex Categories**: Male, Female, Both sexes
   - **Status**: ⚠️ Limited to single year

3. **SA_0000001690** - Age-standardized death rates, cerebrovascular disease
   - **Available Years**: 2004 only
   - **Coverage**: 191 countries
   - **Sex Categories**: Male, Female, Both sexes
   - **Status**: ⚠️ Limited to single year

**Finding**: Most cardiovascular death rate indicators in the WHO GHO API appear to have data only for 2004, which limits their usefulness for time-series analysis. This may be a data availability constraint rather than an API limitation.

### Smoking/Tobacco Use Indicators

Several smoking prevalence indicators are available with good temporal coverage and sex breakdowns:

1. **M_Est_smk_curr_std** - Estimate of current tobacco smoking prevalence (%) (age-standardized rate)
   - **Available Years**: 2000, 2005, 2007, 2010, 2015, 2018, 2020, 2021, 2022, 2025, 2030
   - **Coverage**: 172 countries
   - **Sex Categories**: Male, Female, Both sexes
   - **Total Records**: 5,181
   - **Status**: ✅ Excellent - multiple years, sex breakdowns, age-standardized

2. **M_Est_cig_curr_std** - Estimate of current cigarette smoking prevalence (%) (age-standardized rate)
   - **Available Years**: 2000, 2005, 2007, 2010, 2015, 2020, 2021, 2022, 2025, 2030
   - **Coverage**: 165 countries
   - **Sex Categories**: Male, Female, Both sexes
   - **Total Records**: 4,950
   - **Status**: ✅ Excellent - multiple years, sex breakdowns, cigarette-specific

3. **Adult_curr_tob_smoking** - Prevalence of current tobacco smoking among adults (%)
   - **Available Years**: 2001-2022 (with some gaps: 2001, 2003, 2008-2022)
   - **Coverage**: 190 countries
   - **Sex Categories**: Male, Female, Both sexes
   - **Total Records**: 570
   - **Status**: ✅ Good - broader country coverage, more recent years

**Note**: Many other smoking indicators exist (57+ for "smoking", 208+ for "tobacco") but most are policy/regulatory indicators rather than prevalence data. The indicators above are the most relevant for analyzing smoking as a predictor of HALE gender gaps.

**Finding**: Smoking prevalence indicators have much better temporal coverage than cardiovascular death rates, making them suitable for time-series analysis. The age-standardized estimates (M_Est_smk_curr_std, M_Est_cig_curr_std) are particularly useful as they control for age structure differences between countries.

## Available Methods in `who_data.py`

### Data Retrieval Methods

1. **`get_indicator_data(indicator_code, params=None, years=None)`**
   - Retrieves raw data for any indicator
   - Supports OData filtering via `params`
   - Automatically builds year filters when `years` parameter is provided

2. **`get_hale_data(years=None)`**
   - Retrieves HALE data by sex
   - Returns pandas DataFrame with columns: Country, CountryCode, Year, Sex, HALE_Years, HALE_Low, HALE_High

3. **`get_cardiovascular_death_rates(years=None)`**
   - Retrieves cardiovascular disease death rates by gender
   - Tries multiple indicator codes to find available data
   - Returns pandas DataFrame with death rate data

### Exploration Methods

4. **`search_indicators(search_term)`**
   - Searches for indicators by name/keyword
   - Returns DataFrame with IndicatorCode and IndicatorName

5. **`list_all_indicators()`**
   - Lists all available indicators
   - Returns DataFrame with all indicator codes and names

6. **`get_indicator_years(indicator_code)`**
   - Gets list of available years for a specific indicator
   - Returns sorted list of years

7. **`get_indicator_info(indicator_code)`**
   - Gets comprehensive information about an indicator
   - Returns dictionary with:
     - Available years
     - Year range
     - Number of countries
     - Sex categories
     - Total records

## Command-Line Usage

### Download Data

```bash
# Download HALE data
python HALE/who_data.py --data hale

# Download cardiovascular data
python HALE/who_data.py --data cardio

# Download both
python HALE/who_data.py --data both

# Filter by years
python HALE/who_data.py --data hale --years "2015-2021"
python HALE/who_data.py --data hale --years "2015,2020,2021"
```

### Explore Indicators

```bash
# Search for indicators
python HALE/who_data.py --list-indicators "smoking"
python HALE/who_data.py --list-indicators "cardiovascular"
python HALE/who_data.py --list-indicators "death rate"

# Get info about a specific indicator
python HALE/who_data.py --indicator-info "WHOSIS_000002"
python HALE/who_data.py --indicator-info "SA_0000001444"
python HALE/who_data.py --indicator-info "M_Est_smk_curr_std"

# List all indicators (first 50)
python HALE/who_data.py --list-indicators ""
```

### Options

- `--data`: Choose data to download (hale, cardio, both, all)
- `--years`: Filter by years (range: "2015-2021" or list: "2015,2020,2021")
- `--output-dir`: Directory to save files (default: "data")
- `--hale-filename`: Custom filename for HALE data
- `--cardio-filename`: Custom filename for cardiovascular data
- `--verbose`: Show detailed output
- `--list-indicators`: Search or list indicators
- `--indicator-info`: Get detailed info about an indicator

## Recommendations

1. **For HALE Data**: Use `WHOSIS_000002` - it has good coverage (2000-2021) and includes sex breakdowns.

2. **For Smoking/Tobacco Data**: Use `M_Est_smk_curr_std` or `M_Est_cig_curr_std` - both have excellent temporal coverage (2000-2030) with sex breakdowns and age-standardized rates. These are ideal for analyzing smoking as a predictor of HALE gender gaps.

3. **For Cardiovascular Data**: The WHO GHO API has limited year coverage (mostly 2004). Consider:
   - Using alternative data sources (e.g., Our World in Data, Global Burden of Disease)
   - Using the 2004 data as a cross-sectional snapshot
   - Searching for other mortality indicators that might have better temporal coverage

4. **For Other Predictors**: Use the exploration tools to find indicators for:
   - ✅ Smoking rates - Found: `M_Est_smk_curr_std`, `M_Est_cig_curr_std`, `Adult_curr_tob_smoking`
   - Suicide rates - Search with `--list-indicators "suicide"`
   - Maternal mortality - Search with `--list-indicators "maternal"`
   - Other relevant health indicators

5. **Year Filtering**: Always use OData filters at the API level when possible - it's more efficient than downloading all data and filtering locally.

## Additional Resources

- **WHO GHO Main Page**: https://apps.who.int/gho/data/
- **GHO API Documentation**: https://www.who.int/data/gho/info/gho-odata-api
- **OData Protocol**: https://www.odata.org/

## Notes

- Sex dimension values come in format `SEX_MLE`, `SEX_FMLE`, `SEX_BTSX` but are parsed to "Male", "Female", "Both sexes" in the code
- Some indicators may require specific dimension filters to return data
- The API may have rate limits or timeout issues for very large queries
- Not all indicators have data for all countries or all years

