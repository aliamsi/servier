
def find_drug_mentions(drugs, publications):
    def extract_mentions(drug):
        # Extraire les colonnes à rechercher
        drug_name = drugs['search_column']

        # Filtrer les publications contenant le nom du médicament dans le titre
        filtered_pubmed = list(filter(lambda pub: drug[drug_name].lower() in pub[publications['search_column']].lower(), publications['rows']))

        # Formater les résultats pour chaque type de publication
        pubmed_mentions = list(map(lambda pub: {'id': pub['id'], 'date': pub['date']}, filtered_pubmed))
        journal_mentions = list(map(lambda jour: {'name': jour['journal'], 'date': jour['date']}, filtered_pubmed))

        # Créer la structure finale pour le médicament
        if any([pubmed_mentions, journal_mentions]):
            return {
            'drug': drug['atccode'],
            'pubmed': pubmed_mentions,
            'journal': journal_mentions
        }  
        
    
    # Appliquer l'extraction des mentions pour chaque médicament
    mentions = map(extract_mentions, drugs['rows'])
    return list(filter(lambda mention: mention, mentions))
