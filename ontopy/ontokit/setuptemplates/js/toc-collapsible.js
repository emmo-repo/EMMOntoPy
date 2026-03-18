/**
 * toc-collapsible.js
 *
 * Adds collapse/expand toggle buttons to every level of the page-TOC
 * sidebar rendered by pydata-sphinx-theme's page-toc.html.
 *
 * Each <li> that contains a nested <ul> gets a small chevron button
 * inserted as the first child (left gutter), similar to tree controls
 * in editors like VS Code. Clicking the button hides or shows the
 * child list.
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
      btn.textContent = "\u25BE"; // ▾ (expanded)
      btn.title = "Collapse/expand";

      // Mark items with children and place chevron in left gutter.
      li.classList.add("toc-has-children");
      li.prepend(btn);

      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        const collapsed = childUl.classList.toggle("toc-items-collapsed");
        li.classList.toggle("toc-collapsed", collapsed);
        btn.textContent = collapsed ? "\u25B8" : "\u25BE"; // ▸ or ▾
        btn.setAttribute("aria-expanded", String(!collapsed));
      });
    });
  });
});
