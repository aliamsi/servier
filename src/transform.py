import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def find_drug_mentions(drugs, publications):
    """
    Finds and returns mentions of drugs in a list of publications.

    Args:
        drugs (dict): A dictionary containing information about the drugs.
                      It should have the following structure:
                      - 'rows': A list of dictionaries, where each dictionary represents a drug
                                and contains at least the drug name and its ATC code.
                      - 'search_column': The name of the column in the 'drugs' dictionaries
                                        that contains the drug name.
        publications (dict): A dictionary containing information about the publications.
                             It should have the following structure:
                             - 'rows': A list of dictionaries, where each dictionary represents a publication
                                       and contains at least the publication ID, date, and title.
                             - 'search_column': The name of the column in the 'publications' dictionaries
                                               that contains the publication title.

    Returns:
        list: A list of dictionaries, where each dictionary represents a drug and its mentions
              in the publications. The dictionary structure is as follows:
              - 'drug': The ATC code of the drug.
              - 'pubmed': A list of dictionaries, where each dictionary represents a PubMed mention
                          and contains the publication ID and date.
              - 'journal': A list of dictionaries, where each dictionary represents a journal mention
                           and contains the journal name and date.
    """
    logging.info("Finding drug mentions in publications")

    def extract_mentions(drug):
        """
        Extracts mentions of a specific drug in the publications.

        Args:
            drug (dict): A dictionary representing a drug, containing at least the drug name
                         and its ATC code.

        Returns:
            dict: A dictionary containing the drug's ATC code, PubMed mentions, and journal mentions,
                  or None if no mentions are found.
        """
        logging.info(f"Extracting mentions for drug: {drug[drugs['search_column']]}")

        # Extract the drug name from the drug dictionary
        drug_name = drug[drugs["search_column"]].lower()

        # Filter publications that contain the drug name in the title
        mentions = {"drug": drug["atccode"]}
        for publication in publications:
            search_column = publication["search_column"]
            filtered_publications = list(
                filter(
                    lambda pub: drug_name in pub[search_column].lower(),
                    publication["rows"],
                )
            )

            if filtered_publications:
                # Format the results for each publication type
                mentions[publication["table_name"]] = list(
                    map(
                        lambda pub: {"id": pub["id"], "date": pub["date"]},
                        filtered_publications,
                    )
                )
                mentions["journal"] = list(
                    map(
                        lambda jour: {"name": jour["journal"], "date": jour["date"]},
                        filtered_publications,
                    )
                )

        # Create the final structure for the drug if there are any mentions
        return mentions if mentions.get("journal") else None

    # Apply the mention extraction for each drug
    mentions = map(extract_mentions, drugs["rows"])
    # Filter out any None values from the mentions list
    return list(filter(lambda mention: mention, mentions))
