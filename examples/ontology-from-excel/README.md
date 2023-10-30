# Generate an ontology from excel

This directory contains an example xlsx-file for how to document ontology entities (classes, object properties, annotation properties and data properties) in an Excel workbook.
This workbook can then be used to generate a new ontology or update an already existing ontology with new entities (existing entities are not updated).

Please refer to the (documentation)[https://emmo-repo.github.io/EMMOntoPy/latest/api_reference/ontopy/excelparser/] for full explanation of capabilities.

The file `tool/onto.xlsx` contains examples on how to do things correctly as well as incorrectly.
The tool will by default exit without generating the ontology if it detects concepts defined incorrectly.
However, if the argument force is set to True, it will skip concepts that are erroneously defined
and generate the ontology with what is availble.

To run the tool directly
```console
cd tool # Since the excel file provides a relative path to an imported ontology
excel2onto onto.xlsx # This will fail
excel2onto --force onto.xlsx
```
We suggest developing your excelsheet without fails as once it starts getting big it is difficult to see what is wrong or correct.

It is also possible to generate the ontology in python.
Look at the script make_onto.py for an example.

That should be it.
Good luck!
