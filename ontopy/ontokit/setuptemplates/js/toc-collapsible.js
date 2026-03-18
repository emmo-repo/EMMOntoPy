/**
 * toc-collapsible.js
 *
 * Adds collapse/expand toggle buttons to every level of the page-TOC
 * sidebar rendered by pydata-sphinx-theme's page-toc.html.
 *
 * Each <li> that contains a nested <ul> gets a small toggle button
 * inserted immediately after its anchor.  Clicking the button hides or
 * shows the child list.  The state is tracked with a CSS class
 * "toc-items-collapsed" on the child <ul>, and the button label
 * flips between ▼ (expanded) and ► (collapsed).
 */
document.addEventListener("DOMContentLoaded", function () {
  // pydata-sphinx-theme wraps the page-toc in a <nav> inside the
  // primary sidebar.  We cast a wide net across possible class names
  // used by different versions of the theme.
  const tocNavs = document.querySelectorAll(
    ".bd-sidebar-primary nav, " +
    ".sidebar-primary-item nav, " +
    ".bd-toc-nav, " +
    "[aria-label='Page'] ul"
  );

  if (!tocNavs.length) return;

  tocNavs.forEach(function (nav) {
    // Only target <li> elements that directly own a child <ul>
    nav.querySelectorAll("li").forEach(function (li) {
      const childUl = li.querySelector(":scope > ul");
      if (!childUl) return;

      // Build the toggle button
      const btn = document.createElement("button");
      btn.className = "toc-toggle-btn";
      btn.setAttribute("aria-label", "Toggle subsection");
      btn.setAttribute("aria-expanded", "true");
      btn.textContent = "\u25BC"; // ▼ (expanded)
      btn.title = "Collapse/expand";

      // Place the button right after the <a> link (or as first child)
      const anchor = li.querySelector(":scope > a");
      if (anchor) {
        anchor.after(btn);
      } else {
        li.prepend(btn);
      }

      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        const collapsed = childUl.classList.toggle("toc-items-collapsed");
        btn.textContent = collapsed ? "\u25BA" : "\u25BC"; // ► or ▼
        btn.setAttribute("aria-expanded", String(!collapsed));
      });
    });
  });
});
