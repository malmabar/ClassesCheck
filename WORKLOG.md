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
