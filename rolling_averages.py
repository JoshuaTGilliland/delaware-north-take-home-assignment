from classes.CovidReportData import CovidReportData
from classes.ReportSaver import ReportSaver

from argparse import ArgumentParser, RawTextHelpFormatter, Namespace
from datetime import datetime, timedelta
from tabulate import tabulate

def main():
    parser: ArgumentParser = ArgumentParser(
        description = 'reports the rolling average of new cases per day based on a lookback period and average-case window', 
        formatter_class = RawTextHelpFormatter
    )
    parser.add_argument('rollingAverageWindow', type = int, help = 'how many days to consider for rolling average')
    parser.add_argument('lookbackDays', type = int, help = 'how many days to look back (e.g., 0 = today, 1 = yesterday)')
    parser.add_argument('--timestampReport', action = 'store_true', default = False, help = 'adds current timestamp to report for easy referencing')
    args: Namespace = parser.parse_args()
    
    lookbackDate: str = (datetime.today() + timedelta(days = ((args.lookbackDays + args.rollingAverageWindow) * -1))).strftime('%Y-%m-%dT00:00:00.000')

    covidReport: CovidReportData = CovidReportData(
        dataPath = 'assets\json\coviddata.json',
        description = f'The {args.rollingAverageWindow}-day rolling average number of new cases per day for the last {args.lookbackDays} days',
        query = f"""
            SELECT DISTINCT
                date
                , SUM(CAST(new_results_reported AS int)) AS new_cases
            FROM
                df
            WHERE
                overall_outcome = 'Positive'
                AND date >= '{lookbackDate}'
            GROUP BY
                date
            ORDER BY
                date ASC
        """
    )

    dates, newCaseCount = list(covidReport.query_data().to_dict(orient = 'list').values())
    outputTable: list[dict] = []

    for endIndex in range(args.rollingAverageWindow, len(dates)):
        startIndex: int = endIndex - args.rollingAverageWindow
        average: float = round(sum(newCaseCount[startIndex:endIndex]) / args.rollingAverageWindow, 2)
        outputTable.append({
            'date': dates[endIndex].split('T')[0],
            'average': average
        })

    outputReport: str = tabulate(
        tabular_data = outputTable,
        headers = 'keys', 
        tablefmt = 'grid', 
        showindex = False, 
        floatfmt = '.4f', 
        stralign= 'right'
    )

    ReportSaver.save_report(
        output = outputReport,
        filename = f'rolling_averages_{args.rollingAverageWindow}-days-window_{args.lookbackDays}-days-lookback.txt',
        addTimestamp = args.timestampReport
    )

if __name__ == '__main__':
    main()