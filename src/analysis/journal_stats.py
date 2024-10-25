import json
import logging
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional

from src.utils.retry import retry_on_error
from src.config.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@retry_on_error(max_retries=3, retry_delay=1)
def load_json_data(file_path: Path) -> List[Dict]:
    """
    Load and validate drug mentions data from JSON file.

    Args:
        file_path: Path to the drug mentions JSON file

    Returns:
        List of drug mention dictionaries

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    logging.info(f"Loading drug mentions data from: {file_path}")
    with open(file_path, "r") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Drug mentions data must be a list")

    return data


def analyze_journal_mentions(data: List[Dict]) -> Optional[Dict]:
    """
    Analyze drug mentions data to find the journal with most different drugs.

    Args:
        data: List of drug mention dictionaries

    Returns:
        Dictionary containing journal analysis results or None if no valid data
    """
    logging.info("Analyzing journal drug mentions")

    if not data:
        logging.warning("No drug mentions data available")
        return None

    # Create a mapping of journals to the drugs they mention
    journal_drugs = defaultdict(set)

    # Process each drug mention
    for drug_mention in data:
        drug_code = drug_mention.get("drug")
        if not drug_code:
            logging.warning(f"Found drug mention without drug code: {drug_mention}")
            continue

        # Get all journal mentions for this drug
        journal_mentions = drug_mention.get("journal", [])

        # Add the drug to each journal's set of mentioned drugs
        for mention in journal_mentions:
            journal_name = mention.get("name")
            if journal_name:
                journal_drugs[journal_name].add(drug_code)

    if not journal_drugs:
        logging.warning("No valid journal mentions found in the data")
        return None

    # Find the journal with the most drugs
    journal_name = max(journal_drugs.items(), key=lambda x: len(x[1]))[0]

    result = {
        "name": journal_name,
        "drug_count": len(journal_drugs[journal_name]),
        "drugs": sorted(list(journal_drugs[journal_name])),
    }

    logging.info(
        f"Found journal with most drugs: {journal_name} "
        f"({result['drug_count']} drugs)"
    )

    return result


def save_analysis_results(results: Dict, output_path: Path) -> None:
    """
    Save analysis results to JSON file.

    Args:
        results: Analysis results dictionary
        output_path: Path where to save the results
    """
    logging.info(f"Saving analysis results to: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    logging.info("Analysis results saved successfully")


def main():
    """Main function to orchestrate the journal analysis."""
    # Load configuration
    config = Config()

    logging.info("Starting journal analysis")

    try:
        # Define input/output paths
        input_path = Path(config.get("paths")["gold"]) / "drug_mentions.json"
        output_path = Path(config.get("paths")["gold"]) / "journal_analysis.json"

        # Load and validate data
        data = load_json_data(input_path)

        # Analyze journal mentions
        results = analyze_journal_mentions(data)

        if results:
            # Save analysis results
            save_analysis_results(results, output_path)

            # Print results summary
            print("\nAnalysis Results:")
            print(f"Journal with most drug mentions: {results['name']}")
            print(f"Number of different drugs: {results['drug_count']}")
            print(f"Drugs mentioned (ATC codes): {', '.join(results['drugs'])}")
        else:
            logging.error("Analysis failed: No valid data to analyze")

    except Exception as e:
        logging.error(f"Analysis failed: {str(e)}")
        raise

    logging.info("Journal analysis completed")


if __name__ == "__main__":
    main()
