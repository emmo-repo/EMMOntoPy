from emmo import World                                                 
from emmo import get_ontology                                           

world = World()
battinfo = world.get_ontology('https://raw.githubusercontent.com/BIG-MAP'
                              '/BattINFO/master/battinfo.ttl').load()                                  

   

bvco = world.get_ontology('https://gitlab.cc-asp.fraunhofer.de/ISC-Public/'
                    'ISC-Digital/ontology/bvco/-/raw/master/'
                    'BVCO_inferred.ttl').load()

   

onto = world.get_ontology('bothontologies.ttl')
onto.imported_ontologies
onto.imported_ontologies.append(battinfo)
onto.imported_ontologies.append(bvco)
onto.sync_python_names()
onto.Atom
