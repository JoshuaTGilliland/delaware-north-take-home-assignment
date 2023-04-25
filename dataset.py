from classes.API import API

from argparse import ArgumentParser, RawTextHelpFormatter, Namespace

COVID_DATASET_URL: str = 'https://healthdata.gov/resource/j8mb-icvb.json'

def main():
    parser: ArgumentParser = ArgumentParser(
        description = 'manages covid-19 dataset retrieval and storage', 
        formatter_class = RawTextHelpFormatter
    )
    parser.add_argument('action', choices = ['load', 'clear'], help = 'loads or clears covid dataset for local use')
    args: Namespace = parser.parse_args()

    if args.action == 'load':
        API.get_as_list(COVID_DATASET_URL)
    elif args.action == 'clear':
        API.clear_json_data()

if __name__ == '__main__':
    main()