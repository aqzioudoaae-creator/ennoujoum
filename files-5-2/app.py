"""
=============================================================
 MNOJO - Car Wash Management System
 Main Flask Application
=============================================================
 This application manages a car wash business with three roles:
   - Employee: Register cars and update wash status
   - Client:   Track their car using a unique code
   - Admin:    View statistics, manage employees, see history

 Features:
   - SQLite database (auto initialized)
   - Simulated WhatsApp notifications
   - Daily / Weekly / Monthly revenue stats
   - Auto-generated unique tracking codes
=============================================================
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, get_flashed_messages
import sqlite3
import random
import os
import urllib.parse
from datetime import datetime, timedelta, timezone


# Morocco timezone is UTC+1 year-round (no DST since 2018, except briefly
# during Ramadan when the country temporarily switches to UTC+0).
# Using a fixed +1 offset matches the local clock for the vast majority of the year.
LOCAL_TZ = timezone(timedelta(hours=1))


def now_local():
    """Return the current datetime in the local (Morocco) timezone."""
    return datetime.now(LOCAL_TZ)
from database import init_db, get_db_connection

# -------------------------------------------------------------
# Flask App Configuration
# -------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "mnojo_super_secret_key_2025"   # used for sessions / flash messages

# Pricing rules (DH = Moroccan Dirham)
PRICES = {
    "Normal": 40,
    "Pro": 70,
    "Pro Max": 300
}

# In-memory log of "WhatsApp" messages (simulation only)
# Each message: {phone, message, time, code}

# Initialize the database at import time so it works under gunicorn too
# (gunicorn imports this module but does NOT execute the __main__ block).
init_db()


# -------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------
def generate_unique_code():
    """
    Generate a unique 3-digit tracking code.
    Keeps generating until one not used in the DB is found.
    """
    conn = get_db_connection()
    while True:
        code = str(random.randint(100, 999))
        existing = conn.execute(
            "SELECT id FROM cars WHERE code = ?", (code,)
        ).fetchone()
        if not existing:
            conn.close()
            return code


def build_whatsapp_link(phone, message):
    """Build a real WhatsApp click-to-chat link (wa.me)."""
    clean_phone = "".join(ch for ch in str(phone) if ch.isdigit())
    if clean_phone.startswith("0"):
        clean_phone = "212" + clean_phone[1:]
    encoded_msg = urllib.parse.quote(message)
    return "https://wa.me/" + clean_phone + "?text=" + encoded_msg


def send_whatsapp(phone, message, code=None):
    """
    Build a real WhatsApp click-to-chat link and save to PostgreSQL.
    """
    entry = {
        "phone":   phone,
        "message": message,
        "time":    now_local().strftime("%Y-%m-%d %H:%M:%S"),
        "code":    code,
        "link":    build_whatsapp_link(phone, message),
    }
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO whatsapp_log (phone, message, time, code, link) VALUES (?, ?, ?, ?, ?)",
            (entry["phone"], entry["message"], entry["time"], entry["code"], entry["link"])
        )
        conn.commit()
        conn.close()
    except Exception:
        pass  # never crash the main flow because of logging
    return entry


def get_whatsapp_log(limit=15):
    """Fetch the last N WhatsApp messages from the database."""
    try:
        conn = get_db_connection()
        rows = conn.execute(
            "SELECT * FROM whatsapp_log ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


# -------------------------------------------------------------
# WhatsApp messages (FR / AR)
# -------------------------------------------------------------
SITE_URL = "https://ennoujoum.com"

WA_MESSAGES = {
    "fr": {
        "registered":  "Bonjour, votre voiture a bien été enregistrée. Votre code de suivi est : {code}.\nSuivez votre voiture ici : " + SITE_URL,
        "ready":       "Bonjour, votre voiture est prête. Vous pouvez venir la récupérer. Merci.\n" + SITE_URL,
        "reminder":    "Bonjour, petit rappel : votre voiture (code {code}) vous attend toujours au lavage. Merci de venir la récupérer.\n" + SITE_URL,
        "tracking":    "Votre code de suivi est : {code}\nSuivez votre voiture ici : " + SITE_URL,
    },
    "ar": {
        "registered":  "مرحباً، تم تسجيل سيارتكم بنجاح. رمز التتبع الخاص بكم هو : {code}.\nتابعوا سيارتكم هنا : " + SITE_URL,
        "ready":       "مرحباً، سيارتكم جاهزة. يمكنكم القدوم لاستلامها. شكراً لكم.\n" + SITE_URL,
        "reminder":    "مرحباً، تذكير بسيط : سيارتكم (الرمز {code}) لا تزال في انتظاركم بمحطة الغسيل. نرجو القدوم لاستلامها.\n" + SITE_URL,
        "tracking":    "رمز التتبع الخاص بكم هو : {code}\nتابعوا سيارتكم هنا : " + SITE_URL,
    }
}

def get_lang():
    """Read the visitor's preferred language from the cookie set by main.js.
    Defaults to 'fr' if missing or invalid."""
    lang = request.cookies.get("mnojo_lang", "fr")
    return lang if lang in ("fr", "ar") else "fr"

def wa_text(key, **kwargs):
    """Return a WhatsApp message in the visitor's current language."""
    lang = get_lang()
    template = WA_MESSAGES.get(lang, WA_MESSAGES["fr"]).get(key, "")
    return template.format(**kwargs)


def login_required(role):
    """
    Decorator factory: require a user to be logged in with given role.
    role can be 'admin', 'employee', or 'client'.
    """
    from functools import wraps

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get("role") != role:
                flash("Please log in first.", "error")
                return redirect(url_for("home"))
            return f(*args, **kwargs)
        return wrapper
    return decorator


# =============================================================
#                 PUBLIC / HOME ROUTES
# =============================================================
@app.route("/")
def home():
    """Landing page with three login choices."""
    return render_template("index.html")


# =============================================================
#                 EMPLOYEE ROUTES
# =============================================================
@app.route("/employee/login", methods=["GET", "POST"])
def employee_login():
    """Employee login page."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        conn = get_db_connection()
        emp = conn.execute(
            "SELECT * FROM employees WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if emp:
            session["role"] = "employee"
            session["user_id"] = emp["id"]
            session["username"] = emp["username"]
            flash(f"Welcome back, {emp['username']}!", "success")
            return redirect(url_for("employee_dashboard"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("employee_login.html")


@app.route("/employee/dashboard")
@login_required("employee")
def employee_dashboard():
    """Main employee page: register a car + see active cars."""
    conn = get_db_connection()
    cars = conn.execute(
        "SELECT * FROM cars ORDER BY id DESC"
    ).fetchall()
    conn.close()

    wa_flashes = get_flashed_messages(category_filter=["whatsapp"])
    pending_whatsapp = wa_flashes[-1] if wa_flashes else None

    return render_template(
        "employee_dashboard.html",
        cars=cars,
        prices=PRICES,
        username=session.get("username"),
        pending_whatsapp=pending_whatsapp,
        build_whatsapp_link=build_whatsapp_link,
        wa_text=wa_text,
        whatsapp_log=get_whatsapp_log(15),
    )


@app.route("/employee/register_car", methods=["POST"])
@login_required("employee")
def register_car():
    """Register a new car wash entry."""
    car_type   = request.form.get("car_type")
    phone      = request.form.get("phone", "").strip()
    wash_type  = request.form.get("wash_type")

    # -------- form validation --------
    if not car_type or not phone or not wash_type:
        flash("All fields are required.", "error")
        return redirect(url_for("employee_dashboard"))
    if wash_type not in PRICES:
        flash("Invalid wash type.", "error")
        return redirect(url_for("employee_dashboard"))
    if not phone.replace("+", "").replace(" ", "").isdigit():
        flash("Phone number must contain only digits.", "error")
        return redirect(url_for("employee_dashboard"))

    price = PRICES[wash_type]
    code  = generate_unique_code()
    date  = now_local().strftime("%Y-%m-%d %H:%M:%S")

    # -------- save in DB --------
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO cars (code, car_type, phone, wash_type, price, status, date)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (code, car_type, phone, wash_type, price, "Started", date)
    )
    conn.commit()
    conn.close()

    # -------- create real WhatsApp link --------
    wa_entry = send_whatsapp(
        phone,
        wa_text("registered", code=code),
        code=code
    )
    flash(wa_entry["link"], "whatsapp")

    flash("Car registered successfully! Tracking code: " + code, "success")
    return redirect(url_for("employee_dashboard"))


@app.route("/employee/update_status/<int:car_id>", methods=["POST"])
@login_required("employee")
def update_status(car_id):
    """Update wash status (Started -> In Progress -> Finished)."""
    new_status = request.form.get("status")
    if new_status not in ("Started", "In Progress", "Finished"):
        flash("Invalid status.", "error")
        return redirect(url_for("employee_dashboard"))

    conn = get_db_connection()
    car = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    if not car:
        conn.close()
        flash("Car not found.", "error")
        return redirect(url_for("employee_dashboard"))

    conn.execute("UPDATE cars SET status = ? WHERE id = ?", (new_status, car_id))
    conn.commit()
    conn.close()

    # If status becomes "Finished" -> create pickup message link
    if new_status == "Finished":
        wa_entry = send_whatsapp(
            car["phone"],
            wa_text("ready"),
            code=car["code"]
        )
        flash(wa_entry["link"], "whatsapp")

    flash(f"Status updated to '{new_status}'.", "success")
    return redirect(url_for("employee_dashboard"))


@app.route("/employee/send_reminder/<int:car_id>", methods=["POST"])
@login_required("employee")
def send_reminder(car_id):
    """Send reminder if client didn't pick the car."""
    conn = get_db_connection()
    car = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    conn.close()
    if not car:
        flash("Car not found.", "error")
        return redirect(url_for("employee_dashboard"))

    wa_entry = send_whatsapp(
        car["phone"],
        wa_text("reminder", code=car["code"]),
        code=car["code"]
    )
    flash(wa_entry["link"], "whatsapp")
    flash("Reminder sent successfully.", "success")
    return redirect(url_for("employee_dashboard"))


@app.route("/employee/update_car/<int:car_id>", methods=["POST"])
@login_required("employee")
def employee_update_car(car_id):
    """Employee edits a car (car_type, phone, wash_type, status).
    Price is recomputed from the wash_type."""
    car_type   = request.form.get("car_type", "").strip()
    phone      = request.form.get("phone", "").strip()
    wash_type  = request.form.get("wash_type", "").strip()
    new_status = request.form.get("status", "").strip()

    if not car_type or not phone or not wash_type or not new_status:
        flash("All fields are required.", "error")
        return redirect(url_for("employee_dashboard"))
    if wash_type not in PRICES:
        flash("Invalid wash type.", "error")
        return redirect(url_for("employee_dashboard"))
    if new_status not in ("Started", "In Progress", "Finished"):
        flash("Invalid status.", "error")
        return redirect(url_for("employee_dashboard"))
    if not phone.replace("+", "").replace(" ", "").isdigit():
        flash("Phone number must contain only digits.", "error")
        return redirect(url_for("employee_dashboard"))

    price = PRICES[wash_type]

    conn = get_db_connection()
    car  = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    if not car:
        conn.close()
        flash("Car not found.", "error")
        return redirect(url_for("employee_dashboard"))

    old_status = car["status"]
    conn.execute(
        """UPDATE cars
              SET car_type = ?, phone = ?, wash_type = ?, price = ?, status = ?
            WHERE id = ?""",
        (car_type, phone, wash_type, price, new_status, car_id)
    )
    conn.commit()
    conn.close()

    # If the status just became "Finished", trigger the pickup WhatsApp
    if new_status == "Finished" and old_status != "Finished":
        wa_entry = send_whatsapp(
            phone,
            wa_text("ready"),
            code=car["code"]
        )
        flash(wa_entry["link"], "whatsapp")

    flash("Car updated successfully.", "success")
    return redirect(url_for("employee_dashboard"))


@app.route("/employee/delete_car/<int:car_id>", methods=["POST"])
@login_required("employee")
def employee_delete_car(car_id):
    """Employee deletes a car record."""
    conn = get_db_connection()
    car  = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    if not car:
        conn.close()
        flash("Car not found.", "error")
        return redirect(url_for("employee_dashboard"))

    conn.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    conn.close()
    flash(f"Car #{car['code']} deleted successfully.", "success")
    return redirect(url_for("employee_dashboard"))


# =============================================================
#                 CLIENT ROUTES
# =============================================================
@app.route("/client", methods=["GET", "POST"])
def client_login():
    """Client enters their tracking code."""
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        if not code:
            flash("Please enter your code.", "error")
            return redirect(url_for("client_login"))
        return redirect(url_for("client_track", code=code))
    return render_template("client_login.html")


@app.route("/client/track/<code>")
def client_track(code):
    """Show timeline of the car wash for the given code."""
    conn = get_db_connection()
    car = conn.execute("SELECT * FROM cars WHERE code = ?", (code,)).fetchone()
    conn.close()

    if not car:
        flash(f"No car found with code {code}.", "error")
        return redirect(url_for("client_login"))

    return render_template("client_track.html", car=car)


# =============================================================
#                 ADMIN ROUTES
# =============================================================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin login. Looks up the manager in DB and checks the account is approved."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        conn = get_db_connection()
        mgr = conn.execute(
            "SELECT * FROM managers WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()

        if mgr:
            if mgr["status"] != "approved":
                flash("Your account is awaiting approval from another manager.", "error")
                return render_template("admin_login.html")
            session["role"] = "admin"
            session["username"] = username
            session["manager_id"] = mgr["id"]
            flash(f"Welcome, {username}!", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid manager credentials.", "error")
    return render_template("admin_login.html")


@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():
    """Manager self-registration.
    - If NO manager exists yet -> the first one is auto-approved.
    - Otherwise -> account is created with status='pending' and must be approved.
    - The manager is REQUIRED to set a security question + answer so they can
      reset their password if they ever forget it.
    """
    if request.method == "POST":
        username          = request.form.get("username", "").strip()
        password          = request.form.get("password", "").strip()
        security_question = request.form.get("security_question", "").strip()
        security_answer   = request.form.get("security_answer", "").strip()

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for("admin_register"))
        if len(password) < 4:
            flash("Password must be at least 4 characters.", "error")
            return redirect(url_for("admin_register"))
        if not security_question or not security_answer:
            flash("A security question and its answer are required (used to reset your password if you forget it).", "error")
            return redirect(url_for("admin_register"))
        if len(security_answer) < 2:
            flash("Security answer is too short.", "error")
            return redirect(url_for("admin_register"))

        conn = get_db_connection()
        existing = conn.execute(
            "SELECT id FROM managers WHERE username = ?", (username,)
        ).fetchone()
        if existing:
            conn.close()
            flash("This username is already taken.", "error")
            return redirect(url_for("admin_register"))

        # First manager is auto-approved
        any_approved = conn.execute(
            "SELECT id FROM managers WHERE status = 'approved' LIMIT 1"
        ).fetchone()
        new_status = "approved" if any_approved is None else "pending"

        date = now_local().strftime("%Y-%m-%d %H:%M:%S")
        # Store the security answer in lowercase to be tolerant of casing
        conn.execute(
            """INSERT INTO managers
                  (username, password, status, date, security_question, security_answer)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (username, password, new_status, date,
             security_question, security_answer.lower())
        )
        conn.commit()
        conn.close()

        if new_status == "approved":
            flash("Account created and approved automatically (first manager). You can log in now.", "success")
        else:
            flash("Account created. Waiting for an existing manager to approve it.", "success")
        return redirect(url_for("admin_login"))

    return render_template("admin_register.html")


# =============================================================
#         ADMIN — FORGOT / RESET PASSWORD
# =============================================================
@app.route("/admin/forgot_password", methods=["GET", "POST"])
def admin_forgot_password():
    """Step 1 of password recovery: enter username, get the security question.
    Reserved for managers only — employees use a different flow (the manager
    resets their password directly from the dashboard)."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username:
            flash("Please enter your username.", "error")
            return render_template("admin_forgot.html")

        conn = get_db_connection()
        mgr  = conn.execute(
            "SELECT * FROM managers WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if not mgr:
            # Don't leak whether the username exists — show a generic message
            flash("If this account exists, the next step will appear.", "info")
            return render_template("admin_forgot.html")
        if not mgr["security_question"]:
            flash("This account has no security question on file. Please ask another manager to delete and recreate your account.",
                  "error")
            return render_template("admin_forgot.html")
        if mgr["status"] != "approved":
            flash("This account is not approved yet. Wait for approval before resetting the password.",
                  "error")
            return render_template("admin_forgot.html")

        # Show step 2: the security question + the answer/new-password form
        return render_template(
            "admin_forgot.html",
            step=2,
            username=username,
            security_question=mgr["security_question"]
        )

    return render_template("admin_forgot.html")


@app.route("/admin/reset_password", methods=["POST"])
def admin_reset_password():
    """Step 2 of password recovery: validate the answer, then save the new password."""
    username     = request.form.get("username", "").strip()
    answer       = request.form.get("security_answer", "").strip().lower()
    new_password = request.form.get("new_password", "").strip()

    if not username or not answer or not new_password:
        flash("All fields are required.", "error")
        return redirect(url_for("admin_forgot_password"))
    if len(new_password) < 4:
        flash("New password must be at least 4 characters.", "error")
        return redirect(url_for("admin_forgot_password"))

    conn = get_db_connection()
    mgr  = conn.execute(
        "SELECT * FROM managers WHERE username = ? AND status = 'approved'",
        (username,)
    ).fetchone()

    if not mgr or not mgr["security_answer"]:
        conn.close()
        flash("Unable to reset the password.", "error")
        return redirect(url_for("admin_forgot_password"))

    if answer != mgr["security_answer"]:
        conn.close()
        flash("Wrong answer to the security question.", "error")
        return redirect(url_for("admin_forgot_password"))

    conn.execute(
        "UPDATE managers SET password = ? WHERE id = ?",
        (new_password, mgr["id"])
    )
    conn.commit()
    conn.close()
    flash("Password updated successfully. You can now log in.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin/dashboard")
@login_required("admin")
def admin_dashboard():
    """Admin overview: revenue stats + cars + employees."""
    conn = get_db_connection()
    cars      = conn.execute("SELECT * FROM cars ORDER BY id DESC").fetchall()
    employees = conn.execute("SELECT * FROM employees ORDER BY id ASC").fetchall()
    managers_approved = conn.execute(
        "SELECT * FROM managers WHERE status = 'approved' ORDER BY id ASC"
    ).fetchall()
    managers_pending  = conn.execute(
        "SELECT * FROM managers WHERE status = 'pending'  ORDER BY id ASC"
    ).fetchall()
    conn.close()

    # ------- Calculate revenue stats -------
    today  = now_local().date()
    week_ago  = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    daily_total = weekly_total = monthly_total = 0
    for c in cars:
        # parse stored date
        try:
            car_date = datetime.strptime(c["date"], "%Y-%m-%d %H:%M:%S").date()
        except Exception:
            continue
        if car_date == today:
            daily_total += c["price"]
        if car_date >= week_ago:
            weekly_total += c["price"]
        if car_date >= month_ago:
            monthly_total += c["price"]

    stats = {
        "total_cars":     len(cars),
        "daily_revenue":  daily_total,
        "weekly_revenue": weekly_total,
        "monthly_revenue":monthly_total,
        "finished":       sum(1 for c in cars if c["status"] == "Finished"),
        "in_progress":    sum(1 for c in cars if c["status"] == "In Progress"),
        "started":        sum(1 for c in cars if c["status"] == "Started"),
    }

    # Pending whatsapp link to auto-open (if any flash from this admin)
    wa_flashes = get_flashed_messages(category_filter=["whatsapp"])
    pending_whatsapp = wa_flashes[-1] if wa_flashes else None

    return render_template(
        "admin_dashboard.html",
        cars=cars,
        employees=employees,
        managers_approved=managers_approved,
        managers_pending=managers_pending,
        current_manager_id=session.get("manager_id"),
        stats=stats,
        prices=PRICES,
        pending_whatsapp=pending_whatsapp,
        build_whatsapp_link=build_whatsapp_link,
        wa_text=wa_text,
        whatsapp_log=get_whatsapp_log(15)  # last 15 messages from DB
    )


@app.route("/admin/create_employee", methods=["POST"])
@login_required("admin")
def create_employee():
    """Admin creates a new employee account."""
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not username or not password:
        flash("Username and password are required.", "error")
        return redirect(url_for("admin_dashboard"))

    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM employees WHERE username = ?", (username,)
    ).fetchone()
    if existing:
        conn.close()
        flash("This username already exists.", "error")
        return redirect(url_for("admin_dashboard"))

    conn.execute(
        "INSERT INTO employees (username, password) VALUES (?, ?)",
        (username, password)
    )
    conn.commit()
    conn.close()
    flash(f"Employee '{username}' created successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete_employee/<int:emp_id>", methods=["POST"])
@login_required("admin")
def delete_employee(emp_id):
    """Admin deletes an employee account (cannot delete admin1)."""
    conn = get_db_connection()
    emp = conn.execute("SELECT * FROM employees WHERE id = ?", (emp_id,)).fetchone()
    if emp and emp["username"] != "admin1":
        conn.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()
        flash(f"Employee '{emp['username']}' deleted.", "success")
    else:
        flash("Cannot delete this account.", "error")
    conn.close()
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/update_employee/<int:emp_id>", methods=["POST"])
@login_required("admin")
def admin_update_employee(emp_id):
    """Admin updates an employee password (and optionally username)."""
    new_username = request.form.get("username", "").strip()
    new_password = request.form.get("password", "").strip()

    if not new_password:
        flash("Password cannot be empty.", "error")
        return redirect(url_for("admin_dashboard"))

    conn = get_db_connection()
    emp = conn.execute("SELECT * FROM employees WHERE id = ?", (emp_id,)).fetchone()
    if not emp:
        conn.close()
        flash("Employee not found.", "error")
        return redirect(url_for("admin_dashboard"))

    # Username change is allowed but must stay unique
    if new_username and new_username != emp["username"]:
        existing = conn.execute(
            "SELECT id FROM employees WHERE username = ? AND id != ?",
            (new_username, emp_id)
        ).fetchone()
        if existing:
            conn.close()
            flash("This username is already taken.", "error")
            return redirect(url_for("admin_dashboard"))
        conn.execute(
            "UPDATE employees SET username = ?, password = ? WHERE id = ?",
            (new_username, new_password, emp_id)
        )
    else:
        conn.execute(
            "UPDATE employees SET password = ? WHERE id = ?",
            (new_password, emp_id)
        )

    conn.commit()
    conn.close()
    flash("Employee updated successfully.", "success")
    return redirect(url_for("admin_dashboard"))


# =============================================================
#         ADMIN — FULL CRUD ON CARS
# =============================================================
@app.route("/admin/register_car", methods=["POST"])
@login_required("admin")
def admin_register_car():
    """Admin registers a new car (same logic as employee register_car)."""
    car_type   = request.form.get("car_type")
    phone      = request.form.get("phone", "").strip()
    wash_type  = request.form.get("wash_type")

    if not car_type or not phone or not wash_type:
        flash("All fields are required.", "error")
        return redirect(url_for("admin_dashboard"))
    if wash_type not in PRICES:
        flash("Invalid wash type.", "error")
        return redirect(url_for("admin_dashboard"))
    if not phone.replace("+", "").replace(" ", "").isdigit():
        flash("Phone number must contain only digits.", "error")
        return redirect(url_for("admin_dashboard"))

    code  = generate_unique_code()
    price = PRICES[wash_type]
    date  = now_local().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db_connection()
    conn.execute(
        """INSERT INTO cars (code, car_type, phone, wash_type, price, status, date)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (code, car_type, phone, wash_type, price, "Started", date)
    )
    conn.commit()
    conn.close()

    wa_entry = send_whatsapp(
        phone,
        wa_text("registered", code=code),
        code=code
    )
    flash(wa_entry["link"], "whatsapp")
    flash("Car registered successfully! Tracking code: " + code, "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/update_car/<int:car_id>", methods=["POST"])
@login_required("admin")
def admin_update_car(car_id):
    """Admin edits any field of a car (car_type, phone, wash_type, status).
    Price is recomputed from the wash_type."""
    car_type   = request.form.get("car_type", "").strip()
    phone      = request.form.get("phone", "").strip()
    wash_type  = request.form.get("wash_type", "").strip()
    new_status = request.form.get("status", "").strip()

    if not car_type or not phone or not wash_type or not new_status:
        flash("All fields are required.", "error")
        return redirect(url_for("admin_dashboard"))
    if wash_type not in PRICES:
        flash("Invalid wash type.", "error")
        return redirect(url_for("admin_dashboard"))
    if new_status not in ("Started", "In Progress", "Finished"):
        flash("Invalid status.", "error")
        return redirect(url_for("admin_dashboard"))
    if not phone.replace("+", "").replace(" ", "").isdigit():
        flash("Phone number must contain only digits.", "error")
        return redirect(url_for("admin_dashboard"))

    price = PRICES[wash_type]

    conn = get_db_connection()
    car  = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    if not car:
        conn.close()
        flash("Car not found.", "error")
        return redirect(url_for("admin_dashboard"))

    old_status = car["status"]
    conn.execute(
        """UPDATE cars
              SET car_type = ?, phone = ?, wash_type = ?, price = ?, status = ?
            WHERE id = ?""",
        (car_type, phone, wash_type, price, new_status, car_id)
    )
    conn.commit()
    conn.close()

    # If the status just became "Finished", trigger the pickup WhatsApp
    if new_status == "Finished" and old_status != "Finished":
        wa_entry = send_whatsapp(
            phone,
            wa_text("ready"),
            code=car["code"]
        )
        flash(wa_entry["link"], "whatsapp")

    flash("Car updated successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete_car/<int:car_id>", methods=["POST"])
@login_required("admin")
def admin_delete_car(car_id):
    """Admin deletes a car record."""
    conn = get_db_connection()
    car  = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    if not car:
        conn.close()
        flash("Car not found.", "error")
        return redirect(url_for("admin_dashboard"))

    conn.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    conn.close()
    flash(f"Car #{car['code']} deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/send_reminder/<int:car_id>", methods=["POST"])
@login_required("admin")
def admin_send_reminder(car_id):
    """Admin sends a pickup-reminder WhatsApp to the client."""
    conn = get_db_connection()
    car = conn.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
    conn.close()
    if not car:
        flash("Car not found.", "error")
        return redirect(url_for("admin_dashboard"))

    wa_entry = send_whatsapp(
        car["phone"],
        wa_text("reminder", code=car["code"]),
        code=car["code"]
    )
    flash(wa_entry["link"], "whatsapp")
    flash("Reminder sent successfully.", "success")
    return redirect(url_for("admin_dashboard"))


# =============================================================
#                 LOGOUT
# =============================================================
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    response = redirect(url_for("home"))
    # Force the browser to never cache this redirect,
    # so the navbar always reflects the current session state.
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# =============================================================
#                 OPTIONAL JSON API (live status check)
# =============================================================
@app.route("/api/status/<code>")
def api_status(code):
    """Tiny JSON endpoint used by client_track.html to auto-refresh."""
    conn = get_db_connection()
    car = conn.execute("SELECT * FROM cars WHERE code = ?", (code,)).fetchone()
    conn.close()
    if not car:
        return jsonify({"found": False}), 404
    return jsonify({
        "found":    True,
        "code":     car["code"],
        "status":   car["status"],
        "wash":     car["wash_type"],
        "price":    car["price"]
    })


# =============================================================
#         ADMIN — MANAGER APPROVAL & MANAGEMENT
# =============================================================
@app.route("/admin/approve_manager/<int:manager_id>", methods=["POST"])
@login_required("admin")
def admin_approve_manager(manager_id):
    """Approve a pending manager registration."""
    conn = get_db_connection()
    mgr  = conn.execute("SELECT * FROM managers WHERE id = ?", (manager_id,)).fetchone()
    if not mgr:
        conn.close()
        flash("Manager not found.", "error")
        return redirect(url_for("admin_dashboard"))
    if mgr["status"] == "approved":
        conn.close()
        flash("This manager is already approved.", "info")
        return redirect(url_for("admin_dashboard"))

    conn.execute("UPDATE managers SET status = 'approved' WHERE id = ?", (manager_id,))
    conn.commit()
    conn.close()
    flash(f"Manager '{mgr['username']}' approved.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/reject_manager/<int:manager_id>", methods=["POST"])
@login_required("admin")
def admin_reject_manager(manager_id):
    """Reject (delete) a pending manager registration."""
    conn = get_db_connection()
    mgr  = conn.execute("SELECT * FROM managers WHERE id = ?", (manager_id,)).fetchone()
    if not mgr:
        conn.close()
        flash("Manager not found.", "error")
        return redirect(url_for("admin_dashboard"))
    if mgr["status"] == "approved":
        conn.close()
        flash("Use the delete button to remove an approved manager.", "error")
        return redirect(url_for("admin_dashboard"))

    conn.execute("DELETE FROM managers WHERE id = ?", (manager_id,))
    conn.commit()
    conn.close()
    flash(f"Manager request from '{mgr['username']}' rejected.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete_manager/<int:manager_id>", methods=["POST"])
@login_required("admin")
def admin_delete_manager(manager_id):
    """Remove an approved manager (cannot remove yourself or the last one)."""
    if manager_id == session.get("manager_id"):
        flash("You cannot delete your own account.", "error")
        return redirect(url_for("admin_dashboard"))

    conn = get_db_connection()
    mgr  = conn.execute("SELECT * FROM managers WHERE id = ?", (manager_id,)).fetchone()
    if not mgr:
        conn.close()
        flash("Manager not found.", "error")
        return redirect(url_for("admin_dashboard"))

    other_approved = conn.execute(
        "SELECT id FROM managers WHERE status = 'approved' AND id != ?",
        (manager_id,)
    ).fetchone()
    if mgr["status"] == "approved" and not other_approved:
        conn.close()
        flash("Cannot delete the last approved manager.", "error")
        return redirect(url_for("admin_dashboard"))

    conn.execute("DELETE FROM managers WHERE id = ?", (manager_id,))
    conn.commit()
    conn.close()
    flash(f"Manager '{mgr['username']}' deleted.", "success")
    return redirect(url_for("admin_dashboard"))


# =============================================================
#                 APP ENTRY POINT
# =============================================================
if __name__ == "__main__":
    init_db()
    # NOTE: debug=False to avoid Flask reloader breaking stdout on Windows
    # (which causes OSError [Errno 22] inside print()).
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
