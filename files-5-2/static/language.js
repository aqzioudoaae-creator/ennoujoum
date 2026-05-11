/* ===================================================
   🇦 SECTION: LANGUAGE MANAGEMENT (Gestion langues)
   Description: Gestion du/de la français et arabe + RTL
   Dépend de: i18n_fr.js, i18n_ar.js
   Fonctions principales:
     - getLang(): Récupérer la langue actuelle
     - setLang(lang): Changer la langue
     - applyLang(lang): Appliquer la langue à la page
     - toggleLang(): Basculer FR <-> AR
   =================================================== */
/* =========================================================
   language.js — Gestion de la langue (FR / AR + RTL)
   Dépend de : i18n_fr.js, i18n_ar.js
   ========================================================= */

const I18N = { fr: window.I18N_FR, ar: window.I18N_AR };

function getLang() {
    return localStorage.getItem('mnojo_lang') || 'fr';
}

function setLang(lang) {
    if (lang !== 'fr' && lang !== 'ar') lang = 'fr';
    localStorage.setItem('mnojo_lang', lang);
    // Sync cookie so the server (get_lang()) reads the correct language
    document.cookie = 'mnojo_lang=' + lang + '; path=/; max-age=31536000; SameSite=Lax';
    applyLang(lang);
}

function applyLang(lang) {
    const dict = I18N[lang] || I18N.fr;
    const html = document.documentElement;
    html.setAttribute('lang', lang);
    html.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');

    // Translate all elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key] !== undefined) el.textContent = dict[key];
    });

    // Translate placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (dict[key] !== undefined) el.setAttribute('placeholder', dict[key]);
    });

    // Translate titles (tooltips)
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        if (dict[key] !== undefined) el.setAttribute('title', dict[key]);
    });

    // Translate page title
    const titleEl = document.querySelector('title[data-i18n]');
    if (titleEl) {
        const key = titleEl.getAttribute('data-i18n');
        if (dict[key] !== undefined) document.title = dict[key];
    }

    // Translate status badges
    const statusMap = {
        "Started":     dict["status.started"],
        "In Progress": dict["status.in_progress"],
        "Finished":    dict["status.finished"]
    };
    document.querySelectorAll('[data-status-text]').forEach(el => {
        const original = el.getAttribute('data-status-text');
        if (statusMap[original]) el.textContent = statusMap[original];
    });

    // Translate <select> option labels
    document.querySelectorAll('option[data-i18n-status]').forEach(opt => {
        const original = opt.getAttribute('data-i18n-status');
        if (statusMap[original]) opt.textContent = statusMap[original];
    });

    // Update language toggle button label
    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) langBtn.textContent = dict["common.lang.toggle"];
}

function toggleLang() {
    setLang(getLang() === 'fr' ? 'ar' : 'fr');
}
