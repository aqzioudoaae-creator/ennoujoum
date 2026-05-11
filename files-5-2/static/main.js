/* ===================================================
   INIT & DOM EVENTS (Initialisation & événements DOM)
   Description: Point d'entrée principal - initialisation DOM
   Dépend de: theme.js, language.js
   Fonctions:
     - Appliquer les traductions (i18n)
     - Initialiser le toggle thème
     - Initialiser le toggle langue
     - Auto-dismiss des messages flash
     - Confirmation avant logout
     - Validation input code (3 chiffres max)
   =================================================== */
/* =========================================================
   main.js — Initialisation DOM et interactions
   Dépend de : theme.js, language.js
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

    // Apply translations now that DOM is ready
    applyLang(getLang());

    // Wire theme toggle button
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

    // Wire language toggle button
    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) langBtn.addEventListener('click', toggleLang);

    // Auto-dismiss flash messages after 4 seconds
    document.querySelectorAll('.flash').forEach((flash) => {
        setTimeout(() => {
            flash.style.transition = 'opacity .4s, transform .4s';
            flash.style.opacity    = '0';
            flash.style.transform  = 'translateX(40px)';
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

    // Code input: numeric only, max 3 digits
    const codeInput = document.getElementById('code');
    if (codeInput) {
        codeInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '').slice(0, 3);
        });
    }
});
