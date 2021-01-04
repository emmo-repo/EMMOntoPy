package org.simphony;

import static org.junit.Assert.assertTrue;

import java.io.IOException;

import org.junit.Test;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyStorageException;

/**
 * Unit test for simple App.
 */
public class AppTest {
    /**
     * Rigorous Test :-)
     */
    @Test
    public void shouldAnswerWithTrue() {
        try {
            OntologyLoader.main(new String[] { "resources/foaf.rdf" });
        } catch (OWLOntologyCreationException | OWLOntologyStorageException | IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        assertTrue( true );
    }
}
