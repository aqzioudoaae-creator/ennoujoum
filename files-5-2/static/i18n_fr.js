/* ===================================================
   i18n_fr.js - FRENCH TRANSLATIONS (Traductions FR)
   Description: Dictionnaire complet des textes en français
   Clés principales:
     - page.title.*: Titres de pages
     - nav.*: Eléments de navigation
     - home.*: Textes de la page d'accueil
     - login.*: Formulaires de connexion
     - emp.*: Dashboards employés
     - admin.*: Dashboards admin/manager
     - status.*: Statuts de lavage
     - common.*: Textes courants
   Appelé par: language.js (applyLang, setLang, toggleLang)
   =================================================== */
/* =========================================================
   i18n_fr.js — Traductions françaises
   ========================================================= */
window.I18N_FR = {
    "page.title.home":           "Ennojoum — Lavage Auto",
    "page.title.welcome":        "Ennojoum — Bienvenue",
    "page.title.employee_login": "Connexion Employé — Ennojoum",
    "page.title.client_login":   "Client — Suivez votre voiture",
    "page.title.admin_login":    "Connexion Manager — Ennojoum",
    "page.title.employee_dash":  "Tableau de bord Employé — Ennojoum",
    "page.title.admin_dash":     "Tableau de bord Manager — Ennojoum",
    "page.title.tracking":       "Suivi — Ennojoum",

    "nav.home":                  "Accueil",
    "nav.track":                 "Suivre ma voiture",
    "nav.dashboard":             "Tableau de bord",
    "nav.logout":                "Déconnexion",
    "nav.admin":                 "Administrateur",

    "footer.text":               "— Système de gestion de lavage auto",

    "home.welcome":              "Bienvenue chez",
    "home.subtitle":             "Gestion intelligente du lavage auto. Plus d'attente en file. Recevez une notification WhatsApp dès que votre voiture est prête.",
    "home.role.employee":        "Employé",
    "home.role.employee.desc":   "Enregistrer les voitures et mettre à jour leur statut",
    "home.role.client":          "Client",
    "home.role.client.desc":     "Suivez votre voiture grâce à votre code unique",
    "home.role.manager":         "Manager",
    "home.role.manager.desc":    "Consulter les revenus et gérer les employés",
    "home.btn.login":            "Se connecter",
    "home.btn.track":            "Suivre",

    "login.employee.title":      "Connexion Employé",
    "login.employee.subtitle":   "Connectez-vous pour gérer les lavages",
    "login.client.title":        "Suivez votre voiture",
    "login.client.subtitle":     "Entrez le code unique reçu sur WhatsApp",
    "login.admin.title":         "Connexion Manager",
    "login.admin.subtitle":      "Connectez-vous pour consulter les statistiques et gérer les employés",
    "login.field.username":      "Nom d'utilisateur",
    "login.field.password":      "Mot de passe",
    "login.field.code":          "Code de suivi",
    "login.btn.login":           "Connexion",
    "login.btn.track":           "Suivre",
    "login.hint":                "Identifiants par défaut :",
    "login.back":                "← Retour à l'accueil",

    "emp.dash.title":            "Tableau de bord Employé",
    "emp.dash.subtitle":         "Enregistrez de nouvelles voitures et mettez à jour leur statut de lavage",
    "emp.register.title":        "Enregistrer une nouvelle voiture",
    "emp.field.car_type":        "Type de voiture",
    "emp.field.phone":           "Numéro de téléphone",
    "emp.field.wash_type":       "Type de lavage",
    "emp.field.price":           "Prix",
    "emp.opt.select":            "-- Sélectionner --",
    "emp.opt.small":             "Petite",
    "emp.opt.large":             "Grande",
    "emp.btn.register":          "Enregistrer et envoyer WhatsApp",
    "emp.cars.title":            "Toutes les voitures",
    "emp.empty":                 "Aucune voiture enregistrée pour l'instant. Ajoutez la première ci-dessus.",
    "emp.send.code":             "Envoyer le code de suivi sur WhatsApp",
    "emp.send.reminder":         "Envoyer un rappel",

    "th.code":                   "Code",
    "th.car":                    "Voiture",
    "th.phone":                  "Téléphone",
    "th.wash":                   "Lavage",
    "th.price":                  "Prix",
    "th.status":                 "Statut",
    "th.date":                   "Date",
    "th.actions":                "Actions",
    "th.id":                     "ID",
    "th.username":               "Utilisateur",
    "th.action":                 "Action",
    "th.num":                    "#",

    "status.started":            "Commencé",
    "status.in_progress":        "En cours",
    "status.finished":           "Terminé",

    "admin.title":               "Tableau de bord Manager",
    "admin.subtitle":            "Aperçu des revenus, opérations et personnel",
    "admin.stat.total":          "Total voitures",
    "admin.stat.daily":          "Revenu du jour",
    "admin.stat.weekly":         "Revenu hebdo",
    "admin.stat.monthly":        "Revenu mensuel",
    "admin.status.title":        "Répartition des statuts",
    "admin.status.started":      "Commencé :",
    "admin.status.progress":     "En cours :",
    "admin.status.finished":     "Terminé :",
    "admin.employees.title":     "Employés",
    "admin.create.title":        "Créer un nouvel employé",
    "admin.create.username":     "Nom d'utilisateur",
    "admin.create.password":     "Mot de passe",
    "admin.create.btn":          "Créer l'employé",
    "admin.history.title":       "Historique de toutes les opérations",
    "admin.empty":               "Aucune opération pour l'instant.",
    "admin.whatsapp.title":      "Notifications WhatsApp récentes",
    "admin.whatsapp.empty":      "Aucun message envoyé pour l'instant.",
    "admin.whatsapp.open":       "Ouvrir",
    "admin.default":             "par défaut",
    "admin.delete":              "Supprimer",
    "admin.edit":                "Modifier",
    "admin.save":                "Enregistrer",
    "admin.cancel":              "Annuler",
    "emp.btn.whatsapp":          "WhatsApp",
    "emp.btn.rappel":            "Rappel",

    "track.title":               "Suivi de votre voiture",
    "track.code":                "Code",
    "track.step1":               "Commencé",
    "track.step1.desc":          "La voiture a été enregistrée",
    "track.step2":               "En cours",
    "track.step2.desc":          "Lavage en cours",
    "track.step3":               "Terminé",
    "track.step3.desc":          "Prête à être récupérée",
    "track.banner.started":      "Votre voiture est enregistrée. Le lavage va bientôt commencer.",
    "track.banner.progress":     "Votre voiture est en cours de lavage.",
    "track.banner.finished":     "Votre voiture est prête. Vous pouvez venir la récupérer.",
    "track.refresh":             "Cette page se met à jour automatiquement toutes les 10 secondes.",
    "track.back":                "← Suivre une autre voiture",
    "track.label.car":           "Voiture :",
    "track.label.wash":          "Lavage :",
    "track.label.price":         "Prix :",

    "common.confirm.delete":     "Supprimer l'employé",
    "common.confirm.logout":     "Voulez-vous vraiment vous déconnecter ?",
    "common.theme.toggle":       "Changer le thème",
    "common.lang.toggle":        "العربية"
};
