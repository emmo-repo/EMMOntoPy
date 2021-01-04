package org.simphony;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Logger;

import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.formats.RDFXMLDocumentFormat;
import org.semanticweb.owlapi.model.IRI;
import org.semanticweb.owlapi.model.OWLAxiom;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.semanticweb.owlapi.model.OWLOntology;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyIRIMapper;
import org.semanticweb.owlapi.model.OWLOntologyManager;
import org.semanticweb.owlapi.model.OWLOntologyStorageException;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.util.InferredAxiomGenerator;
import org.semanticweb.owlapi.util.InferredClassAssertionAxiomGenerator;
import org.semanticweb.owlapi.util.InferredDataPropertyCharacteristicAxiomGenerator;
// import org.semanticweb.owlapi.util.InferredDisjointClassesAxiomGenerator;
import org.semanticweb.owlapi.util.InferredEquivalentClassAxiomGenerator;
import org.semanticweb.owlapi.util.InferredEquivalentDataPropertiesAxiomGenerator;
import org.semanticweb.owlapi.util.InferredEquivalentObjectPropertyAxiomGenerator;
import org.semanticweb.owlapi.util.InferredInverseObjectPropertiesAxiomGenerator;
import org.semanticweb.owlapi.util.InferredObjectPropertyCharacteristicAxiomGenerator;
import org.semanticweb.owlapi.util.InferredOntologyGenerator;
// import org.semanticweb.owlapi.util.InferredPropertyAssertionGenerator;
import org.semanticweb.owlapi.util.InferredSubClassAxiomGenerator;
import org.semanticweb.owlapi.util.InferredSubDataPropertyAxiomGenerator;
import org.semanticweb.owlapi.util.InferredSubObjectPropertyAxiomGenerator;
import org.semanticweb.owlapi.util.OWLOntologyMerger;

import uk.ac.manchester.cs.factplusplus.owlapiv3.FaCTPlusPlusReasonerFactory;

import org.protege.xmlcatalog.owlapi.XMLCatalogIRIMapper;

/**
 * Load an ontology, run the reasoner and export the inferred axioms to RDF
 * format.
 *
 */
public class OntologyLoader {
    private final static Logger LOGGER = Logger.getLogger(OntologyLoader.class.getName());
    private OWLOntologyManager manager;
    private OWLDataFactory dataFactory;
    private OWLOntology ontology;
    private IRI ontologyIRI;
    private File outputFile;

    public OntologyLoader() throws IOException {
        this.manager = OWLManager.createOWLOntologyManager();
        this.dataFactory = OWLManager.getOWLDataFactory();
        this.outputFile = new File("./_result_ontology.owl");
    }

    public void loadOntologies(String[] args) {
        for (String arg : args) {
            try {
                File file = new File(arg);
                loadCatalog(file);
                ontology = manager.loadOntologyFromOntologyDocument(file);
            } catch (OWLOntologyCreationException e) {
                e.printStackTrace();
                LOGGER.warning("Could not load " + arg);
            }
        }
    }

    public void mergeOntologies() throws OWLOntologyCreationException {
        OWLOntologyManager newManager = OWLManager.createOWLOntologyManager();
        OWLOntologyMerger merger = new OWLOntologyMerger(manager);
        ontologyIRI = IRI.create(outputFile);
        ontology = merger.createMergedOntology(newManager, ontologyIRI);
        manager = newManager;
    }

    public void generateInferredAxioms() {
        OWLReasonerFactory rf = new FaCTPlusPlusReasonerFactory();
        OWLReasoner reasoner = rf.createReasoner(ontology);
        List<InferredAxiomGenerator<? extends OWLAxiom>> gens = new ArrayList<>();
        gens.add(new InferredSubClassAxiomGenerator());
        gens.add(new InferredClassAssertionAxiomGenerator());
        // gens.add(new InferredDisjointClassesAxiomGenerator());
        gens.add(new InferredEquivalentClassAxiomGenerator());
        gens.add(new InferredEquivalentDataPropertiesAxiomGenerator());
        gens.add(new InferredEquivalentObjectPropertyAxiomGenerator());
        gens.add(new InferredInverseObjectPropertiesAxiomGenerator());
        gens.add(new InferredObjectPropertyCharacteristicAxiomGenerator());
        // gens.add(new InferredPropertyAssertionGenerator());
        gens.add(new InferredSubDataPropertyAxiomGenerator());
        gens.add(new InferredDataPropertyCharacteristicAxiomGenerator());
        gens.add(new InferredObjectPropertyCharacteristicAxiomGenerator());
        gens.add(new InferredSubObjectPropertyAxiomGenerator());
        InferredOntologyGenerator iog = new InferredOntologyGenerator(reasoner, gens);
        iog.fillOntology(dataFactory, ontology);
    }

    public void saveOntology() throws OWLOntologyStorageException {
        manager.saveOntology(ontology, new RDFXMLDocumentFormat());
    }

    private void loadCatalog(File owl_file) {
        File directory = owl_file.getParentFile();
        if (directory == null) {
            directory = new File(".");
        }
        for (String filename : directory.list()) {
            if (filename.startsWith("catalog") && filename.endsWith(".xml")) {
                try {
                    File catalog = new File(directory, filename);
                    OWLOntologyIRIMapper mapper = new XMLCatalogIRIMapper(catalog);
                    manager.getIRIMappers().add(mapper);
                    LOGGER.info("Loaded catalog file " + catalog.toString());
                } catch (IOException e) {
                    LOGGER.warning("Could not load catalog file "+ filename);
                    continue;
                }
            }
        }
    }

    public static void main(String[] args) throws IOException, OWLOntologyCreationException,
            OWLOntologyStorageException {
        // Path projectRoot = Paths.get(".").normalize().toAbsolutePath();
        // System.setProperty("java.library.path",
        //         projectRoot.toString() + "/lib:" + System.getProperty("java.library.path"));
        OntologyLoader loader = new OntologyLoader();
        String command = args[0];
        loader.loadOntologies(Arrays.copyOfRange(args, 1, args.length));
        loader.mergeOntologies();
        System.out.println(command);
        if (command.equals("--run-reasoner")) {
            loader.generateInferredAxioms();
            System.out.println("Reasoner executed");
        }
        loader.saveOntology();
    }
}
