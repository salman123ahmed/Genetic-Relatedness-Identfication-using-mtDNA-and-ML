#!/usr/bin/env python

import requests
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    # filename='data_downloader.log',
    format='%(asctime)s %(levelname)s %(message)s',
)


def download(accessions, tag):
    """
    A script to download sequences from NCBI
    :param tag:
    :param accessions:
    :return:
    """
    ncbi_baseurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    # declare default parameters
    params = {'db': 'nuccore', 'id': accessions, 'retmode': 'text', 'rettype': 'fasta',
              'usehistory': 'y', 'WebEnv': ''}

    # Send a request to the ncbi
    try:
        logging.info('Fetching data')
        handles = requests.post(ncbi_baseurl, data=params)
        logging.info('Writing data to output file')
        with open(f'{tag}_sequences.fasta', 'w') as results:
            results.write(handles.text)
            logging.info('Operation successful')

    except Exception as e:
        logging.error('An error occurred', e)


if __name__ == '__main__':
    sys.argv.remove(sys.argv[0])
    if len(sys.argv) >= 1:
        download(sys.argv)
    else:
        logging.error(
            "Please input accession numbers to be retrieved \n"
            "\nuse this format:$ python3 download.py <accession> <accession> <accession> .... \n"
        )
