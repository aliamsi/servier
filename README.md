# Drug Mention Extraction Pipeline
This project implements a data processing pipeline to extract mentions of drugs from scientific publications and clinical trials.

## Project Structure
├── src
│   ├── __init__.py
│   ├── transform.py
│   └── utils
│       ├── __init__.py
│       ├── file.py
│       └── constants.py
└── tests
    ├── __init__.py
    └── test_utils.py

## Functionality
The pipeline performs the following steps:

Data Loading: Loads data from CSV and JSON files containing information about drugs, PubMed publications, and clinical trials.
Data Combination: Combines data from multiple files related to the same entity (e.g., combining PubMed data from CSV and JSON files).
Drug Mention Identification: Identifies mentions of drug names within the titles of publications and clinical trials.
Output Generation: Generates a JSON file containing a list of drugs and their corresponding mentions in publications and clinical trials.
## Usage
Install Dependencies: Install the required Python packages listed in requirements.txt.
Data Preparation: Place the input data files (CSV and JSON) in the data/bronze directory.
Run the Pipeline: Execute the main.py script to run the data processing pipeline.
Output: The extracted drug mentions will be saved in a JSON file named drug_mentions.json in the data/gold directory.
## Testing
Unit tests are provided in the tests directory. You can run the tests using your preferred testing framework (e.g., unittest).

## Future Improvements
Implement more sophisticated drug name recognition techniques (e.g., using Named Entity Recognition models).
Extend the pipeline to extract drug mentions from the full text of publications and clinical trials.
Develop a user interface for interacting with the pipeline and visualizing the results.