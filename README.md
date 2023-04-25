# Delaware North - Lead Data Engineer Take-Home Assignment
## COVID-19 Reporting Tools
## Joshua Gilliland
### 2023-04-25

# Dependencies
Please run the following pip command in the main code directory to download any dependencies to run the project:

`pip install ./lib`

# How to Use
The following project ingests COVID-19 test result data based in the U.S., along with its territories, and provides reports based on standard metrics.

## Step 1: Load the dataset
Ensure you are connected to the internet first.

Then, run the following Python code to retrieve the necessary dataset:

`python dataset.py load`

This will save the COVID-19 test result data in a .json object for the scripts to retrieve, process, and generate reports based on the data.

## Step 2: Run a Report
There are currently three available reports based on the COVID-19 testing data:

1. `pcr_tests_performed.py`
2. `highest_positivity_rate.py`
3. `rolling_averages.py`

To run any of these scripts, execute the command and include the `--help` argument to ensure any applicable inputs are correct.

You may want to include the optional `--timestampReport` argument for easier referencing.

## Step 3: Read the Report
After the script successfully executes, the generated report will be printed in console and saved to a `.txt` file for future use.

The filename will correspond to the positional arguments inputted when executing the script.

Each report will look like a text-based table with the output data ordered with the desired priorities.

# Insights

## `pcr_tests_performed.py`

The assumption in this test is that "United States" refers to all 50 states plus its territories.

The desired arguments for this assignment are listed below:
- lookbackDays = 1 (to indicate "yesterday")

However, running this command did not produce any output because the dataset has not been refreshed with the most recent data from yesterday.

Therefore, operating under the assumption that no result is better than an estimate based on the last day with data--since we want exact data and not estimates--I generated separate reports for each day working backwards until I received a non-zero output.

This day was 3 days ago (2023-04-22). The output looked like this:

total |
--- |
664767815 |

The oddity here is that days prior seem to result in a higher number. Perhaps that is because of corrections in test counts as the days progress. Or, perhaps old test results fall outside of consideration after a certain time.

## `highest_positivity_rate.py`

The desired arguments for this assignment are listed below:
- stateCount = 10
- lookbackDays = 30

The result looked like this:

|   state |      pct |
---|---|
|      IA | 1.000000 |
|      VI | 0.457143 |
|      MO | 0.222938 |
|      SD | 0.187616 |
|      OK | 0.147738 |
|      HI | 0.123326 |
|      NM | 0.117746 |
|      NV | 0.113813 |
|      UT | 0.112672 |
|      ND | 0.112580 |

The table is ordered by highest percent descending.

It appears that smaller states/territories have higher positivity rates, which could mean a few things:
1. More densely-populated areas are taking more tests (or require more tests) on a regular basis.
2. Smaller, less city-based populations do not take or report COVID-19 tests unless there is a higher probability of a positive result.


## `rolling_averages.py`

The desired arguments for this assignment are listed below:
- rollingAverageWindow = 7
- lookbackDays = 30

The result looked like this:

|       date |    average |
---|---|
| 2023-03-26 | 15488.2900 |
| 2023-03-27 | 15421.5700 |
| 2023-03-28 | 15268.4300 |
| 2023-03-29 | 14886.2900 |
| 2023-03-30 | 14507.7100 |
| 2023-03-31 | 14209.4300 |
| 2023-04-01 | 13901.2900 |
| 2023-04-02 | 13697.8600 |
| 2023-04-03 | 13542.5700 |
| 2023-04-04 | 13329.1400 |
| 2023-04-05 | 13138.0000 |
| 2023-04-06 | 12820.2900 |
| 2023-04-07 | 12432.0000 |
| 2023-04-08 | 12082.1400 |
| 2023-04-09 | 11851.2900 |
| 2023-04-10 | 11595.0000 |
| 2023-04-11 | 11316.4300 |
| 2023-04-12 | 10944.2900 |
| 2023-04-13 | 10768.2900 |
| 2023-04-14 | 10649.2900 |
| 2023-04-15 | 10463.1400 |
| 2023-04-16 | 10269.2900 |
| 2023-04-17 | 10130.7100 |
| 2023-04-18 |  9807.1400 |
| 2023-04-19 |  9237.5700 |
| 2023-04-20 |  8677.5700 |
| 2023-04-21 |  8070.5700 |
| 2023-04-22 |  7353.7100 |

The rolling average decreases over time, indicating that new cases have been dropping in the past month compared ot the prior 7-day window. 

This test assumes a U.S.-wide perspective; a future report could be to stratify the results based on states to see which states trend downward in the last month and which ones trend upward.