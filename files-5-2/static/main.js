/* =========================================================
   MNOJO - Main JavaScript
   ========================================================= */

// Auto-dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach((flash) => {
        setTimeout(() => {
            flash.style.transition = 'opacity .4s, transform .4s';
            flash.style.opacity   = '0';
            flash.style.transform = 'translateX(40px)';
            setTimeout(() => flash.remove(), 400);
        }, 4000);
    });
});

// Confirm before logging out
document.querySelectorAll('.btn-logout').forEach((btn) => {
    btn.addEventListener('click', (e) => {
        if (!confirm('Are you sure you want to logout?')) {
            e.preventDefault();
        }
    });
});

// Highlight code input as user types (uppercase + numeric only)
const codeInput = document.getElementById('code');
if (codeInput) {
    codeInput.addEventListener('input', (e) => {
        e.target.value = e.target.value.replace(/[^0-9]/g, '').slice(0, 3);
    });
}
