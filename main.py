import argparse
import time
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
        type=list,
        help="The information that should be used to create the indexes and the metadata file. \
            Usually they are the 'title', the 'content' and 'h1'."
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

    # Saving the time when the crawler starts
    t0=time.time()

    # Saving the time the crawler ends
    t1=time.time()

    # Printing the time taken by the crawler to crawl
    print(f"time taken to crawl: {t1-t0}")

    index= Index(args.json_file, args.columns_to_index, args.index_for_content, args.stem_index)
    index.create_metadata()
    index.create_index(False, True)


if __name__ == "__main__":
    main()
