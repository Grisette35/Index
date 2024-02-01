import argparse
import time
from index import Index

def parse_args():
    """
    Parses command-line arguments using argparse.

    Returns:
    - argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Web Crawler")
    parser.add_argument(
        "seed_url",
        type=str,
        help="The seed URL to start crawling from."
    )
    parser.add_argument(
        "--max_urls",
        type=int,
        default=100,
        help="Maximum number of URLs to crawl. Default is 100."
    )
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_args()

    # Saving the time when the crawler starts
    t0=time.time()
    
    # Initialize database
    crawler_db = Crawler_db()
    conn, cursor = crawler_db.create_conn()
    crawler_db.initialize_database(conn, cursor)

    # Create a Crawler object with user-specified parameters
    crawler = Crawler(seed_url=args.seed_url, conn=conn, cursor=cursor, max_urls=args.max_urls)

    # Start crawling
    crawler.crawl()

    crawler.write_downloaded()

    # Close the database connection
    crawler_db.close_conn(conn)

    # Saving the time the crawler ends
    t1=time.time()

    # Printing the time taken by the crawler to crawl
    print(f"time taken to crawl: {t1-t0}")

if __name__ == "__main__":
    main()
