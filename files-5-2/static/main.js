/* =========================================================
   ENNOUJOUM — Main bootstrap (DOM ready)
   This file is loaded LAST (after i18n_fr.js, i18n_ar.js,
   theme.js, language.js, search-filter.js). It just wires
   the DOM events to the helpers exposed by those modules.
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

    // Apply translations now that DOM is ready
    applyLang(getLang());

    // Theme toggle button
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

    // Language toggle button
    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) langBtn.addEventListener('click', toggleLang);

    // Auto-dismiss flash messages after 4 seconds
    document.querySelectorAll('.flash').forEach((flash) => {
        setTimeout(() => {
            flash.style.transition = 'opacity .4s, transform .4s';
            flash.style.opacity   = '0';
            flash.style.transform = 'translateX(40px)';
            setTimeout(() => flash.remove(), 400);
        }, 4000);
    });

    // Confirm before logging out
    document.querySelectorAll('.btn-logout').forEach((btn) => {
        btn.addEventListener('click', (e) => {
            const dict = I18N[getLang()] || I18N.fr;
            if (!confirm(dict["common.confirm.logout"])) {
                e.preventDefault();
            }
        });
    });

    // Highlight code input as user types (numeric only, max 3 digits)
    const codeInput = document.getElementById('code');
    if (codeInput) {
        codeInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '').slice(0, 3);
        });
    }
});
