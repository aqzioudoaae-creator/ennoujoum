# 📚 Explication COMPLÈTE de database.py

> Ce fichier gère la **base de données** (lieu de stockage de toutes les informations du site)

---

## 🎯 Objectif du fichier

Le fichier `database.py` fait 3 choses principales:

1. **Connecte** le site à la base de données
2. **Crée** les tables (endroits où on stocke les données)
3. **Prépare** tout au démarrage du site

---

## 📋 PARTIE 1 - Imports et Configuration

```python
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
USE_POSTGRES = bool(DATABASE_URL)
```

### Explication:

**`import os`** → Permet de lire les variables d'environnement (comme une clé secrète)

**`DATABASE_URL`** → Adresse de la base de données
- Si tu es sur **Heroku** (production) → Utilise **PostgreSQL** (serveur distant)
- Si tu es sur **ton ordinateur** → Utilise **SQLite** (fichier local `mnojo.db`)

**`USE_POSTGRES`** → Variable booléenne (`True` ou `False`)
- `True` = Tu utilises PostgreSQL (en production)
- `False` = Tu utilises SQLite (en local)

---

## 🔧 PARTIE 2 - Classe PgConnectionWrapper

```python
class PgConnectionWrapper:
    """Makes psycopg2 connection behave like sqlite3 connection."""
    
    def __init__(self, raw_conn):
        import psycopg2.extras
        self._conn = raw_conn
        self._cur = raw_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
```

### Explication:

C'est une **classe adapter** (traducteur).

**Pourquoi?** SQLite et PostgreSQL ne parlent pas le même "langage":

| SQLite | PostgreSQL |
|--------|-----------|
| Utilise `?` pour paramètres | Utilise `%s` pour paramètres |
| Code différent | Code différent |

**La classe convertit PostgreSQL en langage SQLite** pour que le code app.py marche dans les 2 cas.

#### Méthodes principales:

```python
def execute(self, sql, params=()):
    sql = sql.replace("?", "%s")  # Convertir ? en %s
    self._cur.execute(sql, params)
    return self._cur
```
→ Exécute une requête SQL

```python
def commit(self):
    self._conn.commit()
```
→ **Enregistre** les changements (très important!)

```python
def close(self):
    self._conn.close()
```
→ **Ferme** la connexion

---

## 🌐 PARTIE 3 - Fonction get_db_connection()

```python
def get_db_connection():
    if USE_POSTGRES:
        import psycopg2
        raw_conn = psycopg2.connect(DATABASE_URL)
        return PgConnectionWrapper(raw_conn)
    else:
        import sqlite3
        conn = sqlite3.connect("mnojo.db")
        conn.row_factory = sqlite3.Row
        return conn
```

### Explication:

Cette fonction **ouvre** une connexion à la base de données.

**Si PostgreSQL** (production):
```python
1. Importe le driver psycopg2
2. Se connecte avec DATABASE_URL
3. Enveloppe dans PgConnectionWrapper
```

**Si SQLite** (local):
```python
1. Importe sqlite3
2. Se connecte au fichier mnojo.db (créé localement)
3. Configure row_factory (permet de lire les résultats comme des dictionnaires)
```

**Utilisation dans app.py:**
```python
conn = get_db_connection()  # Ouvre connexion
conn.execute("SELECT ...")  # Exécute une requête
conn.close()               # Ferme connexion
```

---

## 📊 PARTIE 4 - Fonction init_db() - TABLES CRÉÉES

Cette fonction **crée les 4 tables** nécessaires au site.

### TABLE 1: **cars** (Voitures)

```python
CREATE TABLE IF NOT EXISTS cars (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    code      TEXT    UNIQUE NOT NULL,
    car_type  TEXT    NOT NULL,
    phone     TEXT    NOT NULL,
    wash_type TEXT    NOT NULL,
    price     INTEGER NOT NULL,
    status    TEXT    NOT NULL DEFAULT 'Started',
    date      TEXT    NOT NULL
)
```

**Explication des colonnes:**

| Colonne | Type | Signification |
|---------|------|---------------|
| `id` | INTEGER | Numéro unique (1, 2, 3...) |
| `code` | TEXT UNIQUE | Code 3 chiffres (360, 741...) - UNIQUE = pas 2 codes pareils |
| `car_type` | TEXT | Type voiture (Dacia, BMW, etc) |
| `phone` | TEXT | Numéro client |
| `wash_type` | TEXT | Type lavage (Normal, Pro, Pro Max) |
| `price` | INTEGER | Prix en DH (40, 70, 300) |
| `status` | TEXT | État (Started, In Progress, Finished) |
| `date` | TEXT | Date d'enregistrement |

**Exemple de données:**
```
id=1, code=360, car_type=Dacia, phone=212612345678, wash_type=Pro, price=70, status=Started, date=2025-05-11
```

---

### TABLE 2: **employees** (Employés)

```python
CREATE TABLE IF NOT EXISTS employees (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    UNIQUE NOT NULL,
    password TEXT    NOT NULL
)
```

**Explication:**
- `id` → Numéro unique employé
- `username` → Nom utilisateur (emp1, emp2...)
- `password` → Mot de passe (hashé par sécurité)

**Exemple:**
```
id=1, username=emp1, password=hashed_password_123
```

---

### TABLE 3: **managers** (Managers/Admin)

```python
CREATE TABLE IF NOT EXISTS managers (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    username          TEXT    UNIQUE NOT NULL,
    password          TEXT    NOT NULL,
    status            TEXT    NOT NULL DEFAULT 'pending',
    date              TEXT,
    security_question TEXT,
    security_answer   TEXT
)
```

**Explication:**
- `id` → Numéro unique manager
- `username` → Nom utilisateur (admin1, admin2...)
- `password` → Mot de passe
- `status` → État (pending = en attente, approved = approuvé)
- `security_question` → Question pour reset mot de passe
- `security_answer` → Réponse à la question

**Exemple:**
```
id=1, username=admin1, password=hashed, status=approved, 
security_question=Quelle est ta couleur?, security_answer=bleu
```

---

### TABLE 4: **whatsapp_log** (Messages WhatsApp)

```python
CREATE TABLE IF NOT EXISTS whatsapp_log (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    phone   TEXT NOT NULL,
    message TEXT NOT NULL,
    time    TEXT NOT NULL,
    code    TEXT,
    link    TEXT
)
```

**Explication:**
- `id` → Numéro unique message
- `phone` → Téléphone client
- `message` → Contenu du message
- `time` → Heure d'envoi
- `code` → Code voiture (360)
- `link` → Lien WhatsApp clickable

**Exemple:**
```
id=1, phone=212612345678, message="Votre voiture est prête!", 
time=2025-05-11 14:30, code=360, link=https://wa.me/...
```

---

## 🔄 Différences PostgreSQL vs SQLite

### Pour les clés auto-incrémentées:

**PostgreSQL:**
```python
id SERIAL PRIMARY KEY
```

**SQLite:**
```python
id INTEGER PRIMARY KEY AUTOINCREMENT
```

→ **Même résultat:** Les `id` s'incrémentent automatiquement (1, 2, 3...)

---

## 🚀 Comment modifier pour voir les changements sur le site?

### ✅ EXEMPLE 1: Ajouter une nouvelle colonne (colonne age)

**Étape 1:** Modifier database.py

```python
# Dans TABLE cars:
CREATE TABLE IF NOT EXISTS cars (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    code      TEXT    UNIQUE NOT NULL,
    car_type  TEXT    NOT NULL,
    phone     TEXT    NOT NULL,
    wash_type TEXT    NOT NULL,
    price     INTEGER NOT NULL,
    status    TEXT    NOT NULL DEFAULT 'Started',
    date      TEXT    NOT NULL,
    age       INTEGER  # 🆕 NOUVELLE COLONNE
)
```

**Étape 2:** Mettre à jour app.py pour utiliser cette colonne

```python
# Dans la route d'enregistrement voiture:
age = request.form.get('age')
conn.execute(
    "INSERT INTO cars (..., age) VALUES (..., ?)",
    (..., age)
)
```

**Étape 3:** Ajouter l'input dans le formulaire HTML

```html
<!-- Dans templates/_emp_register.html -->
<div class="form-group">
    <label>Âge propriétaire</label>
    <input type="number" name="age" required>
</div>
```

✅ **Résultat sur ennoujoum.com:** Un champ "Âge" apparaît dans le formulaire!

---

### ✅ EXEMPLE 2: Changer un nom de colonne

**Avant:**
```python
car_type TEXT
```

**Après:**
```python
vehicle_type TEXT  # Nom changé
```

Puis dans app.py:
```python
# Avant: car.car_type
# Après: car.vehicle_type
```

---

### ✅ EXEMPLE 3: Ajouter une nouvelle table

**Nouveau tableau pour les avis clients:**

```python
def init_db():
    conn = get_db_connection()
    
    # ...autres tables...
    
    # 🆕 NOUVELLE TABLE:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id    INTEGER NOT NULL,
            rating    INTEGER NOT NULL,
            comment   TEXT,
            date      TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
```

Puis dans app.py, créer une route pour afficher les avis:

```python
@app.route('/reviews/<car_id>')
def get_reviews(car_id):
    conn = get_db_connection()
    reviews = conn.execute(
        "SELECT * FROM reviews WHERE car_id = ?", (car_id,)
    ).fetchall()
    conn.close()
    return render_template('reviews.html', reviews=reviews)
```

✅ **Résultat sur ennoujoum.com:** Page affichant les avis!

---

## 📝 Points clés à retenir

1. **database.py crée les "armoires" (tables)** où on stocke les données
2. **Chaque table = collection de données** (voitures, employés, etc)
3. **Chaque colonne = type d'info** (code, phone, price...)
4. **Les modifications s'affichent immédiatement** sur le site (si tu recharge la page)
5. **PostgreSQL vs SQLite** = même chose, syntaxe légèrement différente

---

## 🎓 Pour l'examen

Le prof te demandera probablement:

✅ **Ajouter une colonne** → Modifie `CREATE TABLE` dans `init_db()`

✅ **Ajouter une table** → Ajoute un `conn.execute(...)` pour nouvelle table

✅ **Changer un nom de colonne** → Modifie dans database.py ET app.py

✅ **Modifier une contrainte** → Par exemple `UNIQUE` ou `NOT NULL`

**Important:** 
- Après modification de database.py, **supprime le fichier `mnojo.db`** (sur local) pour que la nouvelle structure soit créée
- Sur Heroku, les changements se font automatiquement

---

## 🔍 Structure résumée

```
database.py
├── Imports & Configuration
├── Classe PgConnectionWrapper (adapter PostgreSQL ↔ SQLite)
├── Fonction get_db_connection() (ouvre connexion)
└── Fonction init_db() (crée 4 tables)
    ├── Table: cars (voitures)
    ├── Table: employees (employés)
    ├── Table: managers (managers)
    └── Table: whatsapp_log (messages)
```

---

**Besoin de clarifications? Demande-moi!** 🚀
