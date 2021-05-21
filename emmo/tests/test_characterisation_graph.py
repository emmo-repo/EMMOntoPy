#!/usr/bin/env python3
import sys
import os
import time

# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology  # noqa: E402, F401


# Create output directory
outdir = 'test_graph2'
if not os.path.exists(outdir):
    os.makedirs(outdir)
os.chdir(outdir)


# emmopath = os.path.abspath(os.path.join(thisdir, '..', '..', '..',
#                                         'EMMO', 'emmo.ttl'))
emmopath = os.path.abspath(os.path.join(thisdir, 'emmo-inferred.ttl'))
emmo = get_ontology(emmopath)
emmo.load()
time.sleep(1)
# emmo.sync_reasoner()
time.sleep(1)


# Characterisation
leafs = {
         emmo.Sample,
         }
hidden = {emmo.Variable, emmo.Theory, emmo.Manufacturing, emmo.Engineered,
          emmo.PhysicalPhenomenon,
          emmo.Icon, emmo.Index, emmo.Interpretant,
          emmo.MeasurementUnit, emmo.SpecialUnit,
          emmo.IndexSemiosis, emmo.ConventionalSemiosis, emmo.IconSemiosis,
          emmo.Theorization, emmo.Experiment,
          emmo.Declarer, emmo.Deducer, emmo.Cogniser,
          emmo.SubjectiveProperty, emmo.NominalProperty,
          emmo.ModelledQuantitativeProperty,
          emmo.ConventionalQuantitativeProperty,
          }
semiotic = emmo.get_branch(emmo.Holistic, leafs=leafs.union(hidden))
semiotic.difference_update(hidden)
g = emmo.get_graph()
g.add_entities(semiotic, relations='all', edgelabels=False)
g.add_legend()
# g.save('characterisation.png')


# Modelling
leafs = {
    emmo.Model, emmo.Property,
    }
hidden = {emmo.Variable, emmo.Theory, emmo.Manufacturing, emmo.Engineered,
          emmo.Observation, emmo.Sample, emmo.Observer,
          emmo.PhysicalPhenomenon,
          emmo.Index, emmo.Interpretant,
          emmo.MeasurementUnit, emmo.SpecialUnit,
          emmo.IndexSemiosis, emmo.ConventionalSemiosis, emmo.IconSemiosis,
          emmo.Theorization, emmo.Experiment,
          emmo.Declarer, emmo.Deducer, emmo.Cogniser,
          emmo.SubjectiveProperty, emmo.NominalProperty,
          emmo.MeasuredQuantitativeProperty, emmo.MeasuredUncertainty,
          emmo.MeasurementResult,
          emmo.ConventionalQuantitativeProperty,
          }
semiotic = emmo.get_branch(emmo.Holistic, leafs=leafs.union(hidden))
semiotic.difference_update(hidden)
g = emmo.get_graph()
g.add_entities(semiotic, relations='all', edgelabels=False)
g.add_legend()
g.save('modelling.png')
