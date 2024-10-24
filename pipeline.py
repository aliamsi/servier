from pathlib import Path
import logging
from typing import List
from src.config.config import Config
from src.utils.retry import retry_on_error
from src.transform import find_drug_mentions
from src.utils.file import save_to_json, process_file
from src.utils.constants import SCHEMA
from src.utils.utils import process_publication


def setup_logging(config: Config) -> None:
    """Setup logging configuration"""
    logging_config = config.get("logging")
    logging.basicConfig(
        level=logging_config.get("level", "INFO"),
        format=logging_config.get("format"),
        filename=logging_config.get("file"),
    )


def validate_input_files(file_paths: List[Path]) -> bool:
    """Validate input file paths"""
    for file_path in file_paths:
        if not file_path.exists():
            logging.error(f"Input file not found: {file_path}")
            return False
    return True


@retry_on_error(max_retries=3)
def process_drugs(drug_file_path: Path) -> dict:
    """Process drug data with retry mechanism"""
    drugs_data = process_file(drug_file_path)
    return {
        "rows": drugs_data["valid_rows"],
        "search_column": SCHEMA["search_column"]["drugs"],
    }


def main():
    config = Config()
    setup_logging(config)

    logging.info("Starting data processing pipeline")

    # Define file paths
    file_paths = [
        Path(config.get("paths")["bronze"]) / "drugs.csv",
        Path(config.get("paths")["bronze"]) / "pubmed.csv",
        Path(config.get("paths")["bronze"]) / "pubmed.json",
        Path(config.get("paths")["bronze"]) / "clinical_trials.csv",
    ]

    # Validate input files
    if not validate_input_files(file_paths):
        logging.error("Input file validation failed")
        return

    try:
        # Process publications
        publications = process_publication(file_paths)

        # Process drugs with retry mechanism
        drugs = process_drugs(file_paths[0])

        # Find drug mentions
        all_mentions = find_drug_mentions(drugs, publications)

        # Save results
        output_path = Path(config.get("paths")["gold"]) / "drug_mentions.json"
        save_to_json(all_mentions, output_path)

        logging.info("Data processing pipeline completed successfully")

    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
