"""
python example for creating ontology from excel
"""

from pathlib import Path

from ontopy.excelparser import create_ontology_from_excel
from ontopy.utils import write_catalog


thisdir = Path(__file__).resolve().parent
ontology, catalog, errdict = create_ontology_from_excel(
    thisdir / "tool/onto.xlsx",
    force=True,  # Note will force generation of the ontology.
)


# Save the ontology and write out the catalog
ontology.save("onto.ttl", format="turtle", overwrite=True)
write_catalog(catalog)

# Look at the error dictionary
print(errdict.keys())
