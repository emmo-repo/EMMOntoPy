"""
python example for creating ontology from excel
"""
from ontopy.excelparser import create_ontology_from_excel
from ontopy.utils import write_catalog

ontology, catalog = create_ontology_from_excel("onto.xlsx")

ontology.save("microstructure_ontology.ttl", format="turtle", overwrite=True)
write_catalog(catalog)
