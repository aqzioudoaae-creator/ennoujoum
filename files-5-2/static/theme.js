/* =========================================================
   ENNOUJOUM — Theme (light / dark)
   Persisted in localStorage. Apply the data-theme attribute
   on <html> so CSS variables can switch.
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

/* Apply the saved theme as early as possible (before DOM ready)
   so the page does not flash the wrong colors on load. */
document.documentElement.setAttribute('data-theme', getTheme());
