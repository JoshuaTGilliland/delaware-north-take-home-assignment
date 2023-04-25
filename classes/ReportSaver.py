from datetime import datetime
from os import path, makedirs

class ReportSaver:
    """Static class to save generated reports into 'build' directory"""

    REPORTS_DIR: str = 'reports'

    @staticmethod
    def save_report(output: str, filename: str, addTimestamp: bool = False, printReport: bool = True):
        """Saves report to 'reports' directory, optionally adding timestamp
        
        Args:
            output (str): the contents of the report to save
            filename (str): the name of the outputted file
            addTimestamp (bool): indicates whether to add a timestamp to the filename
        """
        if not isinstance(output, str):
            raise TypeError('Error: output must be of type <str>')
        if not isinstance(filename, str):
            raise TypeError('Error: filename must be of type <str>')
        if not isinstance(addTimestamp, bool):
            raise TypeError('Error: addTimestamp must be of type <str>')
        if not isinstance(printReport, bool):
            raise TypeError('Error: printReport must be of type <str>')

        makedirs(ReportSaver.REPORTS_DIR, exist_ok = True)

        if addTimestamp:
            filenameNoExtension, _, extension = filename.rpartition('.')
            timestamp: str = datetime.now().strftime('%Y%d%m%H%M%S')
            filename: str = filenameNoExtension + '_' + timestamp + '.' + extension

        filePath: str = path.join(ReportSaver.REPORTS_DIR, filename)
        open(filePath, 'w').write(output)

        if printReport:
            print(output)

        print('')    
        print(f'[SUCCESS] The report has been saved: {filePath}')
