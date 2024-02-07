import argparse
import time
import json
from index import Index

def parse_args():
    """
    Parses command-line arguments using argparse.

    Returns:
    - argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Creation of different indexes")
    parser.add_argument(
        "json_file",
        type=str,
        help="The json file that contains the crawled webpages."
    )
    parser.add_argument(
        "columns_to_index",
        type=str,
        help="The information that should be used to create the indexes and the metadata file. \
            Usually they are the 'title', the 'content' and 'h1'. \
            They are all contained in the same string, separated by spaces"
    )
    parser.add_argument(
        "--index_for_content",
        type=bool,
        default=False,
        help="Needs to be specified to know if an index should be created for the 'content'. \
        With this value set to be true, the algorithm is taking longer to run."
    )
    parser.add_argument(
        "--stem_index",
        type=bool,
        default=False,
        help="Needs to be specified if an index with the stems is wanted, in addition to the token index.\
            Might take longer if the value is set to True"
    )
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_args()

    # Converting the type of one of the argument into a list
    columns_to_index_list = str.split(args.columns_to_index)

    # Saving the time when the algoirthm starts
    t0=time.time()

    index= Index(args.json_file, columns_to_index_list)
    index.create_metadata()
    index.create_index(args.index_for_content, args.stem_index)

    # Saving the time the algorithm ends
    t1=time.time()

    # Printing the time taken by the algorithm to create the indexes
    print(f"time taken to crawl: {t1-t0}")


if __name__ == "__main__":
    main()
