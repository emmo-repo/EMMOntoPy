/**
 * section-nav.js
 *
 * A javascript that enables navigation in generated documentation using a
 * query parameter. E.g.
 *
 *     page.html?section=my-heading
 *
 * will navigate to section "my-heading".
 *
 * This script will:
 *   - Read the section query parameter
 *   - Locate the element whose id matches the value
 *   - Scroll to that element
 *   - Optionally rewrite the URL to use a clean #fragment instead of the
 *     query parameter
 * This works with any Sphinx theme (Read the Docs, basic, Alabaster, etc.)
 * because it only depends on standard DOM APIs.
 */
(function() {
    // Parse the query parameters
    const params = new URLSearchParams(window.location.search);
    const section = params.get("section");

    if (!section) {
        return; // Nothing to do
    }

    // Attempt to find the element by ID (Sphinx uses IDs for headings)
    const target = document.getElementById(section);

    if (target) {
        // Scroll to the element
        target.scrollIntoView({ behavior: "instant" });

        // OPTIONAL: clean up the URL and convert ?section=... into a hash
        // So the URL becomes page.html#my-heading
        history.replaceState(
            null,
            "",
            window.location.pathname + "#" + section
        );
    }
})();
