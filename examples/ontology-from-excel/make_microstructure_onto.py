"""
python example for creating ontology from excel
"""
from ontopy.excelparser import create_ontology_from_excel

ontology, catalog = create_ontology_from_excel("onto.xlsx")
