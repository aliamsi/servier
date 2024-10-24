import json
import time
import csv
import re
from pathlib import Path
import charset_normalizer
from typing import List
import logging
import os
from datetime import datetime


from src.utils.constants import SCHEMA, DATA_TABLE_NAMES

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def combine_files_by_table_name(file_paths):
    """
    Takes a list of file paths, guesses the table name for each file,
    and combines files with the same table name.

    Args:
        file_paths (list): A list of file paths.

    Returns:
        dict: A dictionary where keys are table names and values are lists of
              combined data from files belonging to that table.
    """
    logging.debug("Combining files by table name")
    combined_data = {}
    for file_path in file_paths:
        table_name = get_name_from_path(file_path)
        if table_name:
            if table_name not in combined_data:
                combined_data[table_name] = {"valid_rows": [], "invalid_rows": []}
            processed_file = process_file(file_path)
            combined_data[table_name]["valid_rows"].extend(processed_file["valid_rows"])
            combined_data[table_name]["invalid_rows"].extend(
                processed_file["invalid_rows"]
            )
    return combined_data


def get_name_from_path(file_path):
    """
    Guess the table name from the file path.

    Args:
        file_path (Path): The path to the file.

    Returns:
        str: The guessed table name, or None if not found.
    """
    logging.debug(f"Guessing table name from file path: {file_path}")
    guessed_table_name = None
    for table_name in DATA_TABLE_NAMES:
        if table_name in file_path.name:
            guessed_table_name = table_name
            break
    logging.debug(f"Guessed table name: {guessed_table_name}")
    return guessed_table_name


def read_rows(file_path, encoding):
    """
    Read rows from a CSV file, validate them against the schema, and separate valid and invalid rows.

    Args:
        file_path (Path): The path to the CSV file.
        encoding (str): The encoding of the CSV file.

    Returns:
        dict: A dictionary containing lists of valid and invalid rows.
             - 'valid_rows': A list of dictionaries, where each dictionary represents a valid row.
             - 'invalid_rows': A list of dictionaries, where each dictionary represents an invalid row
                               and includes the error message.
    """
    logging.info(f"Reading rows from CSV file: {file_path}")

    time_st = time.time()
    valid_rows = []
    invalid_rows = []

    table_name = get_name_from_path(file_path)

    with file_path.open(newline="", encoding=encoding) as filename:
        reader = csv.DictReader(filename)

        for row in reader:
            is_valid, error = check_row(SCHEMA[table_name], row)

            if is_valid:
                valid_rows.append(row)
            else:
                invalid_rows.append({"row": row, "error": error})

    logging.debug(
        f"Finished reading rows from CSV file: {file_path} in {time.time() - time_st} seconds"
    )
    return {"valid_rows": valid_rows, "invalid_rows": invalid_rows}


def json_handler(file_path):
    """
    Handles JSON file reading and attempts to correct common JSON errors.

    Args:
        file_path (Path): The path to the JSON file.
        encoding (str): The encoding of the JSON file.

    Returns:
        dict: The loaded JSON data as a dictionary.
    """
    logging.info(f"Reading JSON file: {file_path}")
    rows = []
    with file_path.open("r", encoding="utf-8") as filename:
        content = filename.read()
        # Try to fix common JSON error of trailing commas
        json_string = re.sub(r",\s*(\}|\])", r"\1", content)

    try:
        output = json.loads(json_string)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        raise  # Re-raise the exception after logging

    return output


def read_json(file_path, encoding):
    """
    Read data from a JSON file, validate it against the schema, and separate valid and invalid entries.

    Args:
        file_path (Path): The path to the JSON file.
        encoding (str): The encoding of the JSON file.

    Returns:
        dict: A dictionary containing lists of valid and invalid entries.
             - 'valid_rows': A list of dictionaries, where each dictionary represents a valid entry.
             - 'invalid_rows': A list of dictionaries, where each dictionary represents an invalid entry
                               and includes the error message.
    """
    logging.info(f"Reading JSON file: {file_path}")

    time_st = time.time()
    valid_rows = []
    invalid_rows = []

    table_name = get_name_from_path(file_path)

    with file_path.open(newline="", encoding=encoding) as filename:
        try:
            output = json.load(filename)
        except json.JSONDecodeError as e:
            logging.warning(f"Encountered JSONDecodeError: {e}. Attempting to fix...")
            output = json_handler(file_path)

        for row in output:
            is_valid, error = check_row(SCHEMA[table_name], row)

            if is_valid:
                valid_rows.append(row)
            else:
                invalid_rows.append({"row": row, "error": error})

        logging.debug(
            f"Finished reading JSON file: {file_path} in {time.time() - time_st} seconds"
        )
        return {"valid_rows": valid_rows, "invalid_rows": invalid_rows}


def check_row(schema, row):
    """
    Check if a row conforms to the defined schema.

    Args:
        schema (dict): A dictionary where keys are column names and values are expected data types.
        row (dict): A dictionary representing a row from the file, where keys are column names
                   and values are the corresponding values.

    Returns:
        tuple: A tuple containing:
               - is_valid (bool): True if the row is valid according to the schema, False otherwise.
               - error (str): An error message if the row is invalid, otherwise None.
    """
    if len(row) != len(schema):
        return (
            False,
            f"Incorrect number of columns. Expected {len(schema)}, found {len(row)}.",
        )

    for col, expected_type in schema.items():
        value = row.get(col, None)
        try:
            if not isinstance(value, expected_type):
                # Attempt to convert the value if it's not of the correct type
                expected_type(value)
        except (ValueError, TypeError):
            return (
                False,
                f"Incorrect type for column '{col}'. Expected {expected_type}, found {type(value)}.",
            )

    return True, None


def get_encoding(file_path: Path):
    """
    Detect the encoding of a file.

    Args:
        file_path (Path): The path to the file.

    Returns:
        str: The detected encoding of the file.
    """
    logging.debug(f"Detecting encoding for file: {file_path}")

    with file_path.open("rb") as file:
        result = charset_normalizer.detect(file.read(10000))

        encoding = result["encoding"]
        logging.debug(f"Detected encoding: {encoding}")
        return encoding


def is_csv(file_path: Path) -> bool:
    """
    Check if a file has a CSV extension.

    Args:
        file_path (Path): The path to the file.

    Returns:
        bool: True if the file has a '.csv' extension, False otherwise.
    """
    return file_path.suffix == ".csv"


def is_json(file_path: Path) -> bool:
    """
    Check if a file has a JSON extension.

    Args:
        file_path (Path): The path to the file.

    Returns:
        bool: True if the file has a '.json' extension, False otherwise.
    """
    return file_path.suffix == ".json"


def process_file(file_path):
    """
    Process a file based on its type (CSV or JSON), read its content,
    and return the processed data.

    Args:
        file_path (Path): The path to the file.

    Returns:
        dict: A dictionary containing the processed data from the file.
              The structure of the dictionary depends on the file type.
    """
    logging.debug(f"Processing file: {file_path}")
    encoding = get_encoding(file_path)
    # table_name = get_name_from_path(file_path)

    if is_csv(file_path):
        reader = read_rows(file_path, encoding)

    elif is_json(file_path):
        reader = read_json(file_path, encoding)
    else:
        message = "File extension must be either CSV or JSON."
        logging.error(message)
        raise Exception(message)

    logging.debug(f"Finished processing file: {file_path}")
    return reader


def save_to_json(data, output_file, encoding="utf-8"):
    """
    Save data to a JSON file.

    Args:
        data: The data to be saved, which can be serialized to JSON.
        output_file (str): The path to the output JSON file.
        encoding (str, optional): The encoding for the output file. Defaults to 'utf-8'.
    """

    with open(output_file, "w", encoding=encoding) as file:
        json.dump(data, file, indent=4)

    logging.info(f"Data saved to JSON file: {output_file}")
