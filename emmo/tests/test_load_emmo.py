# Add emmo to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology  # noqa: E402, F401


emmo = get_ontology(
    'https://raw.githubusercontent.com/emmo-repo/EMMO/v1.0.0/emmo.owl')
emmo.load()
