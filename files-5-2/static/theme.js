/* ===================================================
   THEME MANAGEMENT (Gestion light / dark mode)
   Description: Gestion du thème clair/sombre
   Fonctions principales:
     - getTheme(): Récupérer le thème actuel (défaut: 'light')
     - setTheme(theme): Définir le thème ('light' ou 'dark')
     - toggleTheme(): Basculer entre light <-> dark
     - earlyTheme(): Appliquer le thème AVANT le rendu (pas de flash)
   Stockage: localStorage 'mnojo_theme'
   =================================================== */
/* =========================================================
   theme.js — Gestion du thème (light / dark)
   ========================================================= */

function getTheme() {
    return localStorage.getItem('mnojo_theme') || 'light';
}

function setTheme(theme) {
    if (theme !== 'light' && theme !== 'dark') theme = 'light';
    localStorage.setItem('mnojo_theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
}

function toggleTheme() {
    setTheme(getTheme() === 'dark' ? 'light' : 'dark');
}

/* Apply theme immediately before paint to avoid flash */
(function earlyTheme() {
    try {
        var t = localStorage.getItem('mnojo_theme') || 'light';
        var l = localStorage.getItem('mnojo_lang')  || 'fr';
        document.documentElement.setAttribute('data-theme', t);
        document.documentElement.setAttribute('lang', l);
        document.documentElement.setAttribute('dir', l === 'ar' ? 'rtl' : 'ltr');
    } catch (e) {}
})();
