#!/bin/bash

# Logging function
log() {
    local level=$1
    local message=$2
    echo "$(date '+%Y-%m-%d %H:%M:%S') $level $message" | tee -a data_downloader.log
}

# Function to download sequences from NCBI
download() {
    local tag=$1
    shift
    local accessions=("$@")
    local ncbi_baseurl="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    local params="db=nuccore&retmode=text&rettype=fasta&usehistory=y&WebEnv="
    local ids=$(IFS=, ; echo "${accessions[*]}")

    # Send request to NCBI
    log "INFO" "Fetching data"
    response=$(curl -s --data "$params&id=$ids" "$ncbi_baseurl")

    if [ $? -ne 0 ]; then
        log "ERROR" "An error occurred during data fetch"
        exit 1
    fi

    # Write data to output file
    log "INFO" "Writing data to output file"
    echo "$response" > "${tag}_sequences.fasta"
    log "INFO" "Operation successful"
}

# Main script execution
if [ $# -lt 2 ]; then
    log "ERROR" "Please input accession numbers to be retrieved"
    echo -e "\nUsage: $0 <tag> <accession> <accession> <accession> .... \n"
    exit 1
fi

tag=$1
shift
download "$tag" "$@"

