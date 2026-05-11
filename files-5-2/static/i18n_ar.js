/* ===================================================
   i18n_ar.js - ARABIC TRANSLATIONS (الترجمات العربية)
   Description: Dictionnaire complet des textes en arabe
   Clés: Identiques à i18n_fr.js
     - page.title.*: عناوين الصفحات
     - nav.*: عناصر التنقل
     - home.*: نصوص الصفحة الرئيسية
     - login.*: نماذج تسجيل الدخول
     - emp.*: لوحات تحكم الموظفين
     - admin.*: لوحات تحكم المدير
     - status.*: حالات الغسيل
     - common.*: نصوص شائعة
   Appelé par: language.js (RTL support automatic)
   =================================================== */
/* =========================================================
   i18n_ar.js — الترجمات العربية
   ========================================================= */
window.I18N_AR = {
    "page.title.home":           "النجوم — غسيل السيارات",
    "page.title.welcome":        "النجوم — مرحباً",
    "page.title.employee_login": "دخول الموظف — النجوم",
    "page.title.client_login":   "زبون — تتبع سيارت",
    "page.title.admin_login":    "دخول المدير — النجوم",
    "page.title.employee_dash":  "لوحة تحكم الموظف — النجوم",
    "page.title.admin_dash":     "لوحة تحكم المدير — النجوم",
    "page.title.tracking":       "التتبع — النجوم",

    "nav.home":                  "الرئيسية",
    "nav.track":                 "تتبع سيارتي",
    "nav.dashboard":             "لوحة التحكم",
    "nav.logout":                "تسجيل الخروج",
    "nav.admin":                 "المدير",

    "footer.text":               "— نظام إدارة غسيل السيارات",

    "home.welcome":              "مرحباً بكم في",
    "home.subtitle":             "إدارة ذكية لغسيل السيارات. لا مزيد من الانتظار في الطابور. سيصلك إشعار عبر واتساب بمجرد أن تصبح سيارتك جاهزة.",
    "home.role.employee":        "موظف",
    "home.role.employee.desc":   "تسجيل السيارات وتحديث حالة الغسيل",
    "home.role.client":          "زبون",
    "home.role.client.desc":     "تتبع سيارتك باستخدام رمزك الخاص",
    "home.role.manager":         "مدير",
    "home.role.manager.desc":    "عرض الإيرادات وإدارة الموظفين",
    "home.btn.login":            "تسجيل الدخول",
    "home.btn.track":            "تتبع",

    "login.employee.title":      "دخول الموظف",
    "login.employee.subtitle":   "سجل الدخول لإدارة عمليات الغسيل",
    "login.client.title":        "تتبع سيارتك",
    "login.client.subtitle":     "أدخل الرمز الخاص الذي وصلك عبر واتساب",
    "login.admin.title":         "دخول المدير",
    "login.admin.subtitle":      "سجل الدخول لعرض الإحصائيات وإدارة الموظفين",
    "login.field.username":      "اسم المستخدم",
    "login.field.password":      "كلمة المرور",
    "login.field.code":          "رمز التتبع",
    "login.btn.login":           "دخول",
    "login.btn.track":           "تتبع",
    "login.hint":                "البيانات الافتراضية :",
    "login.back":                "→ العودة إلى الرئيسية",

    "emp.dash.title":            "لوحة تحكم الموظف",
    "emp.dash.subtitle":         "سجل سيارات جديدة وقم بتحديث حالة الغسيل",
    "emp.register.title":        "تسجيل سيارة جديدة",
    "emp.field.car_type":        "نوع السيارة",
    "emp.field.phone":           "رقم الهاتف",
    "emp.field.wash_type":       "نوع الغسيل",
    "emp.field.price":           "السعر",
    "emp.opt.select":            "-- اختر --",
    "emp.opt.small":             "صغيرة",
    "emp.opt.large":             "كبيرة",
    "emp.btn.register":          "تسجيل وإرسال عبر واتساب",
    "emp.cars.title":            "جميع السيارات",
    "emp.empty":                 "لا توجد سيارات مسجلة بعد. أضف الأولى أعلاه.",
    "emp.send.code":             "إرسال رمز التتبع عبر واتساب",
    "emp.send.reminder":         "إرسال تذكير",

    "th.code":                   "الرمز",
    "th.car":                    "السيارة",
    "th.phone":                  "الهاتف",
    "th.wash":                   "الغسيل",
    "th.price":                  "السعر",
    "th.status":                 "الحالة",
    "th.date":                   "التاريخ",
    "th.actions":                "الإجراءات",
    "th.id":                     "المعرف",
    "th.username":               "المستخدم",
    "th.action":                 "إجراء",
    "th.num":                    "#",

    "status.started":            "بدأ",
    "status.in_progress":        "قيد التنفيذ",
    "status.finished":           "منتهي",

    "admin.title":               "لوحة تحكم المدير",
    "admin.subtitle":            "نظرة عامة على الإيرادات والعمليات والموظفين",
    "admin.stat.total":          "إجمالي السيارات",
    "admin.stat.daily":          "إيرادات اليوم",
    "admin.stat.weekly":         "إيرادات الأسبوع",
    "admin.stat.monthly":        "إيرادات الشهر",
    "admin.status.title":        "توزيع الحالات",
    "admin.status.started":      "بدأ :",
    "admin.status.progress":     "قيد التنفيذ :",
    "admin.status.finished":     "منتهي :",
    "admin.employees.title":     "الموظفون",
    "admin.create.title":        "إنشاء موظف جديد",
    "admin.create.username":     "اسم المستخدم",
    "admin.create.password":     "كلمة المرور",
    "admin.create.btn":          "إنشاء الموظف",
    "admin.history.title":       "سجل جميع العمليات",
    "admin.empty":               "لا توجد عمليات بعد.",
    "admin.whatsapp.title":      "إشعارات واتساب الأخيرة",
    "admin.whatsapp.empty":      "لم يتم إرسال أي رسالة بعد.",
    "admin.whatsapp.open":       "فتح",
    "admin.default":             "افتراضي",
    "admin.delete":              "حذف",
    "admin.edit":                "تعديل",
    "admin.save":                "حفظ",
    "admin.cancel":              "إلغاء",
    "emp.btn.whatsapp":          "واتساب",
    "emp.btn.rappel":            "تذكير",

    "track.title":               "تتبع سيارتك",
    "track.code":                "الرمز",
    "track.step1":               "بدأ",
    "track.step1.desc":          "تم تسجيل السيارة",
    "track.step2":               "قيد التنفيذ",
    "track.step2.desc":          "الغسيل قيد التنفيذ",
    "track.step3":               "منتهي",
    "track.step3.desc":          "جاهزة للاستلام",
    "track.banner.started":      "تم تسجيل سيارتك. سيبدأ الغسيل قريباً.",
    "track.banner.progress":     "سيارتك قيد الغسيل الآن.",
    "track.banner.finished":     "سيارتك جاهزة. يمكنك القدوم لاستلامها.",
    "track.refresh":             "يتم تحديث هذه الصفحة تلقائياً كل 10 ثوانٍ.",
    "track.back":                "→ تتبع سيارة أخرى",
    "track.label.car":           "السيارة :",
    "track.label.wash":          "الغسيل :",
    "track.label.price":         "السعر :",

    "common.confirm.delete":     "حذف الموظف",
    "common.confirm.logout":     "هل تريد فعلاً تسجيل الخروج ؟",
    "common.theme.toggle":       "تغيير المظهر",
    "common.lang.toggle":        "Français"
};
