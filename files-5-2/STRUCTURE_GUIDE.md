# 📚 ENNOUJOUM - Guide de Structure du Code

> **Pour l'examen** : Ce guide vous aide à naviguer rapidement dans le code sans modifications

---

## 🗂️ STRUCTURE DU PROJET

```
files-5-2/
├── app.py                    # Application Flask principale
├── database.py              # Gestion base de données
├── Procfile                 # Configuration Heroku
├── requirements.txt         # Dépendances Python
│
├── static/                  # Fichiers statiques (CSS, JS)
│   ├── style-vars.css      # Variables CSS (couleurs, ombres)
│   ├── style-navbar.css    # Styles barre navigation
│   ├── style-home.css      # Styles page accueil
│   ├── style-login.css     # Styles pages connexion
│   ├── style-forms.css     # Styles formulaires
│   ├── style-cards.css     # Styles cartes & dashboards
│   ├── style-tables.css    # Styles tableaux & statuts
│   ├── style-timeline.css  # Styles suivi timeline
│   ├── style-flash.css     # Styles messages notifications
│   ├── style-footer.css    # Styles footer + animations
│   ├── style-toggles.css   # Styles boutons thème/langue
│   │
│   ├── main.js             # Initialisation DOM & événements
│   ├── theme.js            # Gestion light/dark mode
│   ├── language.js         # Gestion multilingue FR/AR
│   ├── search-filter.js    # Filtrage tableaux
│   ├── i18n_fr.js          # Traductions français
│   └── i18n_ar.js          # Traductions arabe
│
└── templates/              # Templates HTML (Jinja2)
    ├── base.html           # Template de base (hérité par tous)
    ├── index.html          # Page accueil (public)
    │
    ├── employee_login.html # Connexion employé
    ├── employee_dashboard.html  # Dashboard employé
    │
    ├── client_login.html   # Connexion client
    ├── client_track.html   # Suivi en temps réel
    │
    ├── admin_login.html    # Connexion manager
    ├── admin_register.html # Inscription manager
    ├── admin_forgot.html   # Reset mot de passe
    ├── admin_dashboard.html    # Dashboard manager
    │
    └── _*.html             # Templates partiels (include)
```

---

## 🎨 FICHIERS CSS - Où modifier les STYLES

| Fichier | Rôle | Modifications possibles |
|---------|------|------------------------|
| **style-vars.css** | Variables globales (couleurs, fonts, shadows) | Couleurs principales, espacements |
| **style-navbar.css** | Barre de navigation | Logo, liens nav, user tag |
| **style-home.css** | Page accueil & login | Hero section, cartes rôles |
| **style-forms.css** | Formulaires | Inputs, labels, boutons |
| **style-cards.css** | Cartes & dashboards | Cartes stat, layouts grilles |
| **style-tables.css** | Tableaux & badges | Tableaux, statuts couleur |
| **style-timeline.css** | Suivi timeline | Étapes, banneau statut |
| **style-flash.css** | Messages notifications | Notifications toast |
| **style-footer.css** | Footer & animations | Animations CSS globales |
| **style-toggles.css** | Boutons thème/langue | Icônes, toggles |

---

## 🔧 FICHIERS JAVASCRIPT - Où modifier la LOGIQUE client

| Fichier | Rôle | Modifications possibles |
|---------|------|------------------------|
| **theme.js** | Light/Dark mode | Logique changement thème |
| **language.js** | Multilingue FR/AR/RTL | Changement langue, RTL |
| **main.js** | Initialisation DOM | Event listeners, validations |
| **search-filter.js** | Filtrage tableaux | Logique filtrage données |
| **i18n_fr.js** | Traductions français | Textes français |
| **i18n_ar.js** | Traductions arabe | Textes arabes |

---

## 📄 FICHIERS HTML - Où modifier les PAGES

### Pages Publiques (sans connexion)
- **index.html** → Page accueil avec 3 rôles (Employee, Client, Manager)

### Employé
- **employee_login.html** → Connexion employé (username + password)
- **employee_dashboard.html** → Dashboard (ajouter voiture + tableau)

### Client
- **client_login.html** → Connexion client (code 3 chiffres)
- **client_track.html** → Suivi en temps réel (timeline + status)

### Manager/Admin
- **admin_login.html** → Connexion manager (username + password)
- **admin_register.html** → Inscription nouveau manager
- **admin_forgot.html** → Reset mot de passe
- **admin_dashboard.html** → Dashboard complet (stats + gestion)

### Template de Base
- **base.html** → Structure HTML commune, navbar, footer

---

## 🐍 FICHIERS PYTHON - Backend (Flask)

| Fichier | Rôle |
|---------|------|
| **app.py** | Routes Flask, logique métier |
| **database.py** | Connexion DB, schéma tables |

### Routes principales dans app.py :
- `@app.route('/')` → Page accueil
- `@app.route('/employee_login', methods=['POST'])` → Connexion employé
- `@app.route('/employee_dashboard')` → Dashboard employé
- `@app.route('/client_login', methods=['POST'])` → Connexion client
- `@app.route('/client_track/<code>')` → Suivi client
- `@app.route('/admin_login', methods=['POST'])` → Connexion admin
- `@app.route('/admin_dashboard')` → Dashboard admin

---

## 🎯 RAPIDE - Modifications courantes pendant l'examen

### ❌ Modifier un texte/label?
→ Cherchez dans **templates/\*.html** ou **static/i18n_fr.js** / **i18n_ar.js**

### ❌ Changer une couleur?
→ Allez dans **static/style-vars.css** (variables CSS comme `--yellow`, `--green`)

### ❌ Ajouter une validation formulaire?
→ Modifiez **app.py** (routes POST) ou **main.js** (client-side)

### ❌ Modifier tableau/dashboard?
→ Cherchez le template partial dans **templates/_\*.html**

### ❌ Ajouter une animation?
→ Modifiez **style-footer.css** (section ANIMATIONS)

### ❌ Changer la mise en page?
→ Modifiez les classes CSS dans le template HTML concerné

---

## 🔑 Sections commentées dans chaque fichier

**TOUS les fichiers CSS, JS, et HTML ont des commentaires de section:**

```
/* ===================================================
   [EMOJI] SECTION: NOM DE LA SECTION
   Description: Ce que ça fait
   Éléments: .class1, .class2, etc.
   =================================================== */
```

**Cherchez ces commentaires pour trouver rapidement la partie à modifier!**

---

## 🚀 À retenir

- ✅ **Commentaires = Navigation facile** - Chaque section est labelisée
- ✅ **Pas de modifications du code** - Seulement des commentaires informatifs
- ✅ **Structure claire** - Frontend (CSS/JS) séparé du Backend (Python)
- ✅ **Multilingue** - Support FR, AR + RTL automatique
- ✅ **Responsive** - Mobile-friendly design

---

**Bonne chance à l'examen! 📚✨**
