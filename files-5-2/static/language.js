/* =========================================================
   ENNOUJOUM — Language switcher (FR / AR)
   Reads I18N_FR and I18N_AR (loaded BEFORE this file).
   Persists the choice in localStorage AND in a cookie so
   the Python backend can read the language for WhatsApp.
   ========================================================= */

const I18N = { fr: I18N_FR, ar: I18N_AR };

function getLang() {
    return localStorage.getItem('mnojo_lang') || 'fr';
}

function setLang(lang) {
    if (lang !== 'fr' && lang !== 'ar') lang = 'fr';
    localStorage.setItem('mnojo_lang', lang);
    // Set a cookie too so the Python backend can read the language
    // (used for translating WhatsApp messages server-side)
    document.cookie = 'mnojo_lang=' + lang + '; path=/; max-age=31536000; SameSite=Lax';
    applyLang(lang);
}

function toggleLang() {
    setLang(getLang() === 'fr' ? 'ar' : 'fr');
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

    // Translate status badges (text comes from server in English)
    const statusMap = {
        "Started":     dict["status.started"],
        "In Progress": dict["status.in_progress"],
        "Finished":    dict["status.finished"]
    };
    document.querySelectorAll('[data-status-text]').forEach(el => {
        const original = el.getAttribute('data-status-text');
        if (statusMap[original]) el.textContent = statusMap[original];
    });

    // Translate <select> option labels (value attribute stays in English for the backend)
    document.querySelectorAll('option[data-i18n-status]').forEach(opt => {
        const original = opt.getAttribute('data-i18n-status');
        if (statusMap[original]) opt.textContent = statusMap[original];
    });

    // Update the language toggle button label (shows the OTHER language)
    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) langBtn.textContent = dict["common.lang.toggle"];
}

/* Apply the saved language as early as possible (before DOM ready) */
(function earlyLangInit() {
    const lang = getLang();
    document.documentElement.setAttribute('lang', lang);
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    document.cookie = 'mnojo_lang=' + lang + '; path=/; max-age=31536000; SameSite=Lax';
})();
