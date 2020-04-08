# Instructions for tools available in emmopython #

## emmocheck ##
Tool for checking that ontologies conform to EMMO conventions.

### usage: ###
emmocheck [options] iri

### options: ###
--catalog-file CATALOGFILE : Name of Protègè catalog file in the same 
folder as the ontology. This option is used together with --local and 
defaults to "catalog-v001.xml".  
--check-imported (-i) :     Whether to check imported ontologies.  
--configfile (-c) CONFIGURE : A yaml file with additional test configurations.  
--database (-d) FILENAME : Load ontology from Owlready sqlite3 database. The iri should be one of the ontologies in the database.  
-h : help  
--local (-l) : Load imported ontologies locally.  Their paths are specified
in Protègè catalog files or via the --path option. The IRI should be a 
file name.  
--path PATH : Paths where imported ontologies can be found.  May be provided
as a comma-separated string and/or with multiple --path options.  
--verbose (-v) :  

### examples: 
emmocheck http://emmo.info/emmo/1.0.0-alpha2  
emmocheck --database demo.sqlite3 http://www.emmc.info/emmc-csa/demo#  
emmocheck -l emmo.owl (in folder to which emmo was downloaded locally)  

(Missing example with local and path)  

## ontoversion ##
Prints version of an ontology to standard output

This script uses rdflib and the versionIRI tag of the ontology to infer
the version.

### usage: ###
ontoversion [options] iri

### special dependencies: ###
rdflib (python package)

### options: ###
--format (-f) FORMAT: OWL format.  Default is "xml".  
-h :  help

### examples: ###
ontoversion http://emmo.info/emmo/1.0.0-alpha

Comment: Fails if no versionIRI is given

## ontograph ##
Tool for visualizing ontologies.

### usage: ###
ontograph [options] iri [output]

### dependencies : ###
Graphviz

### options: ###
--addconstructs (-c) : Whether to add nodes representing class constructs.  
--addnodes (-n) : Whether to add missing target nodes in relations.'  
--catalog-file CATALOG_FILE : Name of Protègè catalog file in the same 
folder as the ontology.  This option is used together with --local and 
defaults to "catalog-v001.xml"  
--database (-d) FILENAME : Load ontology from Owlready2 sqlite3 database.
The `iri` argument should in this case be the IRI of the ontology 
you want to visualise.  
--display (-D) : Whether to display graph.  
--edgelabels (-e) : Whether to add labels to edges.  
--exclude (-E) EXCLUDE : Nodes, including their subclasses, 
to exclude from sub-graphs. May be provided as a comma-separated 
string and/or with multiple --exclude options.  
--format (-f) FORMAT :Format of output file.  By default it is inferred 
from the output file extension.  
--generate-style-file (-S) JSON_FILE : Write default style file 
to a json file.  
-h : help  
--legend (-L) : Whether to add a legend to the graph.  
--leafs LEAFS : Leaf nodes for plotting sub-graphs.  May be provided as 
a comma-separated string and/or with multiple --leafs options.  
--local (l) :Load imported ontologies locally.  Their paths are specified
in Protègè catalog files or via the --path option.  The IRI should
be a file name.  
--path PATH : Paths where imported ontologies can be found.  
May be provided as a comma-separated string and/or with 
multiple --path options.  
--parents (-p) N : Adds N levels of parents to graph.  
--plot-modules (-m) : Whether to plot module inter-dependencies 
instead of their content.  
--rankdir {BT,TB,RL,LR} : Graph direction (from leaves to root).  
Possible values are: "BT" (bottom-top, default), "TB" (top-bottom), 
"RL" (right-left) and "LR" (left-right).  
--reasoner [{HermiT,Pellet}] : Run given reasoner on the ontology.
Valid reasoners are "HermiT" (default) and "Pellet".
Note: these reasoners do not work well with EMMO.  
--relations (-R) RELATIONS : Comma-separated string of relations 
to visualise.  Default is "isA".  "all" means include all relations.  
--root ROOT : Name of root node in the graph.  Defaults to all classes.  
--style-file (-s) JSON_FILE : A json file with style definitions.  

### examples: ###



## ontodoc ##
Tool for documenting ontologies.
### usage: ###
ontodoc [options] iri outfile

### dependencies: ###
pandoc
pdflatex or xelatex

### options: ###
--catalog-file CATALOG_FILE : Name of Protègè catalog file in the same folder as the 
ontology.  This option is used together with --local and defaults to "catalog-v001.xml".  
--database (-d) FILENAME :  Load ontology from Owlready2 sqlite3 database. 
The `iri` argument should in this case be the IRI of the ontology you want to document.  
--figdir (-D) DIR :  Default directory to store generated figures.  If a relative 
path is given, it is relative to the template (see --template), or 
the current directory, if --template is not given. Default: "genfigs"  
--figformat (-F) FIGFORMAT : Format for generated figures.  The default is inferred from 
--format.  
--format (-f) FORMAT : Output format.  May be "md", "simple-html" or any other format 
supported by pandoc.  By default the format is inferred from --output.  
-h : help  
--keep-generated (-k) FILE : Keep a copy of generated markdown input file for pandoc (for debugging).  
--local (-l):  Load imported ontologies locally.  Their paths are specified
in Protègè catalog files or via the --path option.  The IRI should 
be a file name. 
--max-figwidth (-w) MAX_FIGWIDTH : Maximum figure width.  The default is inferred from --format.  
--pandoc-option (-p) STRING : Additional pandoc long options overriding those read from --pandoc-option-file.
It is possible to remove pandoc option --XXX with "--pandoc-option=no-XXX". This option may be provided 
multiple times.   
--pandoc-option-file (-P) FILE :  YAML file with additional pandoc options.  Note, that default 
pandoc options are read from the files "pandoc-options.yaml" and "pandoc-FORMAT-options.yaml" 
(where FORMAT is format specified with '--format).
This option allows to override the defaults and add additional pandoc options.
This option may be provided multiple times.  
--path PATH : Paths where imported ontologies can be found.  
May be provided as a comma-separated string and/or with 
multiple --path options. 
--reasoner [{HermiT,Pellet} :  Run given reasoner on the ontology.
Valid reasoners are "HermiT" (default) and "Pellet".
Note: these reasoners do not work well with EMMO.  
--template (-t) FILE : ontodoc input template.  If not provided, a simple default 
template will be used.  Do not confuse it with the pandoc templates.
