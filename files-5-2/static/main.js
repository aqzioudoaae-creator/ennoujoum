/* =========================================================
   MNOJO — Main JavaScript
   - Theme toggle (light/dark) with localStorage persistence
   - Language switcher (FR/AR) with RTL support
   - Existing features: flash auto-dismiss, logout confirm,
     code input filter
   ========================================================= */

/* ---------- i18n dictionary (FR + AR) ---------- */
const I18N = {
    fr: {
        "page.title.home":          "Ennojoum — Lavage Auto",
        "page.title.welcome":       "Ennojoum — Bienvenue",
        "page.title.employee_login":"Connexion Employé — Ennojoum",
        "page.title.client_login":  "Client — Suivez votre voiture",
        "page.title.admin_login":   "Connexion Manager — Ennojoum",
        "page.title.employee_dash": "Tableau de bord Employé — Ennojoum",
        "page.title.admin_dash":    "Tableau de bord Manager — Ennojoum",
        "page.title.tracking":      "Suivi — Ennojoum",

        "nav.home":                 "Accueil",
        "nav.track":                "Suivre ma voiture",
        "nav.dashboard":            "Tableau de bord",
        "nav.logout":                "Déconnexion",
        "nav.admin":                "Administrateur",

        "footer.text":              "Ennojoum — Système de gestion de lavage auto",

        "home.welcome":             "Bienvenue chez",
        "home.subtitle":            "Gestion intelligente du lavage auto. Plus d'attente en file. Recevez une notification WhatsApp dès que votre voiture est prête.",
        "home.role.employee":       "Employé",
        "home.role.employee.desc":  "Enregistrer les voitures et mettre à jour leur statut",
        "home.role.client":         "Client",
        "home.role.client.desc":    "Suivez votre voiture grâce à votre code unique",
        "home.role.manager":        "Manager",
        "home.role.manager.desc":   "Consulter les revenus et gérer les employés",
        "home.btn.login":           "Se connecter",
        "home.btn.track":           "Suivre",

        "login.employee.title":     "Connexion Employé",
        "login.employee.subtitle":  "Connectez-vous pour gérer les lavages",
        "login.client.title":       "Suivez votre voiture",
        "login.client.subtitle":    "Entrez le code unique reçu sur WhatsApp",
        "login.admin.title":        "Connexion Manager",
        "login.admin.subtitle":     "Connectez-vous pour consulter les statistiques et gérer les employés",
        "login.field.username":     "Nom d'utilisateur",
        "login.field.password":     "Mot de passe",
        "login.field.code":         "Code de suivi",
        "login.btn.login":          "Connexion",
        "login.btn.track":          "Suivre",
        "login.hint":               "Identifiants par défaut :",
        "login.back":               "← Retour à l'accueil",

        "emp.dash.title":           "Tableau de bord Employé",
        "emp.dash.subtitle":        "Enregistrez de nouvelles voitures et mettez à jour leur statut de lavage",
        "emp.register.title":       "Enregistrer une nouvelle voiture",
        "emp.field.car_type":       "Type de voiture",
        "emp.field.phone":          "Numéro de téléphone",
        "emp.field.wash_type":      "Type de lavage",
        "emp.field.price":          "Prix",
        "emp.opt.select":           "-- Sélectionner --",
        "emp.opt.small":            "Petite",
        "emp.opt.large":            "Grande",
        "emp.btn.register":         "Enregistrer et envoyer WhatsApp",
        "emp.cars.title":           "Toutes les voitures",
        "emp.empty":                "Aucune voiture enregistrée pour l'instant. Ajoutez la première ci-dessus.",
        "emp.send.code":            "Envoyer le code de suivi sur WhatsApp",
        "emp.send.reminder":        "Envoyer un rappel",

        "th.code":                  "Code",
        "th.car":                   "Voiture",
        "th.phone":                 "Téléphone",
        "th.wash":                  "Lavage",
        "th.price":                 "Prix",
        "th.status":                "Statut",
        "th.date":                  "Date",
        "th.actions":               "Actions",
        "th.id":                    "ID",
        "th.username":              "Utilisateur",
        "th.action":                "Action",
        "th.num":                   "#",

        "status.started":           "Commencé",
        "status.in_progress":       "En cours",
        "status.finished":          "Terminé",

        "admin.title":              "Tableau de bord Manager",
        "admin.subtitle":           "Aperçu des revenus, opérations et personnel",
        "admin.stat.total":         "Total voitures",
        "admin.stat.daily":         "Revenu du jour",
        "admin.stat.weekly":        "Revenu hebdo",
        "admin.stat.monthly":       "Revenu mensuel",
        "admin.status.title":       "Répartition des statuts",
        "admin.status.started":     "Commencé :",
        "admin.status.progress":    "En cours :",
        "admin.status.finished":    "Terminé :",
        "admin.employees.title":    "Employés",
        "admin.create.title":       "Créer un nouvel employé",
        "admin.create.username":    "Nom d'utilisateur",
        "admin.create.password":    "Mot de passe",
        "admin.create.btn":         "Créer l'employé",
        "admin.history.title":      "Historique de toutes les opérations",
        "admin.empty":              "Aucune opération pour l'instant.",
        "admin.whatsapp.title":     "Notifications WhatsApp récentes",
        "admin.whatsapp.empty":     "Aucun message envoyé pour l'instant.",
        "admin.whatsapp.open":      "Ouvrir",
        "admin.default":            "par défaut",
        "admin.delete":             "Supprimer",

        "track.title":              "Suivi de votre voiture",
        "track.code":               "Code",
        "track.step1":              "Commencé",
        "track.step1.desc":         "La voiture a été enregistrée",
        "track.step2":              "En cours",
        "track.step2.desc":         "Lavage en cours",
        "track.step3":              "Terminé",
        "track.step3.desc":         "Prête à être récupérée",
        "track.banner.started":     "Votre voiture est enregistrée. Le lavage va bientôt commencer.",
        "track.banner.progress":    "Votre voiture est en cours de lavage.",
        "track.banner.finished":    "Votre voiture est prête. Vous pouvez venir la récupérer.",
        "track.refresh":            "Cette page se met à jour automatiquement toutes les 10 secondes.",
        "track.back":               "← Suivre une autre voiture",
        "track.label.car":          "Voiture :",
        "track.label.wash":         "Lavage :",
        "track.label.price":        "Prix :",

        "common.confirm.delete":    "Supprimer l'employé",
        "common.confirm.logout":    "Voulez-vous vraiment vous déconnecter ?",
        "common.theme.toggle":      "Changer le thème",
        "common.lang.toggle":       "العربية"
    },
    ar: {
        "page.title.home":          "النجوم — غسيل السيارات",
        "page.title.welcome":       "النجوم — مرحباً",
        "page.title.employee_login":"دخول الموظف — النجوم",
        "page.title.client_login":  "العميل — تتبع سيارتك",
        "page.title.admin_login":   "دخول المدير — النجوم",
        "page.title.employee_dash": "لوحة تحكم الموظف — النجوم",
        "page.title.admin_dash":    "لوحة تحكم المدير — النجوم",
        "page.title.tracking":      "التتبع — النجوم",

        "nav.home":                 "الرئيسية",
        "nav.track":                "تتبع سيارتي",
        "nav.dashboard":            "لوحة التحكم",
        "nav.logout":                "تسجيل الخروج",
        "nav.admin":                "المدير",

        "footer.text":              "النجوم — نظام إدارة غسيل السيارات",

        "home.welcome":             "مرحباً بكم في",
        "home.subtitle":            "إدارة ذكية لغسيل السيارات. لا مزيد من الانتظار في الطابور. ستصلك إشعار عبر واتساب بمجرد أن تصبح سيارتك جاهزة.",
        "home.role.employee":       "موظف",
        "home.role.employee.desc":  "تسجيل السيارات وتحديث حالة الغسيل",
        "home.role.client":         "عميل",
        "home.role.client.desc":    "تتبع سيارتك باستخدام رمزك الخاص",
        "home.role.manager":        "مدير",
        "home.role.manager.desc":   "عرض الإيرادات وإدارة الموظفين",
        "home.btn.login":           "تسجيل الدخول",
        "home.btn.track":           "تتبع",

        "login.employee.title":     "دخول الموظف",
        "login.employee.subtitle":  "سجل الدخول لإدارة عمليات الغسيل",
        "login.client.title":       "تتبع سيارتك",
        "login.client.subtitle":    "أدخل الرمز الخاص الذي وصلك عبر واتساب",
        "login.admin.title":        "دخول المدير",
        "login.admin.subtitle":     "سجل الدخول لعرض الإحصائيات وإدارة الموظفين",
        "login.field.username":     "اسم المستخدم",
        "login.field.password":     "كلمة المرور",
        "login.field.code":         "رمز التتبع",
        "login.btn.login":          "دخول",
        "login.btn.track":          "تتبع",
        "login.hint":               "البيانات الافتراضية :",
        "login.back":               "→ العودة إلى الرئيسية",

        "emp.dash.title":           "لوحة تحكم الموظف",
        "emp.dash.subtitle":        "سجل سيارات جديدة وقم بتحديث حالة الغسيل",
        "emp.register.title":       "تسجيل سيارة جديدة",
        "emp.field.car_type":       "نوع السيارة",
        "emp.field.phone":          "رقم الهاتف",
        "emp.field.wash_type":      "نوع الغسيل",
        "emp.field.price":          "السعر",
        "emp.opt.select":           "-- اختر --",
        "emp.opt.small":            "صغيرة",
        "emp.opt.large":            "كبيرة",
        "emp.btn.register":         "تسجيل وإرسال عبر واتساب",
        "emp.cars.title":           "جميع السيارات",
        "emp.empty":                "لا توجد سيارات مسجلة بعد. أضف الأولى أعلاه.",
        "emp.send.code":            "إرسال رمز التتبع عبر واتساب",
        "emp.send.reminder":        "إرسال تذكير",

        "th.code":                  "الرمز",
        "th.car":                   "السيارة",
        "th.phone":                 "الهاتف",
        "th.wash":                  "الغسيل",
        "th.price":                 "السعر",
        "th.status":                "الحالة",
        "th.date":                  "التاريخ",
        "th.actions":               "الإجراءات",
        "th.id":                    "المعرف",
        "th.username":              "المستخدم",
        "th.action":                "إجراء",
        "th.num":                   "#",

        "status.started":           "بدأ",
        "status.in_progress":       "قيد التنفيذ",
        "status.finished":          "منتهي",

        "admin.title":              "لوحة تحكم المدير",
        "admin.subtitle":           "نظرة عامة على الإيرادات والعمليات والموظفين",
        "admin.stat.total":         "إجمالي السيارات",
        "admin.stat.daily":         "إيرادات اليوم",
        "admin.stat.weekly":        "إيرادات الأسبوع",
        "admin.stat.monthly":       "إيرادات الشهر",
        "admin.status.title":       "توزيع الحالات",
        "admin.status.started":     "بدأ :",
        "admin.status.progress":    "قيد التنفيذ :",
        "admin.status.finished":    "منتهي :",
        "admin.employees.title":    "الموظفون",
        "admin.create.title":       "إنشاء موظف جديد",
        "admin.create.username":    "اسم المستخدم",
        "admin.create.password":    "كلمة المرور",
        "admin.create.btn":         "إنشاء الموظف",
        "admin.history.title":      "سجل جميع العمليات",
        "admin.empty":              "لا توجد عمليات بعد.",
        "admin.whatsapp.title":     "إشعارات واتساب الأخيرة",
        "admin.whatsapp.empty":     "لم يتم إرسال أي رسالة بعد.",
        "admin.whatsapp.open":      "فتح",
        "admin.default":            "افتراضي",
        "admin.delete":             "حذف",

        "track.title":              "تتبع سيارتك",
        "track.code":               "الرمز",
        "track.step1":              "بدأ",
        "track.step1.desc":         "تم تسجيل السيارة",
        "track.step2":              "قيد التنفيذ",
        "track.step2.desc":         "الغسيل قيد التنفيذ",
        "track.step3":              "منتهي",
        "track.step3.desc":         "جاهزة للاستلام",
        "track.banner.started":     "تم تسجيل سيارتك. سيبدأ الغسيل قريباً.",
        "track.banner.progress":    "سيارتك قيد الغسيل الآن.",
        "track.banner.finished":    "سيارتك جاهزة. يمكنك القدوم لاستلامها.",
        "track.refresh":            "يتم تحديث هذه الصفحة تلقائياً كل 10 ثوانٍ.",
        "track.back":               "→ تتبع سيارة أخرى",
        "track.label.car":          "السيارة :",
        "track.label.wash":         "الغسيل :",
        "track.label.price":        "السعر :",

        "common.confirm.delete":    "حذف الموظف",
        "common.confirm.logout":    "هل تريد فعلاً تسجيل الخروج ؟",
        "common.theme.toggle":      "تغيير المظهر",
        "common.lang.toggle":       "Français"
    }
};

/* ---------- Language ---------- */
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

    // Translate status badges (text comes from server in English: Started / In Progress / Finished)
    const statusMap = {
        "Started":     dict["status.started"],
        "In Progress": dict["status.in_progress"],
        "Finished":    dict["status.finished"]
    };
    document.querySelectorAll('[data-status-text]').forEach(el => {
        const original = el.getAttribute('data-status-text');
        if (statusMap[original]) el.textContent = statusMap[original];
    });

    // Translate <select> option labels (the value attribute stays in English for the backend)
    document.querySelectorAll('option[data-i18n-status]').forEach(opt => {
        const original = opt.getAttribute('data-i18n-status');
        if (statusMap[original]) opt.textContent = statusMap[original];
    });

    // Update language toggle button label (shows the OTHER language)
    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) langBtn.textContent = dict["common.lang.toggle"];
}

/* ---------- Theme ---------- */
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

function toggleLang() {
    setLang(getLang() === 'fr' ? 'ar' : 'fr');
}

/* ---------- Apply on load (as early as possible) ---------- */
(function earlyInit() {
    document.documentElement.setAttribute('data-theme', getTheme());
    const lang = getLang();
    document.documentElement.setAttribute('lang', lang);
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    // Sync cookie with localStorage so the backend gets it on every request
    document.cookie = 'mnojo_lang=' + lang + '; path=/; max-age=31536000; SameSite=Lax';
})();

document.addEventListener('DOMContentLoaded', () => {

    // Apply translations now that DOM is ready
    applyLang(getLang());

    // Wire toggle buttons
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

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
