from classes.CovidReportData import CovidReportData
from classes.ReportSaver import ReportSaver

from argparse import ArgumentParser, RawTextHelpFormatter, Namespace
from datetime import datetime, timedelta
from tabulate import tabulate
import pandas as pd

def main():
    parser: ArgumentParser = ArgumentParser(
        description = 'retrieves the top states based on test positivity rating in the past inputted number of days', 
        formatter_class = RawTextHelpFormatter
    )
    parser.add_argument('stateCount', type = int, help = 'how many states to include in the top count')
    parser.add_argument('lookbackDays', type = int, help = 'how many days to look back (e.g., 0 = today, 1 = yesterday)')
    parser.add_argument('--stateFormat', choices = ['state', 'state_name', 'state_fips'], default = 'state', help = 'the format of the state output')
    parser.add_argument('--timestampReport', action = 'store_true', default = False, help = 'adds current timestamp to report for easy referencing')
    args: Namespace = parser.parse_args()
    
    lookbackDate: str = (datetime.today() + timedelta(days = (args.lookbackDays * -1))).strftime('%Y-%m-%dT00:00:00.000')

    covidReport: CovidReportData = CovidReportData(
        dataPath = 'assets\json\coviddata.json',
        description = f'The top {args.stateCount} states based on test positivity rating in the last {args.lookbackDays} days',
        query = f"""
            SELECT DISTINCT
                {args.stateFormat}
                , (sum(positive_results) / sum(total_results) * 100) AS pct
            FROM (
                SELECT DISTINCT
                    {args.stateFormat}
                    , date
                    , CASE
                        WHEN overall_outcome = 'Positive' THEN CAST(new_results_reported AS float)
                        ELSE 0 END AS positive_results
                    , CAST(new_results_reported AS float) AS total_results
                FROM
                    df 
                WHERE 
                    date >= '{lookbackDate}' 
            )
            GROUP BY
                {args.stateFormat}
            ORDER BY
                pct DESC
            LIMIT 
                {args.stateCount}
            """
    )

    response: pd.DataFrame = covidReport.query_data()

    outputReport: str = tabulate(
        tabular_data = response,
        headers = 'keys', 
        tablefmt = 'grid', 
        showindex = False, 
        floatfmt = '.6f', 
        stralign= 'right'
    )

    ReportSaver.save_report(
        output = str(outputReport),
        filename = f'highest_positivity_rate_{args.stateCount}-states_{args.lookbackDays}-days-lookback.txt',
        addTimestamp = args.timestampReport
    )

if __name__ == '__main__':
    main()