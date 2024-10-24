from pathlib import Path
import logging

from src.transform import find_drug_mentions
from src.utils.file import process_file, save_to_json
from src.utils.constants import SCHEMA

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """
    Main function to orchestrate the data processing pipeline.

    This function loads the datasets, combines PubMed data, finds drug mentions in
    clinical trials and PubMed publications, and saves the results to a JSON file.
    """
    logging.info("Starting data processing pipeline")
    
    # Load datasets
    drugs = process_file(Path('data/bronze/drugs.csv'))
    pubmed_csv = process_file(Path('data/bronze/pubmed.csv'))
    pubmed_json = process_file(Path('data/bronze/pubmed.json'))
    clinical_trials_csv = process_file(Path('data/bronze/clinical_trials.csv'))
    
    # Combine all PubMed data
    all_pubmed = pubmed_csv | pubmed_json
    pubmed = {
        'rows': all_pubmed['valid_rows'],
        'table_name': 'pubmed',
        'search_column': SCHEMA['search_column']['pubmed']
    }
    clinical_trials = {
        'rows': clinical_trials_csv['valid_rows'],
        'table_name': 'clinical_trials',
        'search_column': SCHEMA['search_column']['clinical_trials']
    }
    drugs = {
        'rows': drugs['valid_rows'],
        'table_name': 'drugs',
        'search_column': SCHEMA['search_column']['drugs']
    }

    # Find drug mentions in PubMed and clinical trials
    pubmed_mentions = find_drug_mentions(drugs, pubmed)
    clinical_mentions = find_drug_mentions(drugs, clinical_trials)

    # Combine results
    all_mentions = pubmed_mentions + clinical_mentions

    # Save to JSON
    save_to_json(all_mentions, 'data/gold/drug_mentions.json')
    logging.info("Data processing pipeline completed successfully")


if __name__ == '__main__':
    main()
