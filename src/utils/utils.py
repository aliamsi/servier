from src.utils.constants import PUBLICATION_TABLE_NAMES, SCHEMA
from src.utils.file import save_to_json, combine_files_by_table_name


def process_publication(file_paths):
    publications = []
    for table in PUBLICATION_TABLE_NAMES:
        # search matching files
        matching_files = [file for file in file_paths if table in file.name]
        # for file in matching_files, read data and combine
        combined_data = combine_files_by_table_name(matching_files)
        # save combined data to bronze folder
        save_to_json(combined_data[table]["valid_rows"], f"data/silver/{table}.json")

        # Prepare data for drug mention search
        data = {
            "rows": combined_data[table]["valid_rows"],
            "table_name": table,
            "search_column": SCHEMA["search_column"][table],
        }
        publications.append(data)

    return publications
