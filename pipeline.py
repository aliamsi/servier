from pathlib import Path
import logging

from src.transform import find_drug_mentions
from src.utils.file import save_to_json, process_file
from src.utils.constants import SCHEMA
from src.utils.utils import process_publication

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    """
    Main function to orchestrate the data processing pipeline.

    This function loads the datasets, combines same files data, finds drug mentions in
    clinical trials and PubMed publications, and saves the results to a JSON file.
    """
    logging.info("Starting data processing pipeline")

    # Define file paths
    file_paths = [
        Path("data/bronze/drugs.csv"),
        Path("data/bronze/pubmed.csv"),
        Path("data/bronze/pubmed.json"),
        Path("data/bronze/clinical_trials.csv"),
    ]

    publications = process_publication(file_paths)

    drugs_data = process_file(Path("data/bronze/drugs.csv"))
    drugs = {
        "rows": drugs_data["valid_rows"],
        "search_column": SCHEMA["search_column"]["drugs"],
    }

    # Find drug mentions in PubMed and clinical trials
    all_mentions = find_drug_mentions(drugs, publications)

    # Save to JSON
    save_to_json(all_mentions, "data/gold/drug_mentions.json")
    logging.info("Data processing pipeline completed successfully")


if __name__ == "__main__":
    main()
