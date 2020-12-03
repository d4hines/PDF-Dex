import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from elastic_connector import verify_indexes

from file_handling import get_pdf_list
from process_files import process_file

def create_threaded_workers(MAX_THREADS):
    """
    Finds all the files in a directory and creates worker threads
    """

    verify_indexes()

    # Get all the pdf paths
    pdf_list = get_pdf_list()

    # Create threadpool
    t = ThreadPoolExecutor(max_workers=MAX_THREADS)
    t.map(process_file, pdf_list)

    t.shutdown(wait=True)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process PDF\'s into Elasticsearch Index')
    
    parser.add_argument('--threads', 
                        type=int,
                        help='Number of threads to run process under.',
                        default=1)

    args = parser.parse_args()

    create_threaded_workers(args.threads)

