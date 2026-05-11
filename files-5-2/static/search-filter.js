/* ===================================================
   TABLE SEARCH & FILTER (Recherche et filtrage tableaux)
   Description: Filtrage/recherche dans les tableaux
   Fonction principale:
     - filterTable(inputId, tableId, emptyMsgId)
       Filtre les lignes en matching 'data-search' avec la requête
       Cache aussi les formulaires édition en ligne quand parent caché
   Utilisation:
     <input id="search" onkeyup="filterTable('search', 'table', 'empty-msg')" />
   =================================================== */
/* =========================================================
   ENNOUJOUM — Table search / filter
   Filters table rows by matching a query against each row's
   `data-search` attribute. Edit rows that follow a searched
   row are hidden when the parent row is hidden (so an open
   edit form does not stay visible after filtering).
   ========================================================= */

function filterTable(inputId, tableId, emptyMsgId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    if (!input || !table) return;

    const query = input.value.toLowerCase().trim();
    const rows  = table.querySelectorAll('tbody tr');
    let visible = 0;
    let lastRowVisible = true;

    rows.forEach(row => {
        if (row.classList.contains('searchable-row')) {
            const haystack = (row.getAttribute('data-search') || '').toLowerCase();
            const match    = !query || haystack.indexOf(query) !== -1;
            row.style.display = match ? '' : 'none';
            lastRowVisible = match;
            if (match) visible++;
        } else {
            // Non-searchable row (typically an inline edit form).
            // Only show it if its parent searchable row is visible.
            if (!lastRowVisible) row.style.display = 'none';
        }
    });

    const empty = emptyMsgId ? document.getElementById(emptyMsgId) : null;
    if (empty) empty.style.display = (visible === 0 && query) ? 'inline-block' : 'none';
}
