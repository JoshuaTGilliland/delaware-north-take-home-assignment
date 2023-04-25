from classes.CovidReportData import CovidReportData
from classes.ReportSaver import ReportSaver

from argparse import ArgumentParser, RawTextHelpFormatter, Namespace
from datetime import datetime, timedelta
from tabulate import tabulate
import pandas as pd

def main():
    parser: ArgumentParser = ArgumentParser(
        description = 'reports the total number of PCR tests performed as of an inputted lookback day', 
        formatter_class = RawTextHelpFormatter
    )
    parser.add_argument('lookbackDays', type = int, help = 'how many days to look back (e.g., 0 = today, 1 = yesterday)')
    parser.add_argument('--timestampReport', action = 'store_true', default = False, help = 'adds current timestamp to report for easy referencing')
    args: Namespace = parser.parse_args()
    
    lookbackDate: str = (datetime.today() + timedelta(days = (args.lookbackDays * -1))).strftime('%Y-%m-%dT00:00:00.000')

    covidReport: CovidReportData = CovidReportData(
        dataPath = 'assets\json\coviddata.json',
        description = f'The total number of PCR tests performed in the U.S. {args.lookbackDays} days ago',
        query = f"""
            SELECT DISTINCT 
                sum(cast(total_results_reported AS long)) as total 
            FROM 
                df 
            WHERE 
                date = '{lookbackDate}'
            """
    )

    response: pd.DataFrame = covidReport.query_data()

    outputReport: str = tabulate(
        response, 
        headers = 'keys', 
        tablefmt = 'grid', 
        showindex = False, 
        floatfmt = '.0f', 
        stralign= 'right'
    )

    ReportSaver.save_report(
        output = str(outputReport),
        filename = f'pcr_tests_performed_{args.lookbackDays}-days-lookback.txt',
        addTimestamp = args.timestampReport
    )

if __name__ == '__main__':
    main()