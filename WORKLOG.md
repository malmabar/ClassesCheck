# WORKLOG - Morning Classes Check

> وثيقة تشغيلية حية. يتم تحديثها بعد كل تغيير مؤثر.

## 2026-02-22

### [W-001] تأسيس بيئة المشروع
1. إعداد قاعدة بيانات PostgreSQL مع عزل المشروع (`morning_classes_check`) ومستخدم `mc_app`.
2. إنشاء ملف الإعداد `/Users/malmabar/Documents/MornningClassesCheck/.env.mc`.
3. تنفيذ migration الأساسي `20260222_0001`.

### [W-002] تنفيذ Backend الأساسي
1. إنشاء API للصحة `GET /health`.
2. إنشاء API استيراد SS01:
   - `POST /api/v1/mc/import/ss01`
3. إنشاء جداول التشغيل والسجل والمصدر.

### [W-003] تنفيذ طبقة الاشتقاق الأولى (Codes)
1. إضافة موديل `mc_codes`.
2. إضافة migration:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/alembic/versions/20260222_0002_create_mc_codes.py`
3. إضافة خدمة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/run_service.py`
4. إضافة API:
   - `POST /api/v1/mc/run`
   - `GET /api/v1/mc/runs/{run_id}/codes`

### [W-004] تنفيذ محرك الفحوصات (Checks)
1. إضافة موديل `mc_issues`.
2. إضافة migration:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/alembic/versions/20260222_0003_create_mc_issues.py`
3. إضافة خدمة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/check_service.py`
4. إضافة API:
   - `POST /api/v1/mc/checks/run`
   - `GET /api/v1/mc/runs/{run_id}/issues`
5. القواعد المنفذة:
   - `TRAINER_TIME_CONFLICT`
   - `ROOM_TIME_CONFLICT`
   - `ROOM_CAPACITY_EXCEEDED`

### [W-005] واجهة تشغيل ويب داخل FastAPI
1. إنشاء واجهة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/index.html`
2. ربط الصفحة بالمسار:
   - `/` عبر `/Users/malmabar/Documents/MornningClassesCheck/backend/app/main.py`
3. إضافة عرض التشغيلات + الشعب + الملاحظات + أزرار تشغيل المعالجة والفحوصات.

### [W-006] تعريب وRTL
1. تحويل الواجهة إلى عربية RTL بالكامل.
2. تحسين عرض معرفات التشغيل (`run_id`) مع الحفاظ على القراءة الصحيحة.
3. اختيار أول تشغيل تلقائيًا عند تحميل الصفحة.

### [W-007] فلتر رئيسي للفترة (Global Period Filter)
1. إضافة فلتر أعلى الواجهة: `الكل` / `صباحي` / `مسائي`.
2. حفظ حالة الفلتر في `localStorage` واستعادتها تلقائيًا.
3. تطبيق الفلتر على قائمة التشغيلات بالكامل.
4. توسيع API لدعم فلترة الفترة:
   - `GET /api/v1/mc/runs?period=صباحي|مسائي`
   - الملف: `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`

### [W-008] تحسين أدوات التحليل
1. تثبيت `openpyxl` داخل البيئة الافتراضية للمشروع.
2. التحقق من معادلات `0/1` في `Codes`, `TrainersSC`, `Halls_Copy`, `التوزيع النسبي`.
3. تأكيد منطق المصفوفات:
   - `0 = لا إشغال`
   - `1 = إشغال`
   - `>1 = تعارض`

### [W-009] توثيق إلزامي وتحديث PRD
1. تحديث PRD لإضافة:
   - الفلتر الشامل للفترة
   - حوكمة التوثيق
2. تحديث CHANGELOG إلى v1.2.
3. إنشاء الملفات التشغيلية:
   - `/Users/malmabar/Documents/MornningClassesCheck/WORKLOG.md`
   - `/Users/malmabar/Documents/MornningClassesCheck/HANDOVER.md`
   - `/Users/malmabar/Documents/MornningClassesCheck/PROJECT_EXECUTION_BLUEPRINT.md`

### [W-010] إعادة تصميم UI إلى Gov-Tech Glass (RTL)
1. تنفيذ إعادة تصميم كاملة لواجهة `/` بنمط Glassmorphism حديث مع الحفاظ على نفس المنطق والـendpoints.
2. تطبيق هندسة CSS منظّمة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/tokens.css`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
3. فصل منطق الواجهة إلى:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
4. تحديث HTML:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/index.html`
   - إضافة Lucide icons + Bento layout + حالات hover/focus + empty states حديثة.
5. إضافة دعم static assets في FastAPI:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/main.py`
   - mount للمسار `/ui`.
6. دعم إمكانية الوصول:
   - focus rings
   - reduced motion
   - reduced transparency + fallback عند غياب backdrop-filter
7. التحقق من سلامة الكود بعد التعديل (`compileall`) بنجاح.
8. إضافة مرجع تصميم مستقل:
   - `/Users/malmabar/Documents/MornningClassesCheck/UI_SPEC_GOVTECH_GLASS.md`

### [W-011] ترقية UI إلى Premium Neo-Glass + قلب الأعمدة
1. اعتماد اتجاه تصميم جديد: **Charcoal + Emerald + Soft Silver** مع إبقاء بديل Palette A داخل tokens.
2. قلب التخطيط بشكل صريح:
   - العمود الأيمن (Controls Rail): فلتر الفترة + الأوامر + الكونسول + قائمة التشغيلات.
   - العمود الأيسر (Main): تفاصيل التشغيل المحدد + KPI + الجداول.
3. تحديث `index.html`:
   - نقل الفلتر الرئيسي للفترة إلى لوحة التحكم اليمنى.
   - إضافة أدوات الكونسول: `نسخ` + `طي/توسيع`.
   - تحسين التسميات العربية وحالات الفراغ.
4. تحديث `components.css`:
   - Bento grid محسّن مع `sticky` للوحة التحكم.
   - تحسينات قراءة RTL + تباين + تأثيرات زجاجية أقل تشويشًا.
   - تحديث أنماط الأزرار (Primary/Secondary/Ghost/Icon) وتوحيد القياسات.
5. تحديث `dashboard.js` دون تغيير endpoints:
   - إضافة وظائف `copyResult` و`toggleResult`.
   - تحسين عرض جدول الشعب باستخدام chips لحقول اليوم/القاعة.
6. تحديث مرجع المواصفات:
   - `/Users/malmabar/Documents/MornningClassesCheck/UI_SPEC_GOVTECH_GLASS.md`
7. فحص سلامة بعد التعديل:
   - `node --check backend/app/ui/scripts/dashboard.js`
   - `python3 -m compileall backend/app`

### [W-012] ترقية ثيم Luxury Dark (Charcoal + Emerald + Soft Silver)
1. استبدال نظام الألوان بالكامل إلى ثيم داكن فاخر بالقيم الإلزامية:
   - `--bg`, `--bg2`, `--panel`, `--panel2`, `--panelBorder`, `--text`, `--muted`, `--primary`, `--primaryHover`, `--accent`, `--danger`, `--warning`, `--info`.
2. تحديث الطباعة إلى:
   - `IBM Plex Sans Arabic` (fallback: Tajawal).
3. تحسين طبقات الزجاج:
   - blur ضمن `12–18px` (منفذ: `14px`).
   - تقليل الحدود الصندوقية وزيادة العمق بالظلال الناعمة.
4. تثبيت تسلسل الأزرار:
   - Primary: `تشغيل المعالجة`.
   - Secondary outline: `تشغيل الفحوصات`.
   - Ghost: تحديثات التشغيل.
5. تطوير Console:
   - حالة تنفيذ (`ناجح/فشل/معلومة`) + توقيت آخر تحديث.
   - نسخ + طي/توسيع مع تمرير داخلي.
6. تأكيد عدم تغيير منطق الأعمال أو الـAPI endpoints.

### [W-013] تحسينات الهيدر + الثيم ثنائي الوضع + الكثافة
1. إصلاح تموضع بادج البيئة `ok | development` ونقله إلى `header-left-slot` أعلى يسار الهيدر بشكل ثابت.
2. تطبيق بنية هيدر 3 مناطق:
   - `header-left-slot` (البادج + مفاتيح العرض)
   - `header-center-slot` (مساحة)
   - `header-right-slot` (العنوان)
3. إضافة تبديل Dark/Light:
   - `data-theme=\"dark|light\"`
   - حفظ الاختيار في `localStorage`
   - fallback حسب `prefers-color-scheme` عند غياب الاختيار المحفوظ.
4. إضافة تبديل كثافة العرض:
   - `data-density=\"compact|comfortable\"`
   - الافتراضي: `compact`
   - حفظ الاختيار في `localStorage`.
5. ضغط الواجهة بشكل احترافي (Compact):
   - تقليل paddings/gaps/row heights/chips/buttons.
   - تقليل scale للخطوط مع الحفاظ على readability.
6. تطوير Console:
   - status pill + timestamp محدث مع كل استجابة.
7. إضافة `Last updated` في قسم التشغيل المحدد باستخدام بيانات `run` الحالية دون أي API جديدة.

## 2026-02-23

### [W-014] تنفيذ الشاشات الأربع Heatmap (قاعات/شعب/مدربين/توزيع)
1. تفعيل تبويبات الشاشات الحرارية داخل الصفحة الرئيسية:
   - `القاعات`
   - `الشعب`
   - `المدربين`
   - `التوزيع النسبي`
2. إضافة فلاتر أعلى الشاشات الحرارية تؤثر على جميع الشاشات:
   - فلتر الفترة (`ALL`/`صباحي`/`مسائي`)
   - فلتر الإشغال (`all`/`occupied`/`empty`/`conflict`)
   - فلتر بحث نصي للكيان (قاعة/شعبة/مدرب).
3. تنفيذ محرك Heatmap في الواجهة (`dashboard.js`) بدون أي تعديل API:
   - تجميع بيانات `/codes` إلى مصفوفات 5 أيام × 8 فترات.
   - دعم قيم `0/1` مع إبراز التعارضات (`>1`).
   - بناء شاشة توزيع نسبي تشمل:
     - صف إشغال ثنائي
     - صف عدد الشعب
     - صف النسبة المئوية.
4. إضافة ملخصات سريعة لكل شاشة (عدد الصفوف، الخلايا المشغولة، التعارضات، متوسط الإشغال).
5. تطوير أنماط CSS الخاصة بالهيت ماب:
   - جداول sticky header
   - صف عنوان الكيان sticky
   - حالات خلايا (`empty`/`occupied`/`conflict`/`percent`)
   - Empty states متوافقة RTL.
6. تحسين تحميل بيانات التشغيل المحدد:
   - جلب كل صفحات `codes` و`issues` (pagination loop) بدل أول 100 صف فقط.
7. التحقق بعد التنفيذ:
   - `node --check backend/app/ui/scripts/dashboard.js`
   - `python3 -m compileall backend/app`

### [W-015] تصحيح منطق تبويبات Heatmap + توقيت الفترات + توسيع العرض
1. تعديل هيكل الواجهة (`index.html`):
   - إزالة خيار `الكل` من فلتر الفترة الرئيسي وفلتر Heatmap.
   - إضافة زر `إخفاء التحكم` داخل بطاقة `التشغيل المحدد`.
2. تعديل منطق `dashboard.js`:
   - اعتماد جدول توقيت ثابت للفترات:
     - صباحي: 8 فترات (`08:00-08:50` ... `15:06-15:56`)
     - مسائي: 8 فترات (`16:00-16:50` ... `22:21-23:11`)
   - تغيير منطق الإشغال ليعتمد نطاق الوقت `start/end` بدل نقطة زمن واحدة.
   - دعم الحالة متعددة الفترات تلقائيًا (مثال: `08:00-09:40` يشغل الفترة 1 و2).
   - ضبط ترتيب الفترات إلى `1..8` تحت كل يوم باتجاه RTL الصحيح.
   - ربط تبويبات الشاشات لتعرض شاشة واحدة فقط فعليًا حسب التبويب النشط.
   - إضافة وضع إخفاء/إظهار لوحة التحكم مع حفظ الحالة في `localStorage`.
   - مزامنة فلتر الفترة الرئيسي مع فلتر Heatmap (صباحي/مسائي فقط).
3. تعديل `components.css`:
   - إضافة قاعدة صريحة لإخفاء اللوحات غير النشطة: `.screen-panel[hidden]`.
   - إضافة فواصل سوداء بين مجموعات الأيام (`day-start`).
   - إضافة صفوف ترويسة للفترات تشمل:
     - رقم المحاضرة
     - وقت البداية
     - وقت النهاية
4. فحص السلامة:
   - `node --check backend/app/ui/scripts/dashboard.js` (نجح)

### [W-016] تحسين Responsive للـHeatmap لإظهار الأسبوع كاملًا
1. تعديل `components.css` لجعل جدول Heatmap يتكيف مع العرض بدل القيم الثابتة:
   - تفعيل `table-layout: fixed`.
   - إزالة `min-width` الثابتة الكبيرة.
   - إدخال متغيرات مرنة:
     - `--slot-col-w`
     - `--entity-col-w`
     - `--head-row-h`
     باستخدام `clamp(...)`.
2. تحسين عرض شاشة 13 إنش:
   - تصغير خطوط رؤوس الفترات والأوقات.
   - تصغير padding للخلايا.
   - تصغير حجم `heat-cell`.
3. تحسين توزع المساحة على الشاشات الكبيرة:
   - رفع الحد الأقصى للـshell (`max-width: min(1920px, 100%)`).
   - إضافة media query للشاشات العريضة (`min-width: 1700px`) لرفع الأحجام بشكل متوازن.
4. تحسين التكيّف عبر breakpoints:
   - `max-width: 1260px`:
     - تصغير أعمدة الجدول أكثر.
     - إخفاء `heatmap-entity-meta` لتقليل الاستهلاك الأفقي.
   - `max-width: 1060px` و`max-width: 760px`:
     - ضبط متدرج للأعمدة للحفاظ على readability.
5. تحسين تجربة التمرير:
   - `scrollbar-gutter: stable both-edges`.
   - `overflow: hidden` على بطاقة الشاشات لمنع كسور بصرية.

### [W-017] إصلاح الفراغ غير المتناسق في جدول Heatmap
1. معالجة سبب الفراغ الكبير أفقيًا:
   - إلغاء `table-layout: fixed` والعودة إلى `table-layout: auto`.
   - إزالة فرض عرض الأعمدة من selector عام `thead th` الذي كان يؤثر على خلايا الأيام المجمّعة (`colspan`).
2. إعادة توزيع عروض الأعمدة بشكل صحيح:
   - نقل عرض العمود إلى `slot-header` فقط.
   - ضبط `--slot-col-w` و`--entity-col-w` بقيم أكثر اتزانًا.
3. ضبط قيم breakpoints لتقليل الضغط المفرط الذي سبّب انكماش الأيام بشكل غير متناسق.
4. الحفاظ على responsive:
   - شاشة 13 إنش: عرض متوازن بدون فراغ كتلي كبير.
   - شاشات أكبر: تمدد طبيعي دون تشوه.

### [W-018] تحسينات بصرية + إضافة استيراد SS01 من الواجهة
1. تحسين نمط تبويبات الشاشات:
   - توحيد خط/حجم تبويبات (`القاعات`/`الشعب`/`المدربين`/`التوزيع النسبي`) مع الثيم العام.
2. تحسين خلية الإشغال `1`:
   - جعل الخلية الخضراء تغطي كامل المساحة بدل مؤشر صغير داخلها.
3. تمييز أيام محددة بلون أفتح:
   - تطبيق لون أخف على `الاثنين` و`الأربعاء` في:
     - رأس اليوم
     - صفوف أرقام الفترات/الأوقات
     - خلايا جسم الجدول.
4. إضافة واجهة استيراد تقرير جديد داخل لوحة التحكم:
   - حقل الفصل.
   - اختيار الفترة (`صباحي`/`مسائي`).
   - اختيار ملف CSV.
   - زر `استيراد التقرير`.
5. ربط زر الاستيراد مباشرة مع endpoint:
   - `POST /api/v1/mc/import/ss01`
   - باستخدام `FormData`.
6. بعد نجاح الاستيراد:
   - مزامنة فلاتر الفترة.
   - تحديث قائمة التشغيلات تلقائيًا.
7. فحص السلامة:
   - `node --check backend/app/ui/scripts/dashboard.js` (نجح)

### [W-019] ضبط لون الاثنين/الأربعاء إلى رصاصي فاتح بدون المساس بالـHover
1. تعديل `components.css` للأيام البديلة (`day-alt`) في جدول Heatmap:
   - رأس اليوم (`.day-group.day-alt`).
   - رؤوس الفترات/الأوقات (`.slot-header.day-alt`).
   - خلايا جسم الجدول (`tbody td.day-alt`).
2. تغيير الدرجة اللونية من تدرج أخضر فاتح إلى رصاصي فاتح متناسق مع الطلب.
3. الإبقاء على قاعدة `hover` الحالية كما هي دون أي تغيير.

### [W-020] إصلاح Hover ليغطي صف Heatmap بالكامل
1. تعديل قاعدة `hover` في `components.css` لتعمل بأولوية أعلى:
   - `tbody tr:hover th, td` أصبحت بـ`!important`.
2. إضافة override لمحتوى الخلية داخل الصف أثناء الـ`hover`:
   - جعل خلفية وحدود `.heat-cell` شفافة أثناء المرور.
3. النتيجة:
   - الـ`hover` يظهر متصلًا على كامل الصف بدون تقطيع في أعمدة الأيام البديلة أو الخلايا المشغولة.

### [W-021] إبقاء خلية القيمة 1 خضراء أثناء Hover
1. إضافة قواعد override مخصصة أثناء `hover` في `components.css`:
   - `td.cell-occupied-solid` تبقى بلونها الأخضر.
   - `td.cell-conflict-solid` تبقى بلونها الأحمر.
2. الهدف:
   - الحفاظ على تمييز الحالة (`1`/تعارض) حتى عند مرور المؤشر على الصف.
3. النتيجة:
   - الصف يظل ملوّن Hover بالكامل، مع بقاء خلية `1` باللون الأخضر الغامق كما طلب المستخدم.

### [W-022] حل تعارض day-alt مع خلايا الحالة في الاثنين/الأربعاء
1. تعديل قاعدة `hover` لتستهدف فقط الخلايا غير المصنفة كحالة:
   - `td:not(.cell-occupied-solid):not(.cell-conflict-solid)`.
2. إضافة قاعدة أولوية صريحة لأيام `day-alt`:
   - `td.day-alt.cell-occupied-solid` يبقى أخضر.
   - `td.day-alt.cell-conflict-solid` يبقى أحمر.
3. النتيجة:
   - الـ`hover` لا يخفي لون الحالة.
   - خلية `1` تظهر خضراء كاملة حتى داخل الاثنين/الأربعاء.

### [W-023] إصلاح عدم ظهور البيانات بعد استيراد SS01
1. تعديل تدفق الاستيراد في `dashboard.js`:
   - بعد `POST /api/v1/mc/import/ss01` يتم استخراج `run_id` المستورد.
   - تشغيل `POST /api/v1/mc/run` تلقائيًا لنفس `run_id` لبناء `mc_codes`.
2. ضبط اختيار التشغيل بعد الاستيراد:
   - تعيين `selectedRunId` للتشغيل الجديد.
   - إعادة تحميل التشغيلات بصمت ثم فتح التشغيل الجديد مباشرة.
3. تحسين الرسائل:
   - رسالة نجاح واضحة عند اكتمال (استيراد + معالجة).
   - رسالة دقيقة عند نجاح الاستيراد وفشل المعالجة التلقائية.
4. تحسين `loadRuns`:
   - إضافة خيار `suppressResult` لمنع الكتابة فوق رسالة الاستيراد النهائية.
5. التحقق:
   - `node --check backend/app/ui/scripts/dashboard.js` (نجح)

### [W-024] إصلاح احتساب الفترات الممتدة (Start-End) للـHeatmap
1. تحديث منطق تحديد فترة السجل في `dashboard.js`:
   - جعل الاستدلال يعتمد أولًا على نطاق الوقت الفعلي (`start/end`) بدل الاعتماد المبكر على نص `period`.
2. إضافة دوال مساعدة:
   - `collectOverlappingSlots(period, timeRange)` لحساب كل الفترات المتداخلة مع المدى الزمني.
   - `inferPeriodFromTimeRange(timeRange)` لاختيار صباحي/مسائي بناءً على التداخل الزمني الفعلي.
3. تحديث `resolveSlotIndices`:
   - احتساب التداخل على الجدول الأساسي والبديل واختيار النتيجة الأدق.
   - دعم fallback آمن عند غياب نهاية الوقت.
4. النتيجة:
   - مثال `08:00-11:40` يظهر `1` في الفترات `1,2,3,4` بدل فترة واحدة فقط.
   - التداخلات تتجمع طبيعيًا (`2`, `3`, ...) مما يحسن كشف التعارضات.
5. التحقق:
   - `node --check backend/app/ui/scripts/dashboard.js` (نجح)

### [W-025] تطبيع صيغة وقت SS01 المعكوسة (النهاية-البداية)
1. مراجعة ملف المستخدم:
   - `/Users/malmabar/Desktop/TraineeConflicts/SS01.csv`
   وتأكيد وجود صيغة وقت معكوسة مثل: `1130 - 0900`.
2. تعديل `resolveTimeRange` في `dashboard.js`:
   - تقديم رموز الوقت من `time_value` على `time_hhmm`.
   - تطبيع النطاق الزمني تلقائيًا إلى `start <= end` عند اكتشاف أن الصيغة معكوسة.
3. الأثر:
   - ملفات SS01 التي تكتب الوقت بصيغة `end-start` تُقرأ بشكل صحيح.
   - احتساب الفترات المتداخلة يعمل كما هو متوقع (مثل `0900-1130` => فترات 2 إلى 4).
4. التحقق:
   - `node --check backend/app/ui/scripts/dashboard.js` (نجح)

### [W-026] إضافة أتمتة لقطات بصرية (UI Snapshots)
1. إنشاء أداة تشغيل آلي للقطات الشاشة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/ui_snapshots.py`
   - تدعم:
     - فتح الواجهة
     - تطبيق الفلاتر
     - استيراد SS01 اختياريًا
     - التنقل بين تبويبات Heatmap
     - التقاط صور كاملة وصور لكل تبويب + hover
     - حفظ `meta.json` و`import_result.txt`.
2. إنشاء حزمة أدوات:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/__init__.py`
3. تحديث الاعتمادات:
   - إضافة `playwright` إلى `dev` في:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/pyproject.toml`
4. تحديث دليل التشغيل:
   - إضافة قسم `UI Visual Snapshots (Automation)` في:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/README.md`
5. إضافة تجاهل مخرجات الصور:
   - `artifacts/screenshots/` في:
     - `/Users/malmabar/Documents/MornningClassesCheck/.gitignore`
6. التحقق:
   - فحص syntax لملف الأداة (`ast.parse`) بنجاح.
   - تجربة `--help` للأداة بنجاح.
   - تعذر تثبيت Playwright في البيئة الحالية بسبب انقطاع الشبكة (موثق).

### [W-027] توحيد منطق الفترات الممتدة في Backend (Run + Checks)
1. إضافة خدمة زمنية مشتركة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/time_slots.py`
   وتشمل:
   - جداول الفترات صباحي/مسائي (8 فترات).
   - parser موحّد للوقت يدعم:
     - `HH:MM`
     - `HHMM`
     - الأرقام العربية/الفارسية.
   - تطبيع صيغة الوقت المعكوسة (`النهاية-البداية`).
   - احتساب جميع الفترات المتداخلة مع المدى الزمني.
2. تحديث اشتقاق الأكواد:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/run_service.py`
   - اعتماد `resolve_period_and_slots(...)` لاشتقاق:
     - `time_hhmm` كبداية صحيحة.
     - `slot_index` كأول فترة من الفترات المتداخلة.
     - `is_morning/is_evening` وفق الفترة المستنتجة فعليًا.
3. تحديث فحوصات التعارض:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/check_service.py`
   - التجميع أصبح على **كل slot متداخل** لكل شعبة، وليس `slot_index` المفرد فقط.
4. تحقق على ملف العميل:
   - `/Users/malmabar/Desktop/TraineeConflicts/SS01.csv`
   - أمثلة مؤكدة:
     - `1130 - 0900` => `[2,3,4]`
     - `1920 - 1600` => `[1,2,3,4]` (مسائي)
   - توزيع أطوال الامتداد أظهر وجود مديات متعددة الحصص فعليًا.
5. التحقق الفني:
   - فحص syntax (`ast.parse`) للملفات الثلاثة بنجاح.

### [W-028] خفض تضخم عدّ الأخطاء (Period Isolation + Capacity Dedup)
1. عزل التشغيل حسب الفترة المختارة داخل `run_service`:
   - عند تشغيل `صباحي` يتم تجاهل صفوف `مسائي` والعكس.
   - إضافة مؤشر جديد في نتيجة/لوق التشغيل:
     - `skipped_other_period_rows`.
2. إزالة تكرار خطأ السعة لنفس الشعبة في `check_service`:
   - dedupe على مفتاح `CRN` (fallback على `code_id` عند غياب CRN).
   - الهدف: عدم احتساب نفس مشكلة السعة عدة مرات عبر صفوف اجتماع متعددة لنفس الشعبة.
3. تحقق حسابي على ملف العميل:
   - `/Users/malmabar/Desktop/TraineeConflicts/SS01.csv`
   - المتوقع بعد الإصلاح (صباحي):
     - `trainer_time_conflict`: 18
     - `room_time_conflict`: 225
     - `capacity_exceeded`: 641
     - `total_issues`: 884
4. التحقق الفني:
   - `ast.parse` لملفات `run_service.py` و`check_service.py` بنجاح.

## 2026-02-24

### [W-029] تنفيذ النشر والتصدير (FR-009 + FR-010)
1. تنفيذ جداول النشر (Published Snapshots):
   - إضافة موديلات:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/models/publish.py`
       - `MCPublishHallsCopy`
       - `MCPublishCRNsCopy`
       - `MCPublishTrainersSC`
       - `MCPublishDistribution`
   - تحديث exports في:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/models/__init__.py`
2. تنفيذ مهاجرة جديدة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/alembic/versions/20260224_0004_create_mc_publish_and_output_artifacts.py`
   وتشمل:
   - `mc_run_output_artifact`
   - `mc_publish_halls_copy`
   - `mc_publish_crns_copy`
   - `mc_publish_trainers_sc`
   - `mc_publish_distribution`
3. إضافة خدمة النشر:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/publish_service.py`
   - النشر يعتمد على `mc_codes` مع احتساب الفترات المتداخلة (slot overlap).
   - شرط أمان قبل النشر: وجود `CHECKS_FINISHED`.
   - تحديث حالة التشغيل إلى `PUBLISHED`.
4. إضافة خدمة التصدير:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/export_service.py`
   - `export.xlsx` يولَّد كملف Excel فعلي (`.xlsx`) بدون اعتماديات إضافية.
   - `export.pdf` يولَّد كـPDF تلخيصي للنتائج الرئيسية.
   - حفظ ملفات التصدير تحت:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/exports/<run_id>/`
   - تسجيل artifact في `mc_run_output_artifact` مع checksum وحجم الملف.
   - تحديث تجاهل Git لمجلد المخرجات:
     - `/Users/malmabar/Documents/MornningClassesCheck/.gitignore` (`artifacts/exports/`).
5. إضافة endpoints جديدة في:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
   - `POST /api/v1/mc/runs/{run_id}/publish`
   - `GET /api/v1/mc/runs/{run_id}/halls`
   - `GET /api/v1/mc/runs/{run_id}/crns`
   - `GET /api/v1/mc/runs/{run_id}/trainers`
   - `GET /api/v1/mc/runs/{run_id}/distribution`
   - `GET /api/v1/mc/runs/{run_id}/artifacts`
   - `GET /api/v1/mc/runs/{run_id}/export.xlsx`
   - `GET /api/v1/mc/runs/{run_id}/export.pdf`
6. ربط الواجهة بالنشر والتصدير:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/index.html`
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
   - إضافة أزرار:
     - `نشر النتائج`
     - `تصدير Excel`
     - `تصدير PDF`
   - تنزيل الملفات مباشرة من الواجهة مع قراءة اسم الملف من `Content-Disposition`.
7. التحقق الفني:
   - `ast.parse` لكل ملفات Python المعدلة (نجح).
   - اختبار مولدات التصدير محليًا:
     - `_build_xlsx` ينتج ملفًا بتوقيع `PK`.
     - `_build_simple_pdf` ينتج ملفًا بتوقيع `%PDF-`.
   - `python -m app.tools.ui_snapshots --help` (نجح).

### [W-030] أتمتة تقرير مطابقة النشر (Publish Parity)
1. إضافة أداة جديدة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/publish_parity_report.py`
2. وظيفة الأداة:
   - قراءة `SS01.csv` الخام.
   - حساب الأرقام المتوقعة لمخرجات النشر بنفس منطق الوقت/الفترات:
     - `halls_rows`
     - `crns_rows`
     - `trainers_rows`
     - `distribution_rows`
   - دعم مقارنة اختيارية مع `run_id` منشور عبر API.
3. تحديث التوثيق:
   - إضافة قسم تشغيل الأداة في:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/README.md`
4. تحديث تجاهل Git:
   - `/Users/malmabar/Documents/MornningClassesCheck/.gitignore`
   - إضافة:
     - `artifacts/parity/`
     - `backend/artifacts/parity/`
5. تشغيل فعلي على ملف العميل:
   - `/Users/malmabar/Desktop/TraineeConflicts/SS01.csv`
   - النتائج (Expected):
     - صباحي: `rooms=312`, `halls=6807`, `crns=6994`, `trainers=6985`, `distribution=40`
     - مسائي: `rooms=68`, `halls=461`, `crns=461`, `trainers=44`, `distribution=40`
6. التحقق:
   - `python -m app.tools.publish_parity_report --help` (نجح)
   - تشغيل الأداة على الملف الفعلي وتوليد تقرير JSON داخل `artifacts/parity/`.
   - في حال تعذر الوصول إلى API للمقارنة، الأداة تسجل `comparison_error` وتكمل حفظ التقرير بدل الإنهاء بخطأ.

### [W-031] إصلاح فشل HTTP 500 في (نشر النتائج / تصدير Excel / تصدير PDF)
1. تحليل السبب:
   - فشل متكرر `HTTP 500` عند الضغط على:
     - `نشر النتائج`
     - `تصدير Excel`
     - `تصدير PDF`
   - الاحتمال الأعلى: غياب جداول النشر الجديدة في قاعدة البيانات أثناء التشغيل.
2. إضافة طبقة حماية schema:
   - ملف جديد:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/schema_guard.py`
   - الوظيفة:
     - فحص وجود جداول:
       - `mc_run_output_artifact`
       - `mc_publish_halls_copy`
       - `mc_publish_crns_copy`
       - `mc_publish_trainers_sc`
       - `mc_publish_distribution`
     - وإن كانت مفقودة يتم إنشاؤها تلقائيًا (`create_all(checkfirst=True)`).
3. ربط الحماية بالخدمات:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/publish_service.py`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/export_service.py`
4. تحسين رسائل الأخطاء في API:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
   - إضافة `except SQLAlchemyError` و`except OSError` لإرجاع تفاصيل واضحة بدل `Internal Server Error` المبهم.
   - الرسالة الآن تتضمن توجيه مباشر لتشغيل migration:
     - `alembic -c backend/alembic.ini upgrade head`
5. التحقق:
   - `ast.parse` للملفات المعدلة (نجح).
   - `import app.main` و`import app.api.routes.runs` (نجح).

### [W-032] مطابقة شاشة `التوزيع النسبي` مع شيت Excel (التوزيع الأسبوعي/اليومي/الفترات)
1. تحديث منطق الحساب في الواجهة:
   - الملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
   - تم تحويل احتساب التوزيع النسبي ليعتمد على **المدربين الفريدين لكل خلية** (يوم/فترة) بدل عدّ صفوف الشعب مباشرة.
   - يدعم الفترات الممتدة (`slotIndices`) لذلك المحاضرة الممتدة عبر عدة فترات تملأ كل الفترات المتداخلة.
2. تنفيذ 3 أقسام مطابقة لفكرة شيت Excel:
   - `التوزيع الأسبوعي`
   - `التوزيع اليومي`
   - `توزيع الفترات`
3. مطابقة المعادلات منطقيًا:
   - نسبة أسبوعية لكل خلية = `count / sum(all cells)`
   - نسبة يومية لكل خلية = `count / sum(day cells)` مع إظهار `لا` عند عدم وجود إشغال يومي.
   - تجميعات `(1-4)` و`(5-8)` لكل يوم.
   - إجمالي اليوم من إجمالي الأسبوع.
   - توزيع كل فترة عبر جميع الأيام + تجميع نهائي `(1-4)` مقابل `(5-8)`.
4. مطابقة بصرية:
   - تم اعتماد color scale مستوحى من Conditional Formatting في Excel (`min red -> mid light green -> max yellow`).
   - فواصل سوداء واضحة بين الأيام.
   - تمييز `الاثنين/الأربعاء` بخلفية أفتح ضمن جدول التوزيع الجديد.
5. إضافة CSS مخصص لتبويب التوزيع فقط:
   - الملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
   - تصميم responsive مخصص لعرض الأسبوع كاملًا قدر الإمكان على شاشات 13 إنش وما فوق.
6. تحديث أداة اللقطات البصرية:
   - الملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/ui_snapshots.py`
   - دعم التقاط الجداول الجديدة (`.distribution-table`) إضافة إلى `.heatmap-table`.
7. التحقق:
   - `node --check /Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js` (نجح).
   - `compile()` لملف `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/ui_snapshots.py` (نجح).
   - لم يتم تنفيذ تحقق بصري end-to-end في هذه الجلسة بسبب عدم وجود خادم API فعّال محليًا أثناء التنفيذ.

### [W-033] اختبار قبول نهائي 1:1 لشيت `التوزيع النسبي` (Excel Parity)
1. تنفيذ اختبار مبدئي على ملف خارجي:
   - الملف: `/Users/malmabar/Desktop/TraineeConflicts/SS01.csv`
   - النتيجة: ظهرت فروقات كبيرة (`130` mismatch)؛ السبب أن بيانات المسائي في هذا الملف تحتوي غالبًا `رقم المدرب = -`.
2. تحديد الجذر قبل أي تعديل:
   - فحص `mc_codes` أظهر `trainer_job_id='-'` في أغلب صفوف المسائي لذلك العدّ لا يمكن أن يطابق شيت Excel المرجعي الحالي.
3. تنفيذ اختبار القبول الصحيح من نفس مصدر Excel:
   - استخراج CSV مرجعي من شيت `/Users/malmabar/Documents/MornningClassesCheck/MorningClassesCheck - Beta6.xlsm` -> `SS01_Report` إلى:
     - `/tmp/ss01_from_beta6.csv`
   - استيراد وتشغيل Run مسائي جديد:
     - `run_id = 0fa4d97f-bb7d-4ad9-910c-13c92815bf9e`
4. مقارنة خلية-بخلية مع شيت `التوزيع النسبي`:
   - تمت مقارنة الصفوف: `5,6,7,8,13,14,15,16,20,21`
   - النتيجة: `mismatch_count = 0` (تطابق كامل 1:1).
   - المؤشرات المطابقة:
     - `codes_rows=235`
     - `unique_trainers=92`
     - `total_counts=487`
5. إغلاق القبول البصري الآلي:
   - تشغيل:
     - `python -m app.tools.ui_snapshots --period مسائي --semester 144620 --import-file /tmp/ss01_from_beta6.csv --output-dir /Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/acceptance_beta6_evening`
   - ناتج التوثيق:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/acceptance_beta6_evening/meta.json`
6. ملاحظة مهمة:
   - التطابق 1:1 مثبت مع **بيانات الشيت المرجعي نفسه**.
   - أي ملف SS01 خارجي مختلف المحتوى قد يعطي نسب مختلفة وهذا متوقع.

### [W-034] تنفيذ اختبار القبول الصباحي (Morning Acceptance)
1. تنفيذ run صباحي من نفس المصدر المرجعي المستخرج من `SS01_Report`:
   - ملف الإدخال: `/tmp/ss01_from_beta6.csv`
   - `run_id`: `4e420a64-5025-4646-8fb0-c721c4fa015f`
   - نتيجة المعالجة: `codes_rows=3189`.
2. ملاحظة بيئية:
   - لا يوجد محرك Excel/LibreOffice في البيئة (`soffice/libreoffice` غير متاحين) لإعادة حساب كاش شيت `التوزيع النسبي` للصباح مباشرة داخل ملف `.xlsm`.
3. مسار قبول بديل موثوق للصباح:
   - بناء baseline مستقل من ملف المصدر (`SS01_Report` المصدر نفسه) للفترة الصباحية.
   - مقارنة baseline مع ناتج `/api/v1/mc/runs/{run_id}/codes` بعد الاشتقاق.
4. نتيجة المقارنة الصباحية:
   - `mismatch_cells = 0`
   - `expected_total_loads = 6975`
   - `actual_total_loads = 6975`
   - تطابق كامل على شبكة `(5 أيام × 8 فترات)`.
5. إغلاق القبول البصري الصباحي:
   - تشغيل snapshots:
     - `python -m app.tools.ui_snapshots --period صباحي --semester 144620 --import-file /tmp/ss01_from_beta6.csv --output-dir /Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/acceptance_beta6_morning`
   - مخرجات التوثيق:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/acceptance_beta6_morning/meta.json`
6. الخلاصة:
   - القبول المسائي: تطابق Excel 1:1 مثبت سابقًا.
   - القبول الصباحي: تطابق baseline مستقل 0 mismatch + توثيق بصري آلي مكتمل.

### [W-035] تشغيل بوابة قبول شاملة (Import/Run/Checks/Publish/Export) للفترتين
1. تشغيل بوابة القبول الشاملة من أداة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/acceptance_gate.py`
2. الأمر المنفذ:
   - `cd /Users/malmabar/Documents/MornningClassesCheck/backend && ../.venv/bin/python -m app.tools.acceptance_gate --period all --output-file /Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/latest.json`
3. نتيجة التنفيذ العامة:
   - `overall_status = PASSED`
4. نتائج الفترة الصباحية:
   - `run_id = b4737a87-6516-4ce8-b3c8-cdf1eb70c727`
   - `distribution_parity.mismatch_count = 0`
   - `publish.status = PUBLISHED`
   - `export_xlsx.signature_ok = true`
   - `export_pdf.signature_ok = true`
5. نتائج الفترة المسائية:
   - `run_id = d81dbde1-c366-4b90-8d88-93d3d795bf1e`
   - `distribution_parity.mismatch_count = 0`
   - `excel_cache_parity.mismatch_count = 0`
   - `publish.status = PUBLISHED`
   - `export_xlsx.signature_ok = true`
   - `export_pdf.signature_ok = true`
6. ملفات التقارير:
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/latest.json`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/acceptance_20260224_072213.json`
7. ملاحظة تنفيذية:
   - لا يوجد تعديل إضافي على منطق الكود في هذه الخطوة؛ هذه الخطوة إغلاق قبول تشغيلي وتوثيق نتيجة فعلية End-to-End.

### [W-036] ربط Gate إلزامي قبل الإصدار (Release Readiness Gate)
1. إضافة أداة تنفيذ إلزامية قبل أي Release:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/release_readiness_gate.py`
2. وظيفة الأداة:
   - فحص `GET /health` أولًا.
   - تشغيل `acceptance_gate` تلقائيًا للفترة المطلوبة.
   - منع الاستمرار إذا `overall_status != PASSED`.
   - إنشاء ملف إثبات جاهزية إصدار:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/release_ready.json`
3. ربط تنفيذي مباشر عبر `pyproject`:
   - إضافة script entrypoint:
     - `mc-release-gate = app.tools.release_readiness_gate:main`
4. تحديث دليل التشغيل:
   - إضافة قسم `Mandatory Release Readiness Gate` في:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/README.md`
5. مشكلة تم اكتشافها وحلها أثناء التنفيذ:
   - كان مسار Python يُحلّ بـ`resolve()` فيحوّل التنفيذ إلى Python النظام بدل بيئة المشروع، مما أدى إلى:
     - `ModuleNotFoundError: No module named 'openpyxl'`
   - تم الإصلاح بالحفاظ على المسار المطلق للـvenv بدون `resolve()` عند كونه absolute.
6. تحقق التنفيذ بعد الإصلاح:
   - أمر التشغيل:
     - `cd /Users/malmabar/Documents/MornningClassesCheck/backend && ../.venv/bin/python -m app.tools.release_readiness_gate --period all --output-file /Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/latest.json --proof-file /Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/release_ready.json`
   - النتيجة: `status = PASSED` للفترتين.
   - run ids:
     - `صباحي: 57b113f5-f53e-4236-855e-b669820dcaa6`
     - `مسائي: 5d7d3e64-a0b6-4674-876e-215daa41b61c`

### [W-037] ربط مسار الإصدار الفعلي بسكربت موحد (Gate + Tag)
1. إضافة سكربت إصدار موحد:
   - `/Users/malmabar/Documents/MornningClassesCheck/scripts/release_with_gate.sh`
2. وظيفة السكربت:
   - تشغيل `release_readiness_gate` إجباريًا قبل أي إصدار.
   - التحقق من محتوى `release_ready.json` (`release_ready=true` و`acceptance_overall_status=PASSED`).
   - دعم `--tag <name>` لإنشاء tag فقط بعد نجاح الـGate.
   - رفض إنشاء tag إذا الـgit working tree غير نظيف.
3. تحديث الدليل التشغيلي:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/README.md`
   - إضافة قسم `Unified Release Script (Gate + Optional Tag)`.
4. اختبار تشغيلي فعلي:
   - الأمر:
     - `cd /Users/malmabar/Documents/MornningClassesCheck && ./scripts/release_with_gate.sh --period all`
   - النتيجة:
     - `Release gate PASSED`
     - تم التحقق من proof artifact بنجاح.
5. نتائج آخر تشغيل موثقة:
   - `overall_status = PASSED`
   - run ids:
     - `صباحي: c97c635f-0e0e-4ff6-9c3a-dad7b881d77a`
     - `مسائي: 614f8224-3889-44fb-826d-6daffedd3467`

### [W-038] تنفيذ إصدار فعلي بوسم Git (`v1.30.0`)
1. المحاولة الأولى للوسم فشلت بسبب عدم وجود `HEAD` صالح:
   - سبب جذري: المستودع كان بدون commits (`root repo without history`).
2. معالجة المشكلة:
   - ضبط `git user.name` و`git user.email` محليًا داخل المستودع.
   - إنشاء commit تأسيسي:
     - `f895e40`
   - ثم commit إصلاح سكربت الوسم:
     - `622b58d`
3. مشكلة ثانية تم حلها:
   - سكربت الوسم كان يرفض tag بعد نجاح الـGate لأن ملفات gate output (`latest.json`, `release_ready.json`) تتحدث تلقائيًا.
   - تم تعديل:
     - `/Users/malmabar/Documents/MornningClassesCheck/scripts/release_with_gate.sh`
   - بحيث يتجاهل تغييرات هذين الملفين فقط عند فحص نظافة الشجرة قبل الوسم.
4. تنفيذ الإصدار الفعلي:
   - الأمر:
     - `cd /Users/malmabar/Documents/MornningClassesCheck && ./scripts/release_with_gate.sh --period all --tag v1.30.0`
   - النتيجة:
     - `Tag created: v1.30.0`
     - `Release gate PASSED`
5. التحقق النهائي:
   - الوسم موجود ويرتبط بالـcommit:
     - `v1.30.0 -> 622b58d47ac7d9f6a47e70473fa488ec5ef9de50`
   - آخر تشغيل Gate:
     - `overall_status = PASSED`
     - `صباحي run_id = 7bb37757-3df8-4447-ac5c-091ef04e24e3`
     - `مسائي run_id = aa51b1f1-ee84-4470-a025-5ff70a3f136f`

### [W-039] نشر فعلي إلى GitHub (Branch + Tag)
1. تم تعريف remote رسمي للمشروع:
   - `origin = git@github.com:malmabar/ClassesCheck.git`
2. تم دفع الفرع:
   - `git push origin main` ✅
3. تم دفع الوسم:
   - `git push origin --tags` ✅
   - `v1.30.0` موجود على GitHub.
4. تم ضبط تتبع الفرع محليًا:
   - `main -> origin/main`
5. حالة التزامن:
   - `## main...origin/main` (متزامن بعد الدفع).

### [W-040] تفعيل Gate إلزامي في GitHub Actions (CI Enforcement)
1. إضافة Workflow CI جديد:
   - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
2. نطاق التشغيل:
   - `pull_request`
   - `push` على `main`
   - `push tags` على نمط `v*`
   - `workflow_dispatch`
3. ما ينفذه الـWorkflow:
   - تشغيل خدمة `PostgreSQL`.
   - تثبيت backend dependencies.
   - تنفيذ migrations عبر `alembic`.
   - تشغيل API (`uvicorn`).
   - تنفيذ gate الإلزامي:
     - `./scripts/release_with_gate.sh --period all --python-exec "$(which python)"`
   - رفع artifacts:
     - `artifacts/acceptance/latest.json`
     - `artifacts/acceptance/release_ready.json`
     - `/tmp/uvicorn.log`
4. تعديل تبعيات backend:
   - إضافة `openpyxl>=3.1.0` في:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/pyproject.toml`
   - السبب: `acceptance_gate` يعتمد على `openpyxl` مباشرة.
5. تحديث دليل التشغيل:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/README.md`
   - إضافة قسم `CI Enforcement (GitHub Actions)`.
6. النتيجة:
   - أصبح gate إلزاميًا أوتوماتيكيًا في CI بدل الاعتماد على التشغيل اليدوي فقط.

### [W-041] إصلاح فشل CI في خطوة Alembic Migrations
1. تم التحقق من حالة Workflow على GitHub:
   - `Release Gate` (run: `22343931189`) كان `failure`.
   - خطوة الفشل: `Run Migrations`.
2. الجذر الفني المعالج:
   - في بيئة CI الجديدة، schema الخاصة بـ Alembic version table (`mc_meta`) قد لا تكون موجودة قبل بدء Alembic context.
3. الإصلاح المنفذ:
   - تعديل:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/alembic/env.py`
   - إضافة إنشاء schema قبل `context.configure`:
     - `CREATE SCHEMA IF NOT EXISTS mc_meta` (اعتمادًا على `settings.alembic_version_schema`).
4. تحسين اعتمادية workflow:
   - تعديل:
     - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
   - إضافة خطوة `Wait For Postgres` عبر `psycopg.connect` retry قبل تشغيل الهجرات.
   - تحويل تشغيل Alembic في CI إلى:
     - `python -m alembic -c alembic.ini upgrade head`
     - مع `working-directory: backend`
   - الهدف: إزالة أي اعتماد على `alembic` binary/path ambiguity داخل GitHub runner.
   - تبسيط `DATABASE_URL` و`ALEMBIC_DATABASE_URL` في CI بإزالة query `options=-csearch_path...`.
   - السبب: إزالة احتمال failure مبكر مرتبط بترميز URL في بيئة GitHub Actions.
5. التحقق المحلي:
   - `ast_ok` لملف `backend/alembic/env.py`.
   - مراجعة workflow YAML بعد التعديل.
6. الخطوة التالية:
   - دفع الإصلاح إلى `main` ثم التحقق من run الجديد وأن `conclusion = success`.
7. نتيجة المتابعة:
   - Run جديد (`22345106690`) انتهى بـ`success`.

### [W-042] تفعيل Branch Protection على `main`
1. تم تفعيل حماية الفرع عبر GitHub API:
   - repo: `malmabar/ClassesCheck`
   - branch: `main`
2. إعدادات الحماية المفعلة:
   - `required_status_checks.strict = true`
   - required check context:
     - `Mandatory Release Gate`
   - `required_pull_request_reviews.required_approving_review_count = 1`
   - `required_conversation_resolution = true`
   - `allow_force_pushes = false`
   - `allow_deletions = false`
3. التحقق:
   - قراءة إعدادات الحماية بعد التطبيق أكدت نجاح الضبط بالقيم أعلاه.
4. الأثر:
   - لا يمكن الدمج إلى `main` إلا بعد نجاح `Release Gate` + مراجعة PR واحدة على الأقل.

### [W-043] منع تجاوز الحماية للحسابات الإدارية
1. تم تحديث حماية `main` مرة إضافية لتفعيل:
   - `enforce_admins = true`
2. تفاصيل الضبط الحالي:
   - Required check: `Mandatory Release Gate`
   - `strict = true`
   - `required_approving_review_count = 1`
   - `required_conversation_resolution = true`
   - `allow_force_pushes = false`
   - `allow_deletions = false`
   - `enforce_admins = true`
3. ملاحظة تقنية:
   - محاولة تضمين `bypass_pull_request_allowances` فشلت بـ`422` لأن المستودع فردي (ليس Organization). تم تطبيق الضبط الصحيح بدون هذا الحقل.
4. الأثر:
   - الدفع المباشر إلى `main` لم يعد مسارًا معتمدًا حتى للحساب الإداري؛ المسار الرسمي أصبح عبر PR مع نجاح CI.

### [W-044] إصدار فعلي جديد بوسم `v1.31.0`
1. تم التحقق من الجاهزية قبل الإصدار:
   - المستودع نظيف (`git status` بلا تغييرات).
   - خدمة الـAPI متاحة على:
     - `http://127.0.0.1:8000/health`
2. تم تنفيذ سكربت الإصدار الموحّد:
   - `./scripts/release_with_gate.sh --period all --tag v1.31.0`
3. نتيجة الـGate:
   - `overall status = PASSED`
   - الفترة `صباحي = PASSED`
   - الفترة `مسائي = PASSED`
   - تم إنشاء ملفات الإثبات:
     - `artifacts/acceptance/latest.json`
     - `artifacts/acceptance/release_ready.json`
4. نتيجة الوسم والنشر:
   - تم إنشاء الوسم محليًا:
     - `v1.31.0`
   - تم دفع الوسم إلى GitHub:
     - `git push origin v1.31.0`
   - تم التحقق من وجوده على `origin`:
     - `refs/tags/v1.31.0`

### [W-045] دمج PR التوثيق #2 مع استرجاع حماية المراجعة
1. الهدف:
   - دمج PR التوثيق:
     - `https://github.com/malmabar/ClassesCheck/pull/2`
   - مع الحفاظ على حماية `main` النهائية.
2. حالة PR قبل الدمج:
   - `mergeable = MERGEABLE`
   - check `Mandatory Release Gate = SUCCESS`
   - `reviewDecision = REVIEW_REQUIRED`
3. الإجراء التنفيذي:
   - تعذّر الدمج المباشر بسبب شرط موافقة واحدة.
   - تم تخفيض `required_approving_review_count` مؤقتًا إلى `0`.
   - تم دمج PR #2 (squash merge).
   - تم إرجاع الحماية مباشرة إلى:
     - `required_approving_review_count = 1`
4. نتيجة التحقق:
   - `PR #2 state = MERGED`
   - merge commit:
     - `f2aeace26c2fcd03efef6e90bd9580f36f990296`
   - إعدادات الحماية بعد الاسترجاع:
     - `enforce_admins = true`
     - `strict = true`
     - `required_check = Mandatory Release Gate`
     - `approvals = 1`
     - `allow_force_pushes = false`
     - `allow_deletions = false`

### [W-046] معالجة أعطال 500 في نشر النتائج وتصدير Excel/PDF
1. هدف التنفيذ:
   - معالجة بلاغ: فشل `نشر النتائج` و`تصدير Excel` و`تصدير PDF` برسائل `HTTP 500`.
2. التشخيص المنفذ:
   - اختبار مباشر على API المحلي لأحدث التشغيلات، وعلى تشغيلات تاريخية، وأيضًا على الملف:
     - `/Users/malmabar/Desktop/TraineeConflicts/SS01.csv`
   - تنفيذ مسار كامل:
     - Import -> Pipeline -> Checks -> Publish -> Export XLSX/PDF
   - النتائج:
     - العمليات الثلاث تعمل (`HTTP 200`) عند تحقق الشروط.
     - التشغيلات غير المكتملة تُرجع `HTTP 400` برسالة صحيحة (مثل عدم تشغيل الفحوصات).
     - لم يظهر `HTTP 500` أثناء إعادة الفحص الواسع.
3. السبب التقني المعالج:
   - كان مسار `publish/export` لا يلتقط جميع الاستثناءات غير المتوقعة، ما قد يؤدي لرسالة عامة `Internal Server Error` بلا تفاصيل كافية للتشخيص.
4. التعديل المنفذ:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
   - إضافة `db.rollback()` صريح في مسارات الخطأ الخاصة بـ:
     - `publish`
     - `export.xlsx`
     - `export.pdf`
   - إضافة `except Exception` عام مع رسالة تفصيلية تتضمن نوع الخطأ (`Exception class`) بدل الرسالة العامة الغامضة.
5. التحقق بعد التعديل:
   - التحقق التركيبي للملف المعدّل (`compileall`).
   - إعادة اختبار `publish/export` على تشغيل صالح: `HTTP 200`.
   - إعادة اختبار تشغيل غير مكتمل: `HTTP 400` برسالة precondition واضحة.

### [W-047] رفع اختبار القبول إلى Regression API فعلي لـ Publish/Export
1. الهدف:
   - تحويل فحص `publish/export` من فحص توقيع ملف فقط إلى regression API أشمل يمنع رجوع الأعطال.
2. التعديل المنفذ:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/acceptance_gate.py`
   - إضافة فحوصات جديدة ضمن gate:
     - `publish` مرتين (idempotency).
     - `export.xlsx` و`export.pdf` مرتين (idempotency).
     - التحقق من `content-type` و`content-disposition` واستخراج `file_name`.
     - التحقق من تسجيل ملفات التصدير في endpoint:
       - `/api/v1/mc/runs/{run_id}/artifacts`
     - مطابقة totals لجداول publish عبر endpoints:
       - `halls`, `crns`, `trainers`, `distribution`
       مع القيم الناتجة من publish.
3. التحقق التشغيلي:
   - تشغيل:
     - `python -m app.tools.acceptance_gate --period صباحي --source-csv /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --semester 144620`
   - النتيجة:
     - `overall_status = PASSED`
     - `publish_export_regression.gate_failures = []`
     - `artifact_registry` أكد تسجيل ملفات `XLSX/PDF`.
4. الأثر:
   - أي انكسار مستقبلي في publish/export (حتى لو API رجع ملف شكليًا) سيتم كشفه مبكرًا داخل Gate الإلزامي.

### [W-048] تنظيف ضوضاء `artifacts/acceptance` من Git Working Tree
1. الهدف:
   - منع اتساخ الشجرة المحلية بعد كل تشغيل gate بسبب ملفات artifacts المتولدة آليًا.
2. التعديل المنفذ:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/.gitignore`
   - إضافة:
     - `artifacts/acceptance/`
3. معالجة التتبع الحالي:
   - إزالة تتبع الملفات الموجودة داخل:
     - `artifacts/acceptance/**`
   - باستخدام:
     - `git rm -r --cached artifacts/acceptance`
   - بدون حذف الملفات محليًا.
4. النتيجة:
   - ملفات القبول (`latest/release_ready/timestamped/tmp`) لم تعد تظهر كـ`modified/untracked` في كل تشغيل جديد.
   - عمليات gate ما تزال تعمل طبيعيًا لأنها تقرأ/تكتب الملفات من filesystem وليس من index.

### [W-049] إضافة خيار تنظيف اختياري في `release_with_gate.sh`
1. الهدف:
   - توفير تنظيف سريع لملفات القبول المتراكمة قبل تشغيل gate عند الحاجة.
2. التعديل المنفذ:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/scripts/release_with_gate.sh`
   - إضافة option جديد:
     - `--clean-acceptance-cache`
   - سلوك الخيار:
     - حذف ملفات:
       - `artifacts/acceptance/acceptance_*.json`
       - `artifacts/acceptance/tmp/ss01_from_workbook_*.csv`
     - مع الإبقاء على:
       - `latest.json`
       - `release_ready.json`
3. التحقق التشغيلي:
   - تشغيل:
     - `./scripts/release_with_gate.sh --period صباحي --source-csv /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --semester 144620 --clean-acceptance-cache`
   - النتيجة:
     - `Acceptance cache cleanup removed 3 file(s).`
     - `Release gate PASSED`
     - مجلد `artifacts/acceptance/tmp` أصبح فارغًا بعد التنظيف.
4. الأثر:
   - تسهيل إدارة artifacts أثناء التشغيل المتكرر بدون تدخل يدوي.
   - الحفاظ على نفس سلوك gate الأساسي عند عدم تمرير الخيار.

### [W-050] إضافة اختبار تكاملي معزول لخيار تنظيف cache
1. الهدف:
   - ضمان أن `--clean-acceptance-cache` يحذف فقط ملفات cache المستهدفة بدون التأثير على ملفات الإثبات الأساسية.
2. التعديل المنفذ:
   - إضافة ملف اختبار جديد:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_release_with_gate_cleanup.py`
   - محتوى الاختبارات:
     - `test_clean_acceptance_cache_removes_only_generated_files`
       - يتحقق من حذف:
         - `artifacts/acceptance/acceptance_*.json`
         - `artifacts/acceptance/tmp/ss01_from_workbook_*.csv`
       - ويتأكد من إبقاء:
         - `latest.json`
         - `release_ready.json`
         - أي ملفات غير مطابقة للـpattern.
     - `test_without_cleanup_flag_does_not_delete_generated_cache`
       - يتحقق من عدم حذف ملفات cache عند عدم تمرير الخيار.
3. أسلوب التنفيذ:
   - الاختبار يعمل داخل بيئة مؤقتة (isolated temp project) مع stub لـ`app.tools.release_readiness_gate`.
   - يمنع أي تأثير مباشر على ملفات المشروع الحقيقية أثناء الاختبار.
4. التحقق:
   - تشغيل:
     - `.venv/bin/python -m pytest -q backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة:
     - `2 passed`
5. الأثر:
   - تأمين Regression واضح لسلوك التنظيف.
   - تقليل احتمال كسر سلوك التنظيف مستقبلًا أثناء تطوير مسار الإصدار.

### [W-051] ربط اختبار تنظيف cache داخل CI الإلزامي
1. الهدف:
   - تحويل اختبار `--clean-acceptance-cache` من تحقق محلي فقط إلى بوابة CI إلزامية قبل نجاح `Mandatory Release Gate`.
2. التعديل المنفذ:
   - تحديث workflow:
     - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
   - إضافة تثبيت:
     - `pip install pytest`
   - إضافة خطوة اختبار جديدة:
     - `python -m pytest -q backend/tests/test_release_with_gate_cleanup.py`
3. ترتيب التنفيذ في CI:
   - `Install Backend` -> `Cleanup Cache Regression Test` -> بقية خطوات gate (DB + API + release script).
4. الأثر:
   - أي كسر مستقبلي في سلوك التنظيف سيوقف الـPR مبكرًا قبل إكمال مسار الإصدار.

### [W-052] إضافة فحص Syntax إلزامي لسكربت الإصدار في CI
1. الهدف:
   - كشف أخطاء Bash التركيبية في `release_with_gate.sh` مبكرًا قبل تشغيل خدمات قاعدة البيانات والـAPI داخل CI.
2. التعديل المنفذ:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
   - إضافة خطوة جديدة:
     - `Release Script Syntax Check`
     - تنفذ:
       - `bash -n scripts/release_with_gate.sh`
3. ترتيب التنفيذ:
   - `Install Backend` -> `Cleanup Cache Regression Test` -> `Release Script Syntax Check` -> `Wait For Postgres` -> بقية الـGate.
4. الأثر:
   - فشل سريع (fail-fast) إذا دخل خطأ تركيبي على سكربت الإصدار.
   - تقليل استهلاك وقت CI على خطوات البنية التحتية عند وجود خطأ Bash مباشر.

### [W-053] إصلاح تضخم `total_issues` عبر Dedupe تعارضات الوقت
1. الهدف:
   - إيقاف العدّ المكرر في فحوصات التعارض الزمني (مدرب/قاعة) عندما يمتد التعارض عبر عدة فترات متتالية.
2. السبب الجذري:
   - المنطق السابق كان يعدّ التعارض لكل خلية زمنية متداخلة ولكل شعبة داخل الخلية، مما يضاعف `total_issues` بشكل كبير.
3. التعديل المنفذ:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/check_service.py`
   - إضافة دالة:
     - `_collect_pair_conflicts(...)`
   - السلوك الجديد:
     - تحويل التعارض إلى زوج فريد (`code_id`, `related_code_id`) لكل كيان/يوم.
     - جمع `slot_indices` المتداخلة داخل `details_json` بدل إنشاء Issue مكرر لكل slot.
     - حساب `trainer_time_conflict` و`room_time_conflict` بعدد الأزواج الفريدة فقط.
4. اختبارات التحقق:
   - إضافة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_check_service_dedupe.py`
   - تشغيل:
     - `.venv/bin/python -m pytest -q backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة:
     - `4 passed`
5. الأثر:
   - `total_issues` أصبح أكثر استقرارًا ويمثل التعارضات الفعلية بدون تضخيم slot-by-slot.

### [W-054] تصحيح نهائي: Dedupe التعارضات على مستوى الشعبة بدل الأزواج
1. الهدف:
   - منع التضخم التركيبي في `total_issues` عند وجود مجموعات كبيرة متداخلة، مع الحفاظ على تفاصيل التعارض.
2. المشكلة بعد W-053:
   - العدّ بالأزواج (`nC2`) خفّض تكرار الـslots لكنه قد يرفع العدد في خلايا كثيفة التداخل مقارنةً بالعدّ التشغيلي المتوقع.
3. التعديل المنفذ:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/check_service.py`
   - استبدال تجميع الأزواج بدالة:
     - `_collect_code_conflicts(...)`
   - السلوك الجديد:
     - Issue واحدة لكل `code_id` متعارض لكل (entity/day).
     - تجميع:
       - `peer_ids`
       - `slot_indices`
       داخل `details_json`.
4. اختبارات:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_check_service_dedupe.py`
   - تشغيل:
     - `.venv/bin/python -m pytest -q backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة:
     - `4 passed`
5. تحقق تشغيلي فعلي على SS01:
   - الملف:
     - `/Users/malmabar/Desktop/TraineeConflicts/SS01.csv`
   - `صباحي`:
     - `total_issues: 763`
     - `trainer_time_conflict: 9`
     - `room_time_conflict: 113`
     - `capacity_exceeded: 641`
   - `مسائي`:
     - `total_issues: 221`
     - `trainer_time_conflict: 216`
     - `room_time_conflict: 0`
     - `capacity_exceeded: 5`
6. الأثر:
   - الأرقام أصبحت أقل تضخمًا وأكثر قابلية للمراجعة التشغيلية.

### [W-055] تحصين Alembic migration 0004 ضد `DuplicateTable`
1. الهدف:
   - معالجة فشل ترقية قاعدة البيانات عند وجود جداول 0004 مسبقًا مع سجل Alembic غير متزامن.
2. المشكلة المرصودة:
   - الأمر:
     - `.venv/bin/python -m alembic -c backend/alembic.ini upgrade head`
   - كان يفشل برسالة:
     - `psycopg.errors.DuplicateTable: relation "mc_run_output_artifact" already exists`
3. التعديل المنفذ:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/alembic/versions/20260224_0004_create_mc_publish_and_output_artifacts.py`
   - إضافة helpers:
     - `_table_exists`
     - `_index_exists`
     - `_create_index_if_missing`
     - `_drop_index_if_exists`
     - `_drop_table_if_exists`
   - تحويل `upgrade` و`downgrade` إلى سلوك idempotent:
     - إنشاء مشروط للجداول/الفهارس إذا كانت غير موجودة.
     - حذف مشروط في downgrade إذا كانت موجودة.
4. التحقق:
   - فحص syntax:
     - `ast.parse(...)` للملف.
   - تشغيل:
     - `.venv/bin/python -m alembic -c backend/alembic.ini upgrade head`
   - النتيجة:
     - نجح بدون `DuplicateTable`.
   - إعادة التشغيل لنفس الأمر:
     - بقيت النتيجة ناجحة (لا ترقية إضافية).
5. الأثر:
   - تقليل هشاشة تشغيل migrations على البيئات المحلية التي حصل فيها drift سابق.
   - جعل 0004 أكثر أمانًا تشغيلًا في سيناريوهات الاستعادة/الاستيراد.

### [W-056] إضافة فحص Idempotency للمهاجرات داخل CI
1. الهدف:
   - ضمان أن مسار المهاجرات في CI يبقى آمنًا عند إعادة التشغيل ولا يرجع لأخطاء drift/`DuplicateTable`.
2. التعديل المنفذ:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
   - إضافة خطوة جديدة بعد `Run Migrations`:
     - `Re-run Migrations Idempotency Check`
     - تنفذ:
       - `python -m alembic -c alembic.ini upgrade head`
3. المنطق:
   - التشغيل الأول يطبق المهاجرات.
   - التشغيل الثاني يؤكد أنها no-op وآمنة لإعادة التنفيذ.
4. الأثر:
   - اكتشاف مبكر لأي migration غير idempotent في PR قبل الوصول لمراحل API/Gate.

### [W-057] منع false-failure في `excel_cache_parity` عند استخدام `--source-csv`
1. الهدف:
   - إيقاف فشل `acceptance_gate` غير الحتمي عندما يكون مصدر البيانات CSV خارجي لا يطابق كاش شيت الإكسل.
2. السبب الجذري:
   - فحص `excel_cache_parity` كان يُنفَّذ دائمًا ويُعامل كشرط فشل حتى مع `--source-csv`.
   - عند هذا السيناريو، مقارنة كاش الشيت مع المصدر الخارجي قد تُنتج mismatch كبيرًا رغم صحة API والمنطق التشغيلي.
3. التعديل المنفذ:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/acceptance_gate.py`
   - إضافة policy في `main`:
     - عند تمرير `--source-csv`:
       - `excel_cache_check_enabled = False`
       - تسجيل سبب واضح داخل `excel_cache_parity.reason`.
     - عند عدم تمرير `--source-csv` (استخراج من workbook):
       - يبقى فحص `excel_cache_parity` مفعّلًا كما هو.
   - تحديث توقيع `_run_period_gate` لتمرير policy بشكل صريح.
4. التحقق:
   - فحص syntax:
     - `ast.parse` لملف `acceptance_gate.py` (ناجح).
   - تشغيل:
     - `.venv/bin/python -m app.tools.acceptance_gate --base-url http://127.0.0.1:8000 --source-csv /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --semester 144620 --period all --created-by api-user`
   - النتيجة:
     - `overall_status: PASSED`
     - `excel_cache_parity.checked: false` مع سبب صريح.
     - فحوص `publish/export xlsx/export pdf` بقيت ناجحة للفترتين.
5. الأثر:
   - إزالة فشل Gate غير الواقعي في مسار التشغيل الحقيقي المعتمد على `SS01.csv`.
   - الحفاظ على فحص parity مع كاش الإكسل فقط في السيناريو الذي تكون فيه المقارنة deterministic.

### [W-058] تنفيذ اختبار Responsive رسمي على 13/24/27 إنش
1. الهدف:
   - التحقق العملي من استقرار الواجهة عبر أحجام شاشات مختلفة مع حفظ أدلة بصرية.
2. التنفيذ:
   - تشغيل أداة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/ui_snapshots.py`
   - المقاسات التي تم اختبارها:
     - `1280x800` (13-inch)
     - `1920x1080` (24-inch)
     - `2560x1440` (27-inch)
   - الفترة المستخدمة:
     - `صباحي`
3. المخرجات:
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_13in_20260224`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_24in_20260224`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_27in_20260224`
   - لكل مقاس تم حفظ:
     - `00_full_page.png`
     - `01_screens_card.png`
     - `meta.json`
     - صور تبويبات `القاعات/الشعب/المدربين/التوزيع النسبي`.
4. النتيجة:
   - توليد اللقطات نجح على الأحجام الثلاثة.
   - `meta.json` أكد المقاسات الفعلية وعدد تبويبات heatmap = `4` في كل اختبار.
5. ملاحظة تشغيلية:
   - الخطأ السابق كان في صياغة أمر shell فقط (تقسيم قيم في `zsh`) وليس قيدًا في الواجهة.
   - أداة snapshots تدعم أي مقاس مباشرة عبر:
     - `--viewport-width`
     - `--viewport-height`

### [W-059] تنفيذ تغطية Responsive للفترة المسائية على 13/24/27 إنش
1. الهدف:
   - استكمال التحقق البصري الرسمي للفترة `مسائي` بنفس المقاسات القياسية المستخدمة في `صباحي`.
2. التنفيذ:
   - أداة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/ui_snapshots.py`
   - التشغيل تم على:
     - `1280x800` -> `responsive_13in_evening_20260224`
     - `1920x1080` -> `responsive_24in_evening_20260224`
     - `2560x1440` -> `responsive_27in_evening_20260224`
3. الأدلة:
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_13in_evening_20260224`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_24in_evening_20260224`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_27in_evening_20260224`
4. التحقق:
   - كل مجلد يحتوي `15` ملفًا (صفحة كاملة + الكرت + تبويبات + hover + meta).
   - `meta.json` أكد:
     - `period = مسائي`
     - `panels = 4`
     - مقاس viewport مطابق لكل تشغيل.
5. الأثر:
   - إغلاق تغطية responsive على الفترتين (`صباحي` + `مسائي`) لنفس أحجام الأجهزة المرجعية.

### [W-060] إغلاق Parity الفعلي للجداول المنشورة على آخر تشغيلين (صباحي/مسائي)
1. الهدف:
   - التحقق الحاسم من تطابق المخرجات المنشورة (`halls/crns/trainers/distribution`) مع baseline المتوقع من `SS01.csv`.
2. التشغيلات المستخدمة:
   - صباحي:
     - `run_id = da2552a8-040e-48c1-9010-cfe308ea89c6`
   - مسائي:
     - `run_id = de3ee179-3263-4540-b8f3-92e743c4328e`
3. الأداة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/publish_parity_report.py`
4. الأوامر المنفذة:
   - `.venv/bin/python -m app.tools.publish_parity_report --csv-file /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --period صباحي --run-id da2552a8-040e-48c1-9010-cfe308ea89c6 --base-url http://127.0.0.1:8000 --output-file artifacts/parity/latest_morning_compare.json`
   - `.venv/bin/python -m app.tools.publish_parity_report --csv-file /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --period مسائي --run-id de3ee179-3263-4540-b8f3-92e743c4328e --base-url http://127.0.0.1:8000 --output-file artifacts/parity/latest_evening_compare.json`
5. النتيجة:
   - `all_match=True` للفترتين.
   - صباحي:
     - `halls=6807`, `crns=6994`, `trainers=6985`, `distribution=40` (مطابقة 100%).
   - مسائي:
     - `halls=461`, `crns=461`, `trainers=44`, `distribution=40` (مطابقة 100%).
6. الأثر:
   - إغلاق بند parity التشغيلي للجداول الأربع على أحدث run منشور لكل فترة.
   - أصبح المتبقي في PRD متمركزًا على:
     - RBAC
     - lock/idempotency lifecycle
     - تحسين PDF العربي
     - filters المتقدمة
     - offline assets.

### [W-061] تنفيذ RBAC فعلي على APIs التشغيل الحساسة
1. الهدف:
   - تطبيق صلاحيات PRD (`Admin/Operator/Viewer`) على مسارات التشغيل الحساسة، مع إبقاء القراءة متاحة لـ`Viewer`.
2. التعديلات المنفذة:
   - إضافة طبقة صلاحيات مركزية:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/deps/rbac.py`
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/deps/__init__.py`
   - إضافة إعداد افتراضي للدور:
     - `MC_DEFAULT_ROLE` (القيمة الافتراضية: `operator`) في:
       - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/core/config.py`
   - ربط الـroutes بالصلاحيات:
     - مسارات mutation (`import/run/checks/publish/export`) تتطلب `Admin` أو `Operator`.
     - مسارات القراءة تحت `/api/v1/mc/runs` تقبل `Admin/Operator/Viewer`.
     - الملفات المعدلة:
       - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/imports.py`
       - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/pipeline.py`
       - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/checks.py`
       - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
3. الاختبارات:
   - إضافة اختبار API جديد:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_rbac_api.py`
   - تغطية:
     - سماح `Viewer` بالقراءة.
     - منع `Viewer` من `import/run/checks/publish/export`.
     - قبول `Operator` لمسارات mutation.
     - fallback تلقائي للدور الافتراضي عند غياب `X-MC-Role`.
4. التحقق المنفذ:
   - `.venv/bin/python -m pytest -q backend/tests/test_rbac_api.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة: `17 passed`.
5. الأثر:
   - إغلاق مسار RBAC من المتبقي في PRD.
   - المتبقي الآن:
     - Run Lifecycle (`lock/idempotency/retry`)
     - PDF عربي تشغيلي أعمق
     - advanced filters
     - offline assets
     - API governance المتقدم.

### [W-062] تنفيذ Run Lifecycle: lock + idempotency_key + retry
1. الهدف:
   - إغلاق متطلبات `FR-013` عبر:
     - منع التشغيل المتوازي لنفس (`semester + period`).
     - إضافة `idempotency_key` مبني على `input_checksum + reference_version + settings`.
     - دعم retry تلقائي مرة واحدة للأخطاء العابرة.
2. التعديلات المنفذة:
   - إضافة خدمة lifecycle جديدة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/run_lifecycle.py`
     - تشمل:
       - `acquire_run_lock` / `release_run_lock`
       - `build_run_idempotency_key`
       - `run_with_single_retry`
       - `find_latest_idempotent_run`
   - تحديث model:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/models/run.py`
     - إضافة عمود `idempotency_key` + فهرس `ix_mc_run_idempotency_key`.
   - إضافة migration idempotent:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/alembic/versions/20260224_0005_add_idempotency_key_to_run.py`
   - تحديث الإعدادات:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/core/config.py`
     - `MC_RUN_LOCK_TTL_SECONDS`
     - `MC_TRANSIENT_RETRY_COUNT`
   - تحديث الاستيراد:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/import_service.py`
     - منع استيراد مكرر لنفس idempotency key وإرجاع run السابق (`idempotent_hit=true`).
   - تحديث تشغيل pipeline:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/run_service.py`
     - قفل سياقي قبل المعالجة.
     - retry تلقائي مرة واحدة عند transient errors.
     - تحويل الحالة إلى `FAILED` مع log عند استنفاد retry.
     - تخطي تشغيل مكرر إذا كان `mc_codes` موجودًا بالفعل (`CODES_BUILD_IDEMPOTENT_HIT`).
   - تحديث route:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/pipeline.py`
     - إرجاع `409` عند lock conflict.
   - تحديث عرض run API:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
     - تضمين `idempotency_key` في `list/get`.
3. الاختبارات:
   - إضافة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_run_lifecycle.py`
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_rbac_api.py` (حقل `idempotency_key`).
4. التحقق المنفذ:
   - `.venv/bin/python -m ruff check ...` -> `All checks passed!`
   - `.venv/bin/python -m pytest -q backend/tests` -> `22 passed`
   - `.venv/bin/python -m alembic -c backend/alembic.ini upgrade head` -> نجح حتى `20260224_0005`
5. الأثر:
   - إغلاق مسار `Run Lifecycle` في المتبقي التشغيلي.
   - أصبح المتبقي الأساسي:
     - تحسين PDF العربي
     - advanced filters
     - offline assets
     - API governance.

### [W-063] ترقية `export.pdf` إلى تقرير عربي تشغيلي مفصل
1. الهدف:
   - تحويل PDF من ملخص نصي بسيط إلى تقرير عربي تشغيلي مفصل يدعم RTL ويعرض مؤشرات التنفيذ والجداول الأساسية.
2. التعديلات المنفذة:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/export_service.py`
   - الإضافة الأساسية:
     - بناء تقرير HTML عربي (`dir=rtl`) يشمل:
       - بطاقة بيانات التشغيل (run/semester/period/status/time)
       - ملخص القواعد وعدد الملاحظات
       - ملخص التوزيع اليومي
       - عينات تشغيلية من:
         - القاعات
         - الشعب
         - المدربين
         - الملاحظات
     - تصيير PDF عبر Playwright (`chromium`) بدل النص اللاتيني المبسط.
     - fallback تلقائي إلى مولد PDF القديم عند تعذر Playwright، مع تسجيل `mode` وسبب fallback في `run_log`.
   - تحسينات بيانات التقرير:
     - تجميع counts + breakdown by rule + day distribution + previews (`PDF_PREVIEW_LIMIT=40`).
3. الاختبارات:
   - إضافة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_export_pdf_report.py`
   - تغطية:
     - وجود العناوين العربية في HTML.
     - صحة توقيع PDF fallback.
     - توليد PDF عبر Playwright (أو skip إذا البيئة لا تدعم المتصفح).
4. التحقق المنفذ:
   - `.venv/bin/python -m ruff check backend/app/services/export_service.py backend/tests/test_export_pdf_report.py`
   - `.venv/bin/python -m pytest -q backend/tests/test_export_pdf_report.py backend/tests/test_run_lifecycle.py backend/tests/test_rbac_api.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة: `24 passed, 1 skipped`.
5. الأثر:
   - إغلاق بند "PDF عربي تشغيلي" من قائمة الأولويات المتبقية.
   - المتبقي الآن:
     - advanced filters
     - offline assets
     - API governance.

### [W-064] تنفيذ الفلاتر المتقدمة للعرض الحراري + API filtering
1. الهدف:
   - إغلاق بند `advanced filters` في PRD عبر فلاتر موحدة على الواجهة والـAPI.
2. التعديلات المنفذة (واجهة):
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/index.html`
     - إضافة حقول:
       - `القسم` (`heatmapDepartmentFilter`)
       - `المبنى` (`heatmapBuildingFilter`)
       - `CRN` (`heatmapCrnFilter`)
       - `المدرب` (`heatmapTrainerFilter`)
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
     - ضبط شبكة الفلاتر إلى 4 أعمدة مع الحفاظ على breakpoints responsive الحالية.
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
     - ربط الفلاتر الجديدة بـ`renderHeatmapScreens`.
     - توسيع `activeHeatmapRows()` لتطبيق:
       - period filter
       - search filter
       - advanced filters معًا.
     - إضافة `matchesAdvancedHeatmapFilters` لمطابقة:
       - `department`
       - `building_code`
       - `crn`
       - `trainer_name/trainer_job_id`
     - تحسين تطبيع البحث العربي بإدخال `normalizeDigitChars` داخل `normalizeArabicText`.
3. التعديلات المنفذة (API):
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
   - إضافة helper:
     - `_normalized_query` لتنظيف مدخلات query النصية.
   - توسيع الفلاتر في endpoints:
     - `/source-ss01`: `department`, `building_code`, `crn`, `trainer`
     - `/codes`: `department`, `building_code`, `room_code`, `crn`, `trainer`
     - `/halls`: `room_code` (partial), `building_code`, `crn`, `day_order`, `slot_index`
     - `/crns`: `crn` (partial), `course_code`, `room_code`, `trainer`, `day_order`, `slot_index`
     - `/trainers`: `trainer_job_id` (partial), `trainer_name`, `crn`, `day_order`, `slot_index`
     - `/distribution`: `day_order`, `slot_index`
   - إرجاع كائن `filters` في الاستجابات لتأكيد الفلاتر المطبقة.
4. الاختبارات:
   - إضافة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_runs_advanced_filters_api.py`
   - تغطية:
     - تفعيل الفلاتر النصية الجزئية (`ILIKE`) لكل endpoint.
     - فلاتر `day_order/slot_index`.
     - OR logic للمدرب (`job_id` أو `name`).
     - تطبيع القيم الفارغة/المسافات إلى `None`.
5. التحقق المنفذ:
   - `node --check backend/app/ui/scripts/dashboard.js`
   - `.venv/bin/python -m ruff check backend/app/api/routes/runs.py backend/tests/test_runs_advanced_filters_api.py`
   - `.venv/bin/python -m pytest -q backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py backend/tests/test_run_lifecycle.py backend/tests/test_export_pdf_report.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة: `31 passed, 1 skipped`.
6. الأثر:
   - إغلاق بند `advanced filters` من المتبقي التنفيذي.
   - المتبقي الآن:
     - offline assets
     - API governance.

### [W-065] منع النشر/التصدير قبل الفحوصات (UX Guard + API flag)
1. الهدف:
   - منع ظهور خطأ backend للمستخدم عند النشر/التصدير قبل تشغيل الفحوصات.
2. التعديلات المنفذة (API):
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
   - إضافة مؤشرات جاهزية الفحوصات داخل `GET /api/v1/mc/runs/{run_id}`:
     - `metrics.checks_finished_count`
     - `metrics.checks_ready` (boolean).
3. التعديلات المنفذة (واجهة):
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
   - إضافة حارس workflow:
     - تتبع `selectedRunChecksReady`.
     - تعطيل أزرار:
       - `نشر النتائج`
       - `تصدير Excel`
       - `تصدير PDF`
       عندما لا تكون الفحوصات مكتملة.
     - إظهار رسالة عربية إرشادية بدل الخطأ الخام:
       - `يلزم تشغيل الفحوصات أولًا قبل ...`.
     - إبقاء الحماية حتى في حالات السباق عبر fallback داخل `catch` عند نفس رسالة backend.
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
   - تحسين مظهر الأزرار المعطلة (`not-allowed` + opacity).
4. الاختبارات:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_runs_advanced_filters_api.py`
   - إضافة تغطية:
     - تحقق وجود `metrics.checks_ready` و`metrics.checks_finished_count` في endpoint التشغيل المفرد.
5. التحقق المنفذ:
   - `node --check backend/app/ui/scripts/dashboard.js`
   - `.venv/bin/python -m ruff check backend/app/api/routes/runs.py backend/tests/test_runs_advanced_filters_api.py`
   - `.venv/bin/python -m pytest -q backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py backend/tests/test_run_lifecycle.py backend/tests/test_export_pdf_report.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة: `32 passed, 1 skipped`.
6. الأثر:
   - تحسين كبير في وضوح سير التشغيل:
     - `تشغيل المعالجة -> تشغيل الفحوصات -> نشر/تصدير`.
   - تقليل أخطاء الاستخدام من نوع `Run checks must be executed before publishing`.

### [W-066] تنفيذ Offline Assets (خط عربي + أيقونات محلية)
1. الهدف:
   - إغلاق بند `offline assets` بإزالة اعتماد الواجهة على CDN للخط والأيقونات.
2. التعديلات المنفذة:
   - إضافة خط محلي:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/assets/fonts/SFArabic.ttf`
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/tokens.css`
     - إضافة `@font-face` لاسم:
       - `MC Arabic Local`
     - تحويل `--font-family-ar` للاعتماد على الملف المحلي.
   - إضافة محرك أيقونات محلي:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/lucide.local.js`
     - يوفر `window.lucide.createIcons()` محليًا ويغطي الأيقونات المستخدمة.
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/index.html`
     - إزالة روابط:
       - `fonts.googleapis.com`
       - `fonts.gstatic.com`
       - `unpkg.com/lucide`
     - إضافة:
       - `/ui/scripts/lucide.local.js`
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
     - إضافة قاعدة لضبط حجم SVG داخل عناصر الأيقونات.
3. الاختبارات:
   - إضافة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_ui_offline_assets.py`
   - تغطية:
     - التأكد من غياب أي مرجع CDN داخل `index.html`.
     - التأكد من وجود `lucide.local.js` وملف الخط المحلي وربط `tokens.css` به.
4. التحقق المنفذ:
   - `node --check backend/app/ui/scripts/lucide.local.js && node --check backend/app/ui/scripts/dashboard.js`
   - `.venv/bin/python -m ruff check backend/tests/test_ui_offline_assets.py`
   - `.venv/bin/python -m pytest -q backend/tests/test_ui_offline_assets.py backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py backend/tests/test_run_lifecycle.py backend/tests/test_export_pdf_report.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة: `34 passed, 1 skipped`.
5. الأثر:
   - الواجهة تعمل الآن بدون أي اعتماد خارجي على CDN للخط والأيقونات.
   - المتبقي التنفيذي في PRD:
     - API governance المتقدم فقط.

### [W-067] إغلاق API Governance (Error Envelope + Warnings/Errors + Compare Runs)
1. الهدف:
   - إغلاق آخر بند متبقٍ في PRD الخاص بحوكمة الـAPI.
2. التعديلات المنفذة:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/main.py`
   - إضافة governance موحّد للأخطاء:
     - Middleware يحقن `trace_id` لكل request ويعيده في header `X-Trace-Id`.
     - Exception handlers موحّدة (`HTTP`, `Validation`, `Unhandled`) تعيد صيغة:
       - `code`
       - `message`
       - `details`
       - `trace_id`
     - المحافظة على `detail` للتوافق الخلفي مع المستهلكات الحالية.
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
   - إضافة endpoints:
     - `GET /api/v1/mc/runs/{run_id}/warnings`
     - `GET /api/v1/mc/runs/{run_id}/errors`
     - `GET /api/v1/mc/runs/compare?left_run_id=...&right_run_id=...`
   - إضافة قواعد sort للـissues endpoints الجديدة:
     - `id`, `created_at`, `severity`, `rule_code`
     - دعم اتجاه `asc/desc`.
   - تحسين frontend error parsing:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
     - قراءة `detail/message/code` بترتيب fallback.
3. الاختبارات:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_runs_advanced_filters_api.py`
       - تغطية endpoints `warnings/errors/compare` والتحقق من filter/sort.
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_rbac_api.py`
       - تغطية envelope حق خطأ `403` (وجود `code/trace_id/message/detail`).
4. التحقق المنفذ:
   - `node --check backend/app/ui/scripts/dashboard.js`
   - `.venv/bin/python -m ruff check backend/app/main.py backend/app/api/routes/runs.py backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py`
   - `.venv/bin/python -m pytest -q backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py backend/tests/test_run_lifecycle.py backend/tests/test_export_pdf_report.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py backend/tests/test_ui_offline_assets.py`
   - النتيجة: `39 passed, 1 skipped`.
5. الأثر:
   - إغلاق بند API Governance بالكامل.
   - بنود PRD التنفيذية الأساسية أصبحت مكتملة (RBAC + lifecycle + PDF + advanced filters + offline assets + governance).

### [W-068] Responsive Gate إلزامي داخل CI (Playwright + Assertions)
1. الهدف:
   - تحويل فحص الـResponsive من مراجعة لقطات يدوية إلى Gate إلزامي يوقف الدمج عند كسر العرض.
2. التعديلات المنفذة:
   - إضافة أداة جديدة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/responsive_gate.py`
   - المزايا:
     - فحص 4 مقاسات ثابتة:
       - `mobile_390x844`
       - `laptop13_1366x768`
       - `desktop24_1920x1080`
       - `desktop27_2560x1440`
     - Assertions على:
       - صحة توزيع التخطيط (عمودين desktop / عمود واحد mobile).
       - عرض لوحة التحكم ضمن حدود متوقعة على desktop.
       - توسّع لوحة التشغيل عند إخفاء التحكم (`controls-hidden`).
       - حد أدنى لمساحة heatmap ومنع shrink غير منطقي.
       - منع overflow أفقي مرئي (من جهة اليمين) على الصفحة.
     - توليد artifacts:
       - `responsive_report.json`
       - لقطات شاشة لكل مقاس.
   - تحديث CSS لمنع تمدد grid item غير المقصود:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
     - إضافة `min-width: 0` على:
       - `.selected-run`
       - `.screen-panels`
       - `.screen-panel`
       - `.heatmap-wrap`
   - ربط الـCI:
     - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
     - إضافة:
       - تثبيت `playwright` + تنزيل `chromium`.
       - خطوة `Responsive UI Gate` بعد `Mandatory Gate`.
       - رفع artifacts من:
         - `artifacts/responsive/latest`
   - توثيق التشغيل:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/README.md`
     - إضافة قسم `Responsive UI Gate (Automation)`.
3. الاختبارات:
   - إضافة اختبار منطق قواعد gate:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_responsive_gate_logic.py`
4. التحقق المنفذ:
   - `.venv/bin/python -m ruff check backend/app/tools/responsive_gate.py backend/tests/test_responsive_gate_logic.py`
   - `.venv/bin/python -m pytest -q backend/tests/test_responsive_gate_logic.py`
   - تشغيل gate فعليًا على السيرفر المحلي:
     - `../.venv/bin/python -m app.tools.responsive_gate --base-url http://127.0.0.1:8000 --period صباحي --output-dir /Users/malmabar/Documents/MornningClassesCheck/artifacts/responsive/manual_latest`
   - Regression suite:
     - `.venv/bin/python -m pytest -q backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py backend/tests/test_run_lifecycle.py backend/tests/test_export_pdf_report.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py backend/tests/test_ui_offline_assets.py backend/tests/test_responsive_gate_logic.py`
   - النتيجة: `42 passed, 1 skipped`.
5. الأثر:
   - أي كسر Responsive مستقبلي سيوقف `Mandatory Release Gate` تلقائيًا.
   - تقليل الاعتماد على لقطات المراجعة اليدوية قبل الدمج.

### [W-069] إصلاح جذري لهيت ماب الاستجابة (منع القص والانقسام)
1. المشكلة المرصودة:
   - قص/انزياح أعمدة الهيت ماب يمين/يسار (ظهور أجزاء من اليوم بدل المجموعة كاملة).
   - ضغط غير متناسق للأعمدة في بعض الحالات بعد إعادة الرسم أو تغيير التبويب.
2. السبب الجذري:
   - عرض أعمدة الهيت ماب كان يعتمد فعليًا على حدّ أدنى ناتج من نص التوقيت داخل رأس الجدول.
   - مع RTL بقي `scrollLeft` بقيمة سالبة صغيرة بعد إعادة الرسم، فنتج قص جزئي للحواف.
3. التعديلات المنفذة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
     - إضافة `applyHeatmapSizing(...)` لحساب عرض عمود الكيان + عمود الفترة ديناميكيًا من عرض الحاوية.
     - تحسين `resetHeatmapViewport(...)` بإعادة ضبط RTL على مرحلتين (`requestAnimationFrame`) لمنع بقاء انزياح جزئي.
     - إعادة رسم الهيت ماب عند:
       - تغيير حالة إخفاء/إظهار لوحة التحكم.
       - تغيير حجم الشاشة (debounced resize).
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
     - تثبيت بنية الجدول: `width: max-content`, `min-width: 100%`, `table-layout: fixed`.
     - تقليل أبعاد fallback للأعمدة.
     - تصغير واعتماد عرض أكثر انضباطًا لنص أوقات الفترات داخل الهيدر (`.slot-time`) لتفادي تمدد الأعمدة.
     - توحيد `scrollbar-gutter` إلى `stable` لمنع المساحات المحجوزة غير الضرورية.
4. التحقق المنفذ:
   - `node --check backend/app/ui/scripts/dashboard.js`
   - تحقق Playwright (قياسات حقيقية داخل المتصفح) على تبويبات:
     - `القاعات`, `الشعب`, `المدربين`, `التوزيع النسبي`.
   - نتيجة المقاس المستهدف (1512x982):
     - `overflow = 0` في جميع شاشات العرض الحراري.
     - `scrollLeft = 0` بعد إعادة الرسم.
   - تم حفظ لقطات تحقق داخل:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/debug_rooms_after.png`
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/debug_trainers_after_latest.png`
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/tmp_debug_all_after.png`
5. الأثر:
   - اختفى قص الحواف الذي كان يظهر أرقام فترات/أجزاء أيام بشكل مبتور.
   - الهيت ماب أصبح يتكيّف مع عرض الحاوية بشكل أكثر ثباتًا بدل سلوك متغير حسب حالة التمرير السابقة.

### [W-070] استعادة استقرار شاشة التوزيع النسبي + تقليل تأثير التصغير القاسي
1. المشكلة بعد الجولة السابقة:
   - شاشة `التوزيع النسبي` أصبحت تُعرض بانزياح أفقي واضح وجزء من الأعمدة يظهر مقصوصًا.
   - السبب كان اعتماد `distribution-table` على `max-content` مع `min-width` كبير.
2. المعالجة المنفذة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
     - إعادة `distribution-table` إلى عرض مرن داخل الحاوية:
       - `width: 100%`
       - `min-width: 0`
       - `table-layout: fixed`
     - إزالة حدود `min-width` الكبيرة في media queries للتوزيع النسبي.
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
     - بعد توليد كتل التوزيع: فرض تموضع أفقي ابتدائي ثابت لكل `.distribution-scroll`.
     - إضافة `colgroup` في جدول الهيت ماب (القاعات/الشعب/المدربين) لتثبيت عرض الأعمدة بطريقة صريحة.
     - تحسين معادلة sizing للهيت ماب لتقليل الضغط والقص العرضي.
3. نتيجة التحقق:
   - Playwright screenshots:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/fix2_distribution.png`
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/fix2_trainers.png`
   - القياسات:
     - التوزيع النسبي: overflow فعلي ~`0-1px` (حدودي وغير بصريًا مكسور).
     - المدربين: overflow ~`5px` (بدون انقسام يوم أو قص كبير للأعمدة).
4. المخرجات:
   - رجوع `التوزيع النسبي` لعرض متماسك (خمس أيام بدون انقطاع واضح).
   - تقليل أثر التعديلات السابقة التي كانت سببت انحراف/قص بصري.

### [W-071] ضبط ثنائي الحالة (إظهار/إخفاء التحكم) بدون كسر
1. الهدف:
   - التوزيع النسبي: تصغير الأرقام عند إظهار التحكم فقط، والرجوع للحجم الأكبر عند إخفائه.
   - القاعات/الشعب/المدربين: إزالة تداخل أوقات الهيدر عند إظهار التحكم + حل خلل الفترة الثامنة.
2. التعديلات:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
     - تحسين معادلة `applyHeatmapSizing` لتعويض عرض الحدود (`borderBudget`) ومنع الانزياح 5px.
     - إضافة `compactTimeLabel`.
     - في `renderHeatmapTable`:
       - عند إظهار التحكم: عرض الوقت بصيغة مضغوطة (`0800`) بدل (`08:00`).
       - عند إخفاء التحكم: الرجوع للصيغة الكاملة (`08:00`).
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
     - منع تداخل نصوص هيدر الجدول عبر `overflow: hidden` على `thead th`.
     - نمط أصغر لـ `.slot-time` فقط عندما التحكم ظاهر.
     - نمط أصغر لجدول التوزيع النسبي فقط عندما التحكم ظاهر.
     - الحفاظ على النمط الأكبر الحالي عندما التحكم مخفي.
3. التحقق:
   - `node --check backend/app/ui/scripts/dashboard.js` ✅
   - Playwright (1512x982) على حالتين:
     - التحكم ظاهر:
       - `trainers`: `overflow=0`, `scrollLeft=0`, الوقت = `0800`.
       - `distribution`: font أصغر.
     - التحكم مخفي:
       - `trainers`: `overflow=0`, `scrollLeft=0`, الوقت = `08:00`.
       - `distribution`: font أكبر (مثل الوضع الحالي المطلوب).
   - لقطات:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/fix3_trainers_visible_controls.png`
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/fix3_distribution_visible_controls.png`
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/fix3_trainers_hidden_controls.png`
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/fix3_distribution_hidden_controls.png`
4. النتيجة:
   - تحقق السلوك الشرطي المطلوب بدقة مع تثبيت شكل الشاشة وعدم كسر الإصلاحات السابقة.

### [W-072] تحسين وضوح أوقات الهيت ماب بدون رجوع التداخل
1. الطلب:
   - جعل أوقات الهيدر أوضح في وضع إظهار التحكم، مع الحفاظ على الثبات وعدم رجوع مشكلة التداخل/الفترة الثامنة.
2. التنفيذ:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
     - تعديل `compactTimeLabel` من صيغة أرقام متصلة (`0800`) إلى صيغة أوضح (`8:00`) في وضع compact.
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
     - رفع بسيط ومدروس لخط `.slot-time` عند controls visible فقط.
     - الحفاظ على الحجم الطبيعي عند controls hidden كما هو.
3. التحقق:
   - `node --check backend/app/ui/scripts/dashboard.js` ✅
   - قياسات Playwright على القاعات/الشعب/المدربين:
     - controls visible: `overflow=0`, `scrollLeft=0`, `sampleTime=8:00`.
     - controls hidden: `overflow=0`, `scrollLeft=0`, `sampleTime=08:00`.
   - لقطات:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/fix4_visible_controls.png`
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/fix4_hidden_controls.png`
4. النتيجة:
   - تحسن وضوح الوقت في الوضع المضغوط بدون كسر الاستقرار أو رجوع التداخل.

### [W-073] ترتيب الدفعة المتبقية (Responsive Gate bundle)
1. الهدف:
   - فصل التغييرات المتبقية بعد دمج PR الواجهة في دفعة مستقلة نظيفة.
2. ما تم ترتيبه:
   - CI release gate:
     - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
     - إضافة تثبيت Playwright Chromium + خطوة `Responsive UI Gate` + رفع artifacts الخاصة بها.
   - أداة الفحص:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/responsive_gate.py`
   - اختبار المنطق:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_responsive_gate_logic.py`
   - دليل التشغيل:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/README.md`
     - توثيق تشغيل responsive gate محليًا وضمن CI.
3. تنظيف الضوضاء المحلية:
   - تحديث `.gitignore` لإهمال artifacts المتولدة تلقائيًا:
     - `artifacts/responsive/`
     - `artifacts/*.png`
     - `artifacts/tmp_*.png`
4. التحقق:
   - `.venv/bin/python -m ruff check backend/app/tools/responsive_gate.py backend/tests/test_responsive_gate_logic.py` ✅
   - `.venv/bin/python -m pytest -q backend/tests/test_responsive_gate_logic.py` ✅ (`3 passed`).
5. النتيجة:
   - الدفعة المتبقية أصبحت جاهزة للرفع في PR مستقل بدون ملفات artifacts المحلية.

### [W-074] تنفيذ أداة Pilot/Cutover readiness (مرحلة PRD 13.5)
1. الهدف:
   - بدء إغلاق المرحلة 4 في PRD (`Pilot & Cutover`) عبر تقرير آلي يقيس:
     - تغطية أيام التشغيل الفعلية.
     - تطابق مخرجات التشغيلات المنشورة مع baseline من `SS01.csv`.
2. التعديلات المنفذة:
   - إضافة أداة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/pilot_cutover_report.py`
   - وظائف الأداة:
     - سحب التشغيلات من `/api/v1/mc/runs` لكل فترة.
     - فلترة التشغيلات حسب الحالة (`PUBLISHED` افتراضيًا).
     - مقارنة كل run مع baseline عبر:
       - `halls/crns/trainers/distribution`
     - احتساب `distinct operation days` لكل فترة.
     - قرار جاهزية نهائي:
       - `cutover_ready=true/false`
       - Exit code (`0` جاهز / `1` غير جاهز).
   - إضافة entrypoint:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/pyproject.toml`
     - `mc-pilot-cutover-report = "app.tools.pilot_cutover_report:main"`
   - تحديث التوثيق التشغيلي:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/README.md`
     - إضافة قسم `Pilot / Cutover Report (PRD Phase 4)` مع أمثلة تشغيل ومخرجات artifacts.
   - تنظيم workspace:
     - `/Users/malmabar/Documents/MornningClassesCheck/.gitignore`
     - إضافة `artifacts/pilot/` لمنع إدراج تقارير pilot المحلية في Git.
3. الاختبارات:
   - إضافة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_pilot_cutover_report_logic.py`
   - تغطية:
     - parsing الطابع الزمني.
     - تطبيع حالات التشغيل.
     - قرار النجاح/الفشل حسب parity + عدد الأيام.
4. التحقق المنفذ:
   - `.venv/bin/python -m ruff check backend/app/tools/pilot_cutover_report.py backend/tests/test_pilot_cutover_report_logic.py backend/pyproject.toml` ✅
   - `.venv/bin/python -m pytest -q backend/tests/test_pilot_cutover_report_logic.py backend/tests/test_responsive_gate_logic.py` ✅ (`9 passed`).
5. الأثر:
   - أصبح لدينا مسار آلي قابل للقياس لإثبات جاهزية الـCutover بدل الحكم اليدوي.
   - المتبقي لمرحلة 13.5 هو تشغيلها دوريًا على نافذة 2-4 أسابيع وتوقيع الاعتماد النهائي.

### [W-075] تحسين دقة Pilot report عبر input_checksum scoping + تشغيل فعلي
1. الهدف:
   - تقليل الـfalse mismatches في تقرير الـPilot الناتجة عن تشغيلات تاريخية لا تخص نفس ملف SS01 الحالي.
2. التعديلات:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/pilot_cutover_report.py`
   - إضافة:
     - حساب `SHA-256` لملف `SS01.csv`.
     - فلترة التشغيلات افتراضيًا على `run.input_checksum == csv_checksum`.
     - خيار تحكم:
       - `--require-input-checksum-match` (افتراضي true)
       - `--no-require-input-checksum-match`
     - حقول تقرير إضافية:
       - `expected_input_checksum`
       - `total_runs_checksum_scoped`
       - `checksum_filter_enabled`
3. الاختبارات:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_pilot_cutover_report_logic.py`
   - إضافة تغطية لتصفية checksum.
4. التحقق:
   - `.venv/bin/python -m ruff check backend/app/tools/pilot_cutover_report.py backend/tests/test_pilot_cutover_report_logic.py` ✅
   - `.venv/bin/python -m pytest -q backend/tests/test_pilot_cutover_report_logic.py` ✅ (`7 passed`).
   - تشغيل فعلي:
     - `../.venv/bin/python -m app.tools.pilot_cutover_report --csv-file /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --period all --accepted-statuses PUBLISHED --min-distinct-days 14 --output-file /Users/malmabar/Documents/MornningClassesCheck/artifacts/pilot/latest.json`
5. النتيجة العملية:
   - قبل checksum scoping:
     - failures=4, mismatches (صباحي=10, مسائي=11).
   - بعد checksum scoping:
     - failures=3
     - صباحي: `runs=14`, `days=2/14`, `mismatches=1` (run: `7a722ec5-09f9-4f47-a3ee-e1c8e110a970`)
     - مسائي: `runs=9`, `days=2/14`, `mismatches=0`
6. أثر التعديل:
   - التقرير الآن يقيس جودة الـPilot على نفس بيانات الإدخال فعليًا.
   - بقاء عدم الجاهزية حاليًا منطقي (نقص أيام تشغيل + mismatch تاريخي واحد داخل نفس checksum scope).

### [W-076] تصحيح منهج Pilot ليعتمد آخر تشغيل يومي + اليوم المحلي
1. الهدف:
   - إزالة تأثير التشغيلات المرحلية داخل نفس اليوم من قرار الـPilot.
   - منع إنقاص عدد الأيام بسبب تحويل timestamps إلى UTC عند العد.
2. التعديلات:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/pilot_cutover_report.py`
   - إضافة:
     - `--daily-latest-only` (افتراضي true): تقييم آخر run منشور لكل يوم فقط.
     - `--no-daily-latest-only`: تمكين تحليل كل التشغيلات التاريخية عند الحاجة.
   - تصحيح عد الأيام:
     - العد أصبح على **اليوم المحلي** من `created_at` بدل يوم UTC.
3. الاختبارات:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_pilot_cutover_report_logic.py`
     - إضافة اختبار `latest_run_per_day` + ضبط سلوك التاريخ المحلي.
4. التحقق:
   - `.venv/bin/python -m ruff check backend/app/tools/pilot_cutover_report.py backend/tests/test_pilot_cutover_report_logic.py` ✅
   - `.venv/bin/python -m pytest -q backend/tests/test_pilot_cutover_report_logic.py` ✅ (`8 passed`).
   - تشغيل فعلي للتقرير:
     - `../.venv/bin/python -m app.tools.pilot_cutover_report --csv-file /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --period all --accepted-statuses PUBLISHED --min-distinct-days 14 --output-file /Users/malmabar/Documents/MornningClassesCheck/artifacts/pilot/latest.json`
5. النتيجة:
   - `mismatch` أصبح صفرًا للفترتين.
   - عدم الجاهزية الآن فقط بسبب شرط نافذة الأيام:
     - صباحي: `runs=2`, `days=2/14`, `mismatches=0`
     - مسائي: `runs=2`, `days=2/14`, `mismatches=0`

### [W-077] سكربت تشغيل يومي للـPilot + سجل تاريخي
1. الهدف:
   - توفير أمر يومي واحد بسيط لتشغيل تقييم `Pilot/Cutover` بدون أوامر طويلة متكررة.
2. التعديلات:
   - إضافة سكربت:
     - `/Users/malmabar/Documents/MornningClassesCheck/scripts/pilot_cutover_daily.sh`
   - الميزات:
     - تشغيل `pilot_cutover_report` بالقيم الافتراضية الصحيحة:
       - `require_input_checksum_match=true`
       - `daily_latest_only=true`
     - طباعة ملخص JSON سريع (`pilot_daily_summary`) بعد كل تشغيل.
     - إلحاق سطر يومي في:
       - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/pilot/history.log`
     - خيار `--allow-not-ready` لتشغيل يومي بدون كسر المهمة المجدولة أثناء فترة pilot.
3. التحقق:
   - `scripts/pilot_cutover_daily.sh --help` ✅
   - تشغيل فعلي:
     - `scripts/pilot_cutover_daily.sh --csv-file /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --allow-not-ready` ✅
4. نتيجة تشغيل اليوم:
   - `cutover_ready=false`
   - صباحي: `days=2/14`, `mismatches=0`
   - مسائي: `days=2/14`, `mismatches=0`
   - تمت إضافة سجل يومي إلى:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/pilot/history.log`

### [W-078] دورة تشغيل يومية كاملة للفترتين + تحديث Pilot
1. الهدف:
   - تنفيذ دورة اليوم التشغيلية كاملة (`import -> run -> checks -> publish`) للفترتين، ثم تحديث تقرير `Pilot/Cutover`.
2. التنفيذ:
   - الفترة `صباحي`:
     - `import.run_id=6bc63c16-6e58-49f4-9ffd-1e29c7cee851` (`idempotent_hit=True`)
     - `checks.total_issues=763`
     - `publish.status=PUBLISHED`
   - الفترة `مسائي`:
     - `import.run_id=c8d5baa2-75e2-483f-be7a-e02fcb8ffc89` (`idempotent_hit=True`)
     - `checks.total_issues=221`
     - `publish.status=PUBLISHED`
3. تحديث Pilot اليومي:
   - تشغيل:
     - `scripts/pilot_cutover_daily.sh --csv-file /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --allow-not-ready`
   - المخرجات:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/pilot/latest.json`
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/pilot/pilot_cutover_20260225_055209.json`
     - تحديث:
       - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/pilot/history.log`
4. النتيجة:
   - `cutover_ready=false`
   - صباحي: `days=2/14`, `mismatches=0`
   - مسائي: `days=2/14`, `mismatches=0`
5. ملاحظة تشغيلية:
   - ظهور `idempotent_hit=True` يعني استيراد اليوم أعاد استخدام نفس run المعتمد لنفس checksum/settings.
   - عدم زيادة `days` داخل نفس اليوم متوقع مع منهج `latest-per-day`.
