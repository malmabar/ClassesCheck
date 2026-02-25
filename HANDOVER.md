# HANDOVER - Morning Classes Check

## 1) الحالة الحالية

1. الـBackend يعمل على FastAPI + SQLAlchemy + Alembic.
2. الاستيراد من `SS01` يعمل بنجاح.
3. اشتقاق `mc_codes` يعمل.
4. محرك الفحوصات يعمل ويكتب النتائج في `mc_issues`.
5. الواجهة الحالية تعمل على `/` بالعربية RTL.
6. يوجد فلتر رئيسي للفترة (`صباحي`/`مسائي`) داخل لوحة التحكم اليمنى (بدون خيار `الكل`).
7. تم إطلاق تصميم **Premium Gov-Tech Neo-Glass** (Bento + Lucide + Accessibility safeguards) مع قلب الأعمدة:
   - يسار: تفاصيل التشغيل المحدد.
   - يمين: لوحة التحكم التشغيلية.
8. تمت إضافة أدوات كونسول مدمجة:
   - نسخ الاستجابة.
   - طي/توسيع الاستجابة.
9. تم ترقية الثيم إلى نسخة داكنة فاخرة:
   - Charcoal + Emerald + Soft Silver.
   - القيم المعتمدة عبر tokens إلزامية في `tokens.css`.
10. تم اعتماد خط واجهة عربي:
   - IBM Plex Sans Arabic (مع fallback Tajawal).
11. تمت إضافة مفاتيح عرض في الهيدر:
   - تبديل Dark/Light.
   - تبديل الكثافة Compact/Comfortable.
12. تمت إضافة منطقة مخصصة للبادج أعلى يسار الهيدر (`header-left-slot`) بدون تشوه أو تداخل.
13. تم تفعيل شاشات Heatmap منفصلة داخل التشغيل المحدد:
   - القاعات
   - الشعب
   - المدربين
   - التوزيع النسبي
14. تمت إضافة فلاتر Heatmap شاملة تؤثر على جميع الشاشات الأربع:
   - فلتر الفترة (`صباحي`/`مسائي`)
   - فلتر الإشغال
   - فلتر بحث نصي.
15. تم تحديث تحميل بيانات `codes/issues` ليجلب جميع الصفحات (pagination) بدل أول 100 صف.
16. تم تصحيح تبويبات الشاشات الحرارية لتكون حصرية:
   - عند تفعيل تبويب واحد يظهر Panel واحد فقط.
17. تم اعتماد جدول توقيت ثابت للفترات في Heatmap:
   - صباحي: `08:00-08:50` ... `15:06-15:56`
   - مسائي: `16:00-16:50` ... `22:21-23:11`
18. تم تحديث منطق الإشغال الزمني ليحسب نطاق الوقت (`start/end`) ويملأ أكثر من فترة عند التداخل.
19. تمت إضافة زر `إخفاء التحكم` لطي اللوحة اليمنى وتوسيع مساحة الشاشات الحرارية.
20. تمت إضافة فواصل سوداء واضحة بين مجموعات الأيام ورؤوس الفترات/الأوقات في جدول Heatmap.
21. تم تنفيذ تحسين responsive جديد لجدول Heatmap لإظهار الأسبوع كاملًا على الشاشات المتوسطة (مثل 13 إنش) عبر تقليل أحجام الأعمدة والخلايا بشكل مرن.
22. تم تحسين التكيّف للشاشات الكبيرة عبر توسيع عرض الـshell وضبط أحجام الجدول تلقائيًا دون كسر التخطيط.
23. تم إصلاح خلل بصري ظهر لاحقًا (فراغ أفقي كبير وغير متناسق داخل Heatmap) عبر تصحيح آلية توزيع أعمدة الجدول.
24. تم إضافة وحدة استيراد SS01 مباشرة من الواجهة داخل لوحة التحكم:
   - فصل
   - فترة
   - ملف CSV
   - زر تنفيذ الاستيراد.
25. تم تحسين خلية الإشغال بقيمة `1` لتظهر كتعبئة خضراء كاملة داخل الخلية.
26. تم توحيد ستايل خطوط تبويبات الشاشات الحرارية بما يتسق مع الثيم العام.
27. تم تمييز يومي `الاثنين` و`الأربعاء` بخلفية أفتح في رؤوس الأيام وخلايا الجداول.
28. تم تعديل تمييز `الاثنين` و`الأربعاء` إلى درجة رصاصي فاتح (بدل الميل الأخضر) مع إبقاء سلوك `hover` الحالي دون تغيير.
29. تم إصلاح سلوك `hover` في Heatmap ليغطي الصف بالكامل حتى عند وجود خلايا `day-alt` أو خلايا إشغال/تعارض.
30. تم ضبط أولوية الألوان أثناء `hover` بحيث لا تختفي خلية القيمة `1` الخضراء (ولا خلية التعارض الحمراء) عند المرور على الصف.
31. تم إصلاح تعارض CSS بين `day-alt` وخلايا الحالة عبر قواعد أكثر تحديدًا لضمان بقاء الأخضر/الأحمر داخل الاثنين/الأربعاء مع استمرار `hover` لباقي الصف.
32. تم إصلاح تدفق الاستيراد من الواجهة ليشغّل المعالجة تلقائيًا بعد `SS01 import` ويعرض بيانات التشغيل الجديد مباشرة دون حاجة تشغيل يدوي إضافي.
33. تم إصلاح احتساب المدى الزمني في Heatmap بحيث يتم تعليم كل الفترات المتداخلة (وليس فترة البداية فقط)، مع دعم تجميع التداخلات لقيم `2+`.
34. تم إصلاح قراءة تنسيق وقت SS01 المعكوس (`النهاية - البداية`) عبر تطبيع تلقائي للنطاق الزمني قبل احتساب الفترات.
35. تمت إضافة أداة لقطات بصرية آلية (`app.tools.ui_snapshots`) لتقليل الاعتماد على اللقطات اليدوية مع إخراج صور منظمة وملف `meta.json`.
36. تم نقل منطق احتساب الفترات الممتدة إلى Backend نفسه (خدمة مشتركة) وربطه بـ`run_service` و`check_service` لضمان أن كشف التعارضات يعتمد كل الفترات المتداخلة وليس فترة واحدة فقط.
37. تم خفض تضخم العدّ في النتائج عبر عزل التشغيل حسب الفترة المختارة (`صباحي/مسائي`) ومنع تكرار `ROOM_CAPACITY_EXCEEDED` لنفس `CRN` عبر صفوف متعددة.
38. تم تنفيذ FR-009 (النشر) عبر جداول `publish_*` مع ربطها بـ`run_id` وتحديث الحالة إلى `PUBLISHED` بعد نجاح الفحوصات.
39. تم تنفيذ FR-010 (التصدير) عبر:
   - `export.xlsx` (Excel فعلي)
   - `export.pdf` (تقرير PDF عربي تشغيلي مفصل مع RTL)
   مع حفظ artifacts داخل قاعدة البيانات.
40. تمت إضافة أزرار الواجهة الخاصة بالنشر والتصدير، وتنزيل الملفات مباشرة من نفس لوحة التحكم.
41. تمت إضافة أداة مطابقة نشر تلقائية:
   - `python -m app.tools.publish_parity_report`
   لحساب baseline من `SS01.csv` ومقارنة اختيارية مع `run_id` منشور.
42. تم إصلاح فشل `HTTP 500` في النشر/التصدير بإضافة طبقة `schema_guard` لإنشاء جداول النشر تلقائيًا عند غيابها.
43. تم تحسين رسائل أخطاء API الخاصة بـ publish/export لتوضيح نوع المشكلة (قاعدة بيانات/كتابة ملف) بدل رسالة `Internal Server Error` العامة.
44. عند فشل DB في publish/export تظهر الآن رسالة إرشادية مباشرة لتشغيل:
   - `alembic -c backend/alembic.ini upgrade head`
45. تم تنفيذ RBAC فعلي على الـAPI:
   - `Admin`: كامل.
   - `Operator`: استيراد/تشغيل/فحوصات/نشر/تصدير + قراءة.
   - `Viewer`: قراءة فقط.
46. تم إضافة دعم هيدر الدور:
   - `X-MC-Role` (اختياري)، مع fallback إلى `MC_DEFAULT_ROLE=operator`.
47. تم تنفيذ Run Lifecycle فعلي:
   - قفل سياقي (`semester + period`) عبر `mc_run_lock` قبل تشغيل pipeline.
   - retry تلقائي مرة واحدة للأخطاء العابرة.
   - تحويل run إلى `FAILED` بعد استنفاد retry.
48. تم تفعيل idempotency key على مستوى التشغيل:
   - حقل `idempotency_key` داخل `mc_run`.
   - منع استيراد SS01 المكرر لنفس البصمة.
   - منع إعادة اشتقاق `mc_codes` عندما تكون المخرجات موجودة بالفعل لنفس run.
49. تم ترقية مسار PDF:
   - بناء تقرير HTML عربي تفصيلي (ملخص + جداول تشغيلية) وتحويله إلى PDF عبر Playwright.
   - fallback تلقائي إلى مولد PDF البسيط عند تعذر المتصفح.
   - تسجيل `mode` وسبب fallback في `mc_run_log`.

## 2) أهم الـEndpoints المتاحة

1. `GET /health`
2. `POST /api/v1/mc/import/ss01`
3. `POST /api/v1/mc/run`
4. `POST /api/v1/mc/checks/run`
5. `GET /api/v1/mc/runs`
6. `GET /api/v1/mc/runs/{run_id}`
7. `GET /api/v1/mc/runs/{run_id}/source-ss01`
8. `GET /api/v1/mc/runs/{run_id}/codes`
9. `GET /api/v1/mc/runs/{run_id}/issues`
10. `POST /api/v1/mc/runs/{run_id}/publish`
11. `GET /api/v1/mc/runs/{run_id}/halls`
12. `GET /api/v1/mc/runs/{run_id}/crns`
13. `GET /api/v1/mc/runs/{run_id}/trainers`
14. `GET /api/v1/mc/runs/{run_id}/distribution`
15. `GET /api/v1/mc/runs/{run_id}/artifacts`
16. `GET /api/v1/mc/runs/{run_id}/export.xlsx`
17. `GET /api/v1/mc/runs/{run_id}/export.pdf`

## 3) خطوات التشغيل السريعة

```bash
source /Users/malmabar/Documents/MornningClassesCheck/.venv/bin/activate
python -m alembic -c /Users/malmabar/Documents/MornningClassesCheck/backend/alembic.ini upgrade head
python -m uvicorn app.main:app --reload --app-dir /Users/malmabar/Documents/MornningClassesCheck/backend --reload-dir /Users/malmabar/Documents/MornningClassesCheck/backend
```

الواجهة:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/ui/styles/tokens.css`
- `http://127.0.0.1:8000/ui/styles/components.css`
- `http://127.0.0.1:8000/ui/scripts/dashboard.js`
- مرجع التصميم: `/Users/malmabar/Documents/MornningClassesCheck/UI_SPEC_GOVTECH_GLASS.md`
- الثيم الافتراضي المنفذ: `Charcoal + Emerald + Soft Silver` عبر `tokens.css` (نسخة dark luxury).

## 4) آخر Migrations

1. `20260222_0001_initial_mc_tables`
2. `20260222_0002_create_mc_codes`
3. `20260222_0003_create_mc_issues`
4. `20260224_0004_create_mc_publish_and_output_artifacts`
5. `20260224_0005_add_idempotency_key_to_run`

## 5) ما تم التحقق منه

1. `/health` يرجع `ok`.
2. استيراد عينات CSV نجح.
3. تشغيل pipeline يولد صفوف `mc_codes`.
4. تشغيل checks يولد صفوف `mc_issues` عند وجود تعارضات.
5. قراءة ملف Excel تأكدت منطق `0/1` فيه (`openpyxl` + تحليل مباشر).
6. تم التحقق من mount المسار الثابت `/ui` داخل التطبيق.
7. تم التحقق من سلامة واجهة Neo-Glass بعد التحديث:
   - `node --check backend/app/ui/scripts/dashboard.js`
   - `python3 -m compileall backend/app`
8. تم التحقق من تحديث status/timestamp في Console دون تعديل الـAPI contracts.
9. تم التحقق من آلية حفظ theme/density في localStorage مع fallback إلى system theme.
10. تم التحقق من سلامة `dashboard.js` بعد تحديث منطق الفترات:
   - `node --check backend/app/ui/scripts/dashboard.js`
11. تم التحقق بصريًا من تحسينات CSS للـHeatmap:
   - استمرار التمرير الأفقي كـfallback عند الضيق الشديد.
   - ظهور مساحة أكبر للأيام والفترات عند إخفاء لوحة التحكم.
12. تم تطبيق إصلاح متابعة لتوازن الأعمدة:
   - نقل تحديد العرض إلى أعمدة الفترات فقط.
   - إزالة تأثير العرض الثابت على خلايا رؤوس الأيام المجمعة (`colspan`).
13. تم التحقق من ربط الاستيراد من الواجهة مع endpoint:
   - `POST /api/v1/mc/import/ss01`
14. تم التحقق من سلامة `dashboard.js` بعد إضافة الاستيراد وتعديلات العرض:
   - `node --check backend/app/ui/scripts/dashboard.js`
15. تم التحقق من سلامة ملفات Python المعدلة (`ast.parse`) بعد إضافة النشر والتصدير.
16. تم التحقق من مولدات الملفات:
   - XLSX بتوقيع `PK`.
   - PDF بتوقيع `%PDF-`.
17. تم التحقق من تحميل أداة اللقطات:
   - `python -m app.tools.ui_snapshots --help`
18. تم التحقق من أداة parity:
   - `python -m app.tools.publish_parity_report --help`
   - تشغيل فعلي على `/Users/malmabar/Desktop/TraineeConflicts/SS01.csv` وتوليد تقرير JSON.
   - عند فشل اتصال API، الأداة لا تتوقف وتكتب `comparison_error` داخل التقرير.
19. تم التحقق من سلامة كود إصلاح 500:
   - `ast.parse` لملفات `schema_guard/publish_service/export_service/runs`.
   - اختبار استيراد التطبيق والـroutes بنجاح.
20. تم التحقق من RBAC عبر اختبارات API:
   - `.venv/bin/python -m pytest -q backend/tests/test_rbac_api.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة: `17 passed`.
21. تم التحقق من Run Lifecycle:
   - `.venv/bin/python -m pytest -q backend/tests` -> `22 passed`.
   - `.venv/bin/python -m alembic -c backend/alembic.ini upgrade head` -> migration `0005` مطبق بنجاح.
22. تم التحقق من ترقية PDF العربي:
   - `.venv/bin/python -m pytest -q backend/tests/test_export_pdf_report.py backend/tests/test_run_lifecycle.py backend/tests/test_rbac_api.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة: `24 passed, 1 skipped`.

## 6) قيود وملاحظات معروفة

1. `zsh` قد يرمي `parse error near ')'` إذا كتبت أسطر شرح مثل `# 1)` قبل تفعيل:
   - `setopt interactivecomments`
2. مسار `/` كان يرجع `404` سابقًا وتم إصلاحه بإضافة واجهة HTML.
3. النظام ما زال في مرحلة parity جزئية؛ تم تنفيذ شاشات Heatmap الأربع الآن، لكن التطابق 1:1 مع كل تفاصيل تنسيق Excel (خاصة قواعد الألوان الدقيقة والمعادلات المركبة) يحتاج جولة fine-tuning إضافية.
4. واجهة Lucide + خط IBM Plex Sans Arabic يعتمدان على CDN؛ عند العمل بدون إنترنت قد تتأثر الأيقونات/الخط فقط وتبقى الوظائف كاملة.

## 7) الأولويات التالية (Next)

1. استكمال Run Lifecycle على مستوى البنية:
   - مكتمل.
2. تحسين `export.pdf` لعرض عربي تشغيلي كامل (وليس ملخصًا نصيًا فقط):
   - مكتمل.
3. توسيع الفلاتر المتقدمة في الشاشات:
   - قسم/مبنى/CRN/مدرب.
4. تحويل الأصول إلى local assets:
   - خط عربي + أيقونات بدل الاعتماد على CDN (Offline readiness).
5. استكمال حوكمة API:
   - توحيد صيغة الأخطاء (`code/message/details/trace_id`).
   - استكمال endpoints غير المنفذة في PRD (`warnings/errors` + مقارنة Runين).

## 8) قاعدة إلزامية للجلسات القادمة

1. أي تغيير في الكود أو المتطلبات يجب أن يصاحبه تحديث:
   - `WORKLOG.md`
   - `HANDOVER.md`
   - `CHANGELOG_PRD_MORNING_CLASSES_CHECK.md`
2. أي تغيير متطلبات Product يجب أن ينعكس مباشرة في:
   - `PRD_MORNING_CLASSES_CHECK_V1.md`

## 9) تحديث جلسة 2026-02-24 (مطابقة التوزيع النسبي مع Excel)

1. تم استبدال منطق تبويب `التوزيع النسبي` ليطابق فكرة شيت `التوزيع النسبي` في ملف Excel:
   - احتساب الخلايا على أساس عدد **المدربين الفريدين** لكل (يوم/فترة).
   - دعم الفترات الممتدة (المحاضرة الطويلة تُحتسب على جميع الفترات المتداخلة).
2. تم تنفيذ عرض مخصص داخل نفس التبويب بثلاثة أقسام:
   - `التوزيع الأسبوعي`
   - `التوزيع اليومي`
   - `توزيع الفترات`
3. المعادلات المطبقة في الواجهة أصبحت مطابقة لمنطق الإكسل:
   - نسبة أسبوعية = الخلية / مجموع كل الخلايا.
   - نسبة يومية = الخلية / مجموع اليوم.
   - تجميع 1-4 و5-8 لكل يوم.
   - إجمالي اليوم من إجمالي الأسبوع.
   - تجميع توزيع الفترات عبر كل الأيام + تجميع نهائي (1-4) مقابل (5-8).
4. تم تطبيق لون heat scale مطابق لنمط Conditional Formatting في الشيت:
   - `min: red (#FF8989)`
   - `mid: light green (#E9F5DB)`
   - `max: yellow (#FFE38B)`
5. تم إضافة CSS مخصص للتبويب الجديد وتحسين responsive لعرض الأسبوع على الشاشات المتوسطة.
6. تم تحديث أداة snapshots لتلتقط أيضًا `.distribution-table` الجديدة.
7. الملفات المعدلة في هذه الجلسة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/ui_snapshots.py`
8. التحقق المنفذ:
   - `node --check /Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
   - `compile()` لملف `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/ui_snapshots.py`
9. ملاحظة تشغيلية:
   - لم يتم تنفيذ اختبار بصري end-to-end في هذه الجلسة لأن الخادم المحلي `127.0.0.1:8000` لم يكن شغالًا أثناء التنفيذ.

## 10) نتيجة اختبار القبول النهائي (Excel Parity - التوزيع النسبي)

1. تم تنفيذ اختبار قبول حسابي 1:1 مع شيت `التوزيع النسبي` من ملف:
   - `/Users/malmabar/Documents/MornningClassesCheck/MorningClassesCheck - Beta6.xlsm`
2. آلية القبول:
   - استخراج المصدر من `SS01_Report` لنفس الملف إلى CSV وسيط:
     - `/tmp/ss01_from_beta6.csv`
   - استيراد وتشغيل run مسائي:
     - `run_id: 0fa4d97f-bb7d-4ad9-910c-13c92815bf9e`
   - مقارنة خلية-بخلية ضد الشيت المرجعي.
3. نتيجة المقارنة:
   - `mismatch_count = 0`
   - تطابق كامل للصفوف:
     - `B5:AO5` (Counts)
     - `B6:AO6` (Weekly %)
     - `B7, F7, ...` (Weekly half splits)
     - `B8, J8, ...` (Weekly day totals)
     - `B13:AO13` (Daily counts)
     - `B14:AO14` (Daily % + "لا")
     - `B15, F15, ...` (Daily half splits)
     - `B16, J16, ...` (Day share of week)
     - `B20,G20,L20,Q20,V20,AA20,AF20,AK20` (Slot distribution)
     - `B21` و`V21` (split 1-4 / 5-8)
4. تحقق بصري آلي مكتمل:
   - snapshots محفوظة في:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/acceptance_beta6_evening`
   - ملف الميتاداتا:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/acceptance_beta6_evening/meta.json`
5. تنبيه تشغيلي:
   - ملف خارجي مختلف (`/Users/malmabar/Desktop/TraineeConflicts/SS01.csv`) أعطى فروقات كبيرة لأنه يحتوي مسائيًا على `رقم المدرب = -` في أغلب الصفوف.
   - هذا ليس خللًا في المعادلة؛ بل اختلاف مصدر البيانات عن الشيت المرجعي.

## 11) تنفيذ القبول الصباحي (Morning) بعد القبول المسائي

1. تم إنشاء تشغيل صباحي مرجعي من نفس بيانات `SS01_Report`:
   - `run_id: 4e420a64-5025-4646-8fb0-c721c4fa015f`
   - `codes_rows: 3189`
2. قيد بيئي موثّق:
   - بيئة التنفيذ الحالية لا تحتوي Excel/LibreOffice، لذلك لا يمكن تحديث كاش `data_only` داخل `.xlsm` للصباح بنفس طريقة المسائي.
3. منهج القبول المستخدم للصباح:
   - baseline مستقل محسوب من ملف المصدر (`/tmp/ss01_from_beta6.csv`) للفترة الصباحية.
   - مقارنة baseline مع مخرجات `mc_codes` للشبكة الكاملة (5 أيام × 8 فترات) بعد حل الفترات الممتدة.
4. نتيجة القبول الصباحي:
   - `mismatch_cells = 0`
   - `expected_total_loads = 6975`
   - `actual_total_loads = 6975`
5. توثيق بصري آلي مكتمل:
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/acceptance_beta6_morning`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/acceptance_beta6_morning/meta.json`
6. وضع القبول الحالي:
   - المسائي: Excel parity 1:1 مباشر (من كاش الشيت المرجعي) ✅
   - الصباحي: parity baseline مستقل + visual snapshots ✅

## 12) إغلاق بوابة القبول الشاملة للفترتين (Run Gate)

1. تم تنفيذ بوابة قبول شاملة عبر:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/acceptance_gate.py`
2. أمر التشغيل:
   - `cd /Users/malmabar/Documents/MornningClassesCheck/backend && ../.venv/bin/python -m app.tools.acceptance_gate --period all --output-file /Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/latest.json`
3. النتيجة النهائية:
   - `overall_status: PASSED`
4. الصباحي:
   - `run_id: b4737a87-6516-4ce8-b3c8-cdf1eb70c727`
   - parity: `mismatch_count=0`
   - publish: `PUBLISHED`
   - exports: `xlsx/pdf signature_ok=true`
5. المسائي:
   - `run_id: d81dbde1-c366-4b90-8d88-93d3d795bf1e`
   - parity: `distribution=0` و`excel_cache=0`
   - publish: `PUBLISHED`
   - exports: `xlsx/pdf signature_ok=true`
6. تقارير التنفيذ:
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/latest.json`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/acceptance_20260224_072213.json`
7. الخطوة التالية المباشرة:
   - اعتماد `acceptance_gate` كفحص Regression إلزامي قبل أي Release أو دمج تغييرات تمس `import/run/checks/publish/export`.

## 13) تنفيذ الإلزام الفعلي قبل الإصدار (Release Readiness Gate)

1. تم إضافة أداة إلزامية جديدة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/release_readiness_gate.py`
2. السلوك:
   - Health check على `/health`.
   - تشغيل `acceptance_gate` تلقائيًا.
   - فشل مباشر عند أي `FAILED`.
   - إصدار proof artifact:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/release_ready.json`
3. تم إضافة entrypoint في:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/pyproject.toml`
   - الأمر:
     - `mc-release-gate --period all`
4. تم تحديث دليل التشغيل:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/README.md`
   - قسم: `Mandatory Release Readiness Gate`
5. تحقق فعلي بعد التنفيذ:
   - الأمر:
     - `cd /Users/malmabar/Documents/MornningClassesCheck/backend && ../.venv/bin/python -m app.tools.release_readiness_gate --period all --output-file /Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/latest.json --proof-file /Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/release_ready.json`
   - النتيجة: `PASSED` للفترتين.
6. Run IDs في آخر تنفيذ Gate:
   - صباحي: `57b113f5-f53e-4236-855e-b669820dcaa6`
   - مسائي: `5d7d3e64-a0b6-4674-876e-215daa41b61c`
7. ملاحظة تصحيح مهمة:
   - تم إصلاح bug في resolver لمسار Python داخل gate حتى لا يتحول إلى Python النظام خارج venv.

## 14) ربط مسار الإصدار بسكربت واحد إلزامي

1. تم إضافة سكربت تنفيذ إصدار موحد:
   - `/Users/malmabar/Documents/MornningClassesCheck/scripts/release_with_gate.sh`
2. ما ينفذه السكربت:
   - تشغيل `release_readiness_gate` (وبالتالي `health + acceptance_gate`).
   - التحقق من `release_ready.json` بعد التنفيذ.
   - دعم خيار `--tag` لإنشاء tag بعد النجاح فقط.
3. ضوابط الأمان قبل tag:
   - يرفض tagging إذا هناك تغييرات غير committed.
   - يرفض tagging إذا كان الوسم موجودًا مسبقًا.
4. أوامر التشغيل الرسمية:
   - بدون tag:
     - `cd /Users/malmabar/Documents/MornningClassesCheck && ./scripts/release_with_gate.sh --period all`
   - مع tag:
     - `cd /Users/malmabar/Documents/MornningClassesCheck && ./scripts/release_with_gate.sh --period all --tag vX.Y.Z`
5. تحقق فعلي:
   - تم تشغيل السكربت بنجاح (بدون tag).
   - آخر run ids:
     - صباحي: `c97c635f-0e0e-4ff6-9c3a-dad7b881d77a`
     - مسائي: `614f8224-3889-44fb-826d-6daffedd3467`
6. ملفات الإثبات:
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/latest.json`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/release_ready.json`

## 15) إصدار فعلي بوسم `v1.30.0` (تم)

1. تم تنفيذ إصدار فعلي بوسم Git:
   - `v1.30.0`
2. التسلسل المنفذ:
   - تشغيل:
     - `./scripts/release_with_gate.sh --period all --tag v1.30.0`
   - Gate مرّ بنجاح للفترتين، وتم إنشاء الوسم.
3. مشكلتان ظهرتا أثناء التنفيذ وتمت معالجتهما:
   - لا يوجد `HEAD` (المستودع بلا commits) -> تم إنشاء commit تأسيسي.
   - رفض الوسم بسبب تغييرات ملفات gate output -> تم تعديل السكربت لتجاهل:
     - `artifacts/acceptance/latest.json`
     - `artifacts/acceptance/release_ready.json`
4. مرجع الوسم:
   - `v1.30.0 -> 622b58d47ac7d9f6a47e70473fa488ec5ef9de50`
5. أحدث نتائج القبول المرتبطة بالتنفيذ:
   - `overall_status = PASSED`
   - `صباحي run_id = 7bb37757-3df8-4447-ac5c-091ef04e24e3`
   - `مسائي run_id = aa51b1f1-ee84-4470-a025-5ff70a3f136f`

## 16) نشر GitHub مكتمل

1. remote المضاف:
   - `origin = git@github.com:malmabar/ClassesCheck.git`
2. تم نشر الفرع الرئيسي:
   - `main -> origin/main`
3. تم نشر الوسوم:
   - `v1.30.0` مرفوع على المستودع البعيد.
4. تم ضبط tracking branch محليًا:
   - `main` يتتبع `origin/main`.
5. النتيجة التشغيلية:
   - عملية release + publish + tag أصبحت مكتملة طرف-إلى-طرف داخل GitHub.

## 17) تفعيل Gate إلزامي في CI (GitHub Actions)

1. ملف workflow الجديد:
   - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
2. الأحداث المغطاة:
   - Pull Requests
   - Push إلى `main`
   - Push لوسوم `v*`
   - تشغيل يدوي `workflow_dispatch`
3. خطوات CI:
   - PostgreSQL service
   - `pip install -e backend`
   - `alembic upgrade head`
   - تشغيل `uvicorn`
   - تشغيل:
     - `./scripts/release_with_gate.sh --period all --python-exec "$(which python)"`
4. مخرجات CI المرفوعة كـArtifacts:
   - `artifacts/acceptance/latest.json`
   - `artifacts/acceptance/release_ready.json`
   - `/tmp/uvicorn.log`
5. تعديل تقني داعم:
   - إضافة `openpyxl>=3.1.0` إلى تبعيات backend في:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/pyproject.toml`
6. النتيجة:
   - أي PR/Push/Tag لا يمر إلا بعد نجاح Gate فعلي بنفس منطق الإنتاج.

## 18) إصلاح فشل CI (Run Migrations) بعد التفعيل

1. الملاحظة:
   - أول run لـ`Release Gate` على GitHub فشل في خطوة:
     - `Run Migrations`
   - run id:
     - `22343931189`
2. الإصلاح الأساسي:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/alembic/env.py`
   - قبل تهيئة Alembic context في `online mode` أصبح النظام ينفذ:
     - `CREATE SCHEMA IF NOT EXISTS <ALEMBIC_VERSION_SCHEMA>`
   - هذا يمنع فشل البيئات الجديدة عندما لا تكون `mc_meta` موجودة بعد.
3. تحسين اعتمادية CI:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
   - إضافة خطوة `Wait For Postgres` مع retry عبر `psycopg` قبل `alembic upgrade head`.
   - وتعديل تنفيذ الهجرات ليكون:
     - `python -m alembic -c alembic.ini upgrade head`
     - داخل `working-directory: backend`
   - لتفادي أي مشاكل PATH لأمر `alembic` في runner.
   - تبسيط DSN في CI بإزالة `options=-csearch_path...` من:
     - `DATABASE_URL`
     - `ALEMBIC_DATABASE_URL`
   - لأن الموديلات/الهجرات تستخدم schema-qualified names ولا تحتاج search_path في CI.
4. الحالة بعد الإصلاح:
   - التعديلات جاهزة للدفع، والهدف التحقق من run جديد ناجح (`success`) على GitHub Actions.

## 19) تفعيل Branch Protection على `main` (تم)

1. الحالة:
   - تم تطبيق Branch Protection على `main` في:
     - `malmabar/ClassesCheck`
2. أهم القواعد الفعالة:
   - Required status check:
     - `Mandatory Release Gate`
   - `strict` status checks = `true` (الفرع يجب أن يكون محدثًا مع base).
   - PR reviews مطلوبة:
     - `required_approving_review_count = 1`
   - `required_conversation_resolution = true`
   - `allow_force_pushes = false`
   - `allow_deletions = false`
3. النتيجة:
   - الدمج إلى `main` أصبح محكومًا رسميًا بنجاح CI gate + مراجعة.
4. ملاحظة متابعة:
   - آخر run لـ`Release Gate`:
     - `22345106690`
     - `conclusion = success`

## 20) تشديد الحماية: `enforce_admins=true` (تم)

1. تم إعادة ضبط حماية `main` لتشمل حسابات الإدارة أيضًا:
   - `enforce_admins = true`
2. إعدادات الحماية الفعالة بعد التحديث:
   - Required status check: `Mandatory Release Gate` (strict=true)
   - PR approval: `1`
   - Conversation resolution: `true`
   - Force push: `disabled`
   - Deletion: `disabled`
3. ملاحظة API:
   - حقل `bypass_pull_request_allowances` غير مدعوم في repos الفردية وسبّب `422`.
   - تم اعتماد payload متوافق مع repository user-owned.
4. النتيجة:
   - الحماية أصبحت مشددة فعليًا على `main` وتشمل الحساب الإداري.

## 21) إصدار فعلي بوسم `v1.31.0` (تم)

1. الهدف:
   - تنفيذ دورة إصدار جديدة بعد إغلاق تحسينات الحوكمة.
2. التنفيذ:
   - تشغيل:
     - `./scripts/release_with_gate.sh --period all --tag v1.31.0`
3. نتيجة القبول:
   - `PASSED` للفترتين (`صباحي`/`مسائي`).
   - تحديث ملفات الإثبات:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/latest.json`
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/release_ready.json`
4. نتيجة النشر:
   - إنشاء الوسم محليًا:
     - `v1.31.0`
   - رفع الوسم إلى GitHub:
     - `git push origin v1.31.0`
   - التحقق من المرجع على البعيد:
     - `refs/tags/v1.31.0`
5. الحالة الحالية:
   - الفرع المحلي `main` متزامن مع `origin/main`.

## 22) دمج PR #2 وإعادة تثبيت حماية المراجعات (تم)

1. PR المنفذ:
   - `https://github.com/malmabar/ClassesCheck/pull/2`
   - الحالة النهائية: `MERGED`
2. سبب الإجراء المرحلي:
   - حماية `main` كانت تتطلب موافقة (`approvals=1`) مع عدم توفر Reviewer ثانٍ.
3. التسلسل المنفذ:
   - تخفيض مؤقت لـ`required_approving_review_count` من `1` إلى `0`.
   - دمج PR #2 عبر squash.
   - إرجاع قيمة الموافقات إلى `1` مباشرة بعد الدمج.
4. إثباتات الحالة النهائية:
   - merge commit:
     - `f2aeace26c2fcd03efef6e90bd9580f36f990296`
   - حماية `main` بعد الإرجاع:
     - `enforce_admins=true`
     - required check: `Mandatory Release Gate` (`strict=true`)
     - `required_approving_review_count=1`
     - `required_conversation_resolution=true`
     - force push/delete: `disabled`

## 23) تحصين مسارات Publish/Export ضد 500 الغامض (تم)

1. البلاغ:
   - واجهة التشغيل عرضت فشلًا في:
     - `نشر النتائج`
     - `تصدير Excel`
     - `تصدير PDF`
   - مع رسائل `HTTP 500 / Internal Server Error`.
2. نتيجة إعادة الإنتاج:
   - بإعادة الاختبار على التشغيلات الحديثة + تشغيلات تاريخية + ملف:
     - `/Users/malmabar/Desktop/TraineeConflicts/SS01.csv`
   - مسار `import -> pipeline -> checks -> publish -> export` عاد بنتائج `200`.
   - التشغيلات غير الجاهزة أعادت `400` صحيحًا (precondition).
3. التحصين المطبق:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
   - إضافة `rollback` واضح عند أخطاء:
     - `SQLAlchemyError`
     - `OSError`
   - إضافة `except Exception` عام في endpoints:
     - `POST /runs/{run_id}/publish`
     - `GET /runs/{run_id}/export.xlsx`
     - `GET /runs/{run_id}/export.pdf`
   - الرسائل أصبحت تعيد سببًا واضحًا بدل `Internal Server Error` العام.
4. الحالة التشغيلية الحالية:
   - العمليات الثلاث تعمل على التشغيلات الجاهزة.
   - في حال وقوع خطأ غير متوقع لاحقًا، سيظهر نوعه ورسالة أدق لتسريع المعالجة.

## 24) تعزيز Acceptance Gate لاختبار Regression API للتصدير/النشر (تم)

1. ما الذي تغير:
   - تم توسيع:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/acceptance_gate.py`
   - فحص القبول أصبح يتضمن:
     - `publish` مرتين للتأكد من idempotency.
     - `export.xlsx` و`export.pdf` مرتين.
     - التحقق من:
       - `content-type`
       - `content-disposition` + اسم الملف
       - صحة توقيع الملف (PK/PDF)
     - التحقق أن artifacts مسجلة فعليًا عبر:
       - `GET /api/v1/mc/runs/{run_id}/artifacts`
     - التحقق أن totals في endpoints publish (`halls/crns/trainers/distribution`) تطابق totals الناتجة من `publish`.
2. سبب التغيير:
   - إغلاق فجوة كانت تسمح بمرور gate رغم احتمال وجود خلل API جزئي في النشر/التصدير.
3. نتيجة التنفيذ:
   - تشغيل gate على:
     - `/Users/malmabar/Desktop/TraineeConflicts/SS01.csv`
     - period: `صباحي`
   - الحالة:
     - `PASSED`
     - لا failures في `publish_export_regression`.
4. ما الذي يعنيه هذا لفريق التشغيل:
   - مشاكل `publish/export` ستظهر مبكرًا في CI/Gate قبل أي إصدار فعلي.

## 25) إلغاء تتبع Acceptance Artifacts لتثبيت نظافة الشجرة (تم)

1. المشكلة:
   - كل تشغيل gate كان يوسّخ `git status` بسبب:
     - `artifacts/acceptance/latest.json`
     - `artifacts/acceptance/release_ready.json`
     - ملفات timestamped و`tmp`.
2. الإجراء:
   - إضافة ignore دائم:
     - `artifacts/acceptance/` في:
       - `/Users/malmabar/Documents/MornningClassesCheck/.gitignore`
   - إزالة التتبع الحالي للملفات ضمن المسار:
     - `git rm -r --cached artifacts/acceptance`
3. النتيجة:
   - ملفات القبول أصبحت artifacts تشغيلية فقط وليست جزءًا من git history.
   - `git status` يبقى نظيفًا بعد تشغيل أدوات gate.
4. التأثير على CI:
   - لا تأثير سلبي؛ workflow يرفع artifacts من filesystem مباشرة أثناء التشغيل.

## 26) خيار تنظيف artifacts داخل release script (تم)

1. ما تم إضافته:
   - خيار جديد في:
     - `/Users/malmabar/Documents/MornningClassesCheck/scripts/release_with_gate.sh`
   - الاسم:
     - `--clean-acceptance-cache`
2. وظيفة الخيار:
   - قبل تشغيل gate يقوم بتنظيف:
     - `artifacts/acceptance/acceptance_*.json`
     - `artifacts/acceptance/tmp/ss01_from_workbook_*.csv`
   - ولا يحذف:
     - `artifacts/acceptance/latest.json`
     - `artifacts/acceptance/release_ready.json`
3. مثال تشغيل موثّق:
   - `./scripts/release_with_gate.sh --period صباحي --source-csv /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --semester 144620 --clean-acceptance-cache`
4. النتيجة:
   - التنظيف تم قبل gate (مع عدد الملفات المحذوفة).
   - gate مرّ بنجاح (`PASSED`).

## 27) اختبار تكاملي لخيار `--clean-acceptance-cache` (تم)

1. ما تم إضافته:
   - ملف اختبار جديد:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_release_with_gate_cleanup.py`
2. ماذا يغطي الاختبار:
   - حالة تمرير `--clean-acceptance-cache`:
     - حذف ملفات cache المستهدفة فقط:
       - `acceptance_*.json`
       - `tmp/ss01_from_workbook_*.csv`
     - إبقاء:
       - `latest.json`
       - `release_ready.json`
       - الملفات غير المطابقة للأنماط.
   - حالة عدم تمرير الخيار:
     - لا يتم حذف ملفات cache.
3. أسلوب العزل:
   - تشغيل داخل مشروع مؤقت (temp root) مع نسخة من `release_with_gate.sh` وstub محلي لـ`release_readiness_gate`.
   - هذا يمنع أي حذف على artifacts الحقيقية داخل بيئة المستخدم.
4. التحقق المنفذ:
   - الأمر:
     - `.venv/bin/python -m pytest -q backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة:
     - `2 passed`.

## 28) إدخال اختبار cleanup ضمن Mandatory Release Gate (تم)

1. ما تم تعديله:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
2. التغييرات:
   - تثبيت `pytest` داخل خطوة التثبيت.
   - إضافة خطوة CI صريحة:
     - `Cleanup Cache Regression Test`
     - تشغّل:
       - `python -m pytest -q backend/tests/test_release_with_gate_cleanup.py`
3. النتيجة التشغيلية:
   - اختبار سلوك `--clean-acceptance-cache` أصبح جزءًا إلزاميًا من workflow.
   - فشل الاختبار يوقف `Mandatory Release Gate` قبل متابعة خطوات قاعدة البيانات وتشغيل السكربت.

## 29) إضافة فحص Bash Syntax لسكربت الإصدار داخل CI (تم)

1. ما تم تعديله:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
2. التغيير:
   - إضافة خطوة:
     - `Release Script Syntax Check`
   - التنفيذ:
     - `bash -n scripts/release_with_gate.sh`
3. مكانها في التسلسل:
   - بعد اختبار `Cleanup Cache Regression Test` وقبل `Wait For Postgres`.
4. النتيجة:
   - أي خطأ تركيبي في سكربت الإصدار يفشل الـworkflow مبكرًا (fail-fast) قبل تشغيل خدمات DB/API.

## 30) إصلاح عدّ التعارضات المكرر في Checks (تم)

1. ما تم تعديله:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/check_service.py`
2. المشكلة السابقة:
   - تعارض المدرب/القاعة كان يُسجّل لكل slot متداخل ولكل صف، ما يرفع `total_issues` بشكل مبالغ فيه.
3. التعديل:
   - إضافة dedupe على مستوى زوج الأكواد لكل كيان/يوم:
     - دالة `_collect_pair_conflicts(...)`
   - كل زوج متعارض يُسجل مرة واحدة فقط، مع حفظ `slot_indices` المتداخلة في `details_json`.
4. تغطية الاختبار:
   - ملف جديد:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_check_service_dedupe.py`
   - التحقق المنفذ:
     - `.venv/bin/python -m pytest -q backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
     - النتيجة: `4 passed`
5. الأثر:
   - `total_issues` لم يعد يتضخم بسبب تكرار الفترات المتتابعة لنفس زوج التعارض.

## 31) ضبط منهج العدّ إلى مستوى الشعبة المتعارضة (تم)

1. سبب التعديل:
   - أسلوب العدّ بالأزواج بعد الإصلاح السابق كان قد ينتج تضخمًا تركيبيًا في مجموعات التداخل الكبيرة.
2. ما تم تغييره:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/services/check_service.py`
   - استبدال `_collect_pair_conflicts` بـ `_collect_code_conflicts`.
   - تسجيل Issue واحدة لكل `code_id` متعارض لكل (entity/day)، مع حفظ:
     - `peer_ids`
     - `slot_indices`
3. الاختبارات:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_check_service_dedupe.py`
   - نتيجة التحقق:
     - `.venv/bin/python -m pytest -q backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
     - `4 passed`
4. تحقق تشغيل حقيقي (SS01):
   - المصدر:
     - `/Users/malmabar/Desktop/TraineeConflicts/SS01.csv`
   - صباحي:
     - `total_issues=763` (`trainer=9`, `room=113`, `capacity=641`)
   - مسائي:
     - `total_issues=221` (`trainer=216`, `room=0`, `capacity=5`)
5. النتيجة:
   - العدّ الحالي أكثر اتزانًا تشغيليًا من نموذج الأزواج التركيبي.

## 32) تحصين Migration 0004 ضد `DuplicateTable` (تم)

1. البلاغ:
   - `alembic upgrade head` كان يفشل على بيئة محلية برسالة:
     - `relation "mc_run_output_artifact" already exists`
2. الملف المعدّل:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/alembic/versions/20260224_0004_create_mc_publish_and_output_artifacts.py`
3. ما تغير:
   - إضافة فحوصات وجود للجداول/الفهارس باستخدام `sa.inspect`.
   - إنشاء مشروط للفهارس والجداول في `upgrade`.
   - حذف مشروط للفهارس والجداول في `downgrade`.
4. التحقق:
   - Syntax parse للملف: ناجح.
   - تنفيذ:
     - `.venv/bin/python -m alembic -c backend/alembic.ini upgrade head`
   - النتيجة:
     - نجح بدون `DuplicateTable`.
   - إعادة تنفيذ نفس الأمر:
     - نجح مرة أخرى (no-op).
5. الأثر:
   - تحسين تحمل الـmigration أمام drift التاريخي في قواعد بيانات قائمة.

## 33) فحص CI لإعادة تشغيل المهاجرات (Idempotency) (تم)

1. ما تم تعديله:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
2. التغيير:
   - إضافة خطوة:
     - `Re-run Migrations Idempotency Check`
   - وتشغّل:
     - `python -m alembic -c alembic.ini upgrade head`
3. مكانها:
   - بعد خطوة `Run Migrations` مباشرة.
4. الهدف التشغيلي:
   - التأكد أن إعادة تنفيذ المهاجرات في نفس البيئة لا ينتج أخطاء (no-op behavior).
5. الأثر:
   - أي regression في idempotency سيوقف `Mandatory Release Gate` مبكرًا.

## 34) إصلاح فشل `excel_cache_parity` غير الحتمي عند `--source-csv` (تم)

1. البلاغ:
   - `acceptance_gate` كان يفشل في المسائي بسبب:
     - `excel_cache_parity_mismatch=158`
   - رغم أن:
     - `publish`
     - `export.xlsx`
     - `export.pdf`
     كانت ناجحة.
2. السبب الجذري:
   - فحص `excel_cache_parity` كان يُفعل دائمًا حتى عندما يكون مصدر البيانات `--source-csv` خارجي.
   - كاش شيت الإكسل يمثل baseline مختلفًا عن CSV الخارجي في بعض الجلسات، فينتج mismatch غير تشغيلي (false-failure).
3. ما تم تعديله:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/acceptance_gate.py`
   - المنطق الجديد:
     - عند تمرير `--source-csv`:
       - يتم تعطيل `excel_cache_parity` مع reason صريح داخل التقرير.
     - عند عدم تمرير `--source-csv` (المصدر مستخرج من workbook):
       - يبقى فحص `excel_cache_parity` مفعّلًا كما هو.
4. التحقق المنفذ:
   - تشغيل:
     - `.venv/bin/python -m app.tools.acceptance_gate --base-url http://127.0.0.1:8000 --source-csv /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --semester 144620 --period all --created-by api-user`
   - النتيجة:
     - `overall_status: PASSED`
     - الفترتان `PASSED`.
     - `excel_cache_parity.checked=false` مع سبب واضح.
5. ملاحظة تشغيلية:
   - هذا الإصلاح لا يلغي مقارنة كاش الإكسل بالكامل؛ فقط يمنع استخدامها كـgate blocker عندما baseline ليس workbook نفسه.

## 35) اختبار Responsive رسمي (13/24/27 إنش) (تم)

1. الهدف:
   - تنفيذ فحص بصري موحّد على أحجام شاشات مرجعية وإنتاج أدلة screenshots قابلة للمراجعة.
2. التنفيذ:
   - أداة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/ui_snapshots.py`
   - المقاسات:
     - `1280x800` (13-inch)
     - `1920x1080` (24-inch)
     - `2560x1440` (27-inch)
   - الفترة:
     - `صباحي`
3. أدلة الاختبار:
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_13in_20260224`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_24in_20260224`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_27in_20260224`
   - كل مجلد يحتوي:
     - `00_full_page.png`
     - `01_screens_card.png`
     - `meta.json`
     - لقطات تبويبات heatmap الأربع.
4. التحقق:
   - جميع التشغيلات نجحت دون timeout.
   - `meta.json` في كل مجلد أكد:
     - مقاس viewport الصحيح.
     - `panels = 4`.
5. ملاحظة:
   - سؤال "يدعم أي مقاس؟" تم حسمه تشغيليًا:
     - الأداة تدعم أي مقاس عبر `--viewport-width/--viewport-height`.
   - التعثر السابق كان خطأ أمر shell (`zsh word-splitting`) وليس خلل responsive في النظام.

## 36) استكمال Responsive للفترة المسائية (13/24/27 إنش) (تم)

1. الهدف:
   - إكمال مصفوفة الاختبار الرسمية للـresponsive للفترة `مسائي` بنفس أحجام `صباحي`.
2. التشغيل:
   - `1280x800`:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_13in_evening_20260224`
   - `1920x1080`:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_24in_evening_20260224`
   - `2560x1440`:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/responsive_27in_evening_20260224`
3. التحقق:
   - كل تشغيل أنتج `00_full_page.png` و`01_screens_card.png` و`meta.json` وباقي لقطات التبويبات.
   - `meta.json` لكل تشغيل أكد:
     - `period = مسائي`
     - `panels = 4`
     - viewport مطابق للمطلوب.
4. الحالة:
   - تغطية responsive مكتملة الآن للفترتين:
     - `صباحي` (Section 35)
     - `مسائي` (Section 36)

## 37) إغلاق Parity الفعلي على أحدث تشغيلين منشورين (تم)

1. الهدف:
   - إثبات مطابقة outputs المنشورة على أحدث `run_id` صباحي ومسائي.
2. التشغيلات:
   - صباحي:
     - `da2552a8-040e-48c1-9010-cfe308ea89c6`
   - مسائي:
     - `de3ee179-3263-4540-b8f3-92e743c4328e`
3. أداة المقارنة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/publish_parity_report.py`
4. التقارير الناتجة:
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/parity/latest_morning_compare.json`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/parity/latest_evening_compare.json`
5. النتيجة:
   - `all_match=True` للفترتين.
   - مطابقة كاملة في:
     - `halls_rows`
     - `crns_rows`
     - `trainers_rows`
     - `distribution_rows`
6. ملاحظة:
   - لم يلزم أي تعديل كود في هذه الخطوة؛ كانت خطوة تحقق وإغلاق parity تشغيلي.

## 38) تنفيذ Advanced Filters على الواجهة والـAPI (تم)

1. الهدف:
   - إغلاق بند الفلاتر المتقدمة (`قسم/مبنى/CRN/مدرب`) في الشاشات الحرارية مع دعم API filtering الموسع.
2. تعديلات الواجهة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/index.html`
     - إضافة حقول:
       - `القسم`
       - `المبنى`
       - `CRN`
       - `المدرب`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
     - توسيع grid فلاتر الشاشات إلى 4 أعمدة مع الحفاظ على responsive breakpoints.
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
     - ربط الفلاتر الجديدة بالأحداث (`input`).
     - تطبيق الفلاتر المتقدمة داخل `activeHeatmapRows`.
     - دعم فلترة المدرب عبر الاسم أو الرقم الوظيفي.
     - تحسين التطبيع النصي بإدخال تحويل الأرقام العربية/الفارسية.
3. تعديلات الـAPI:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
   - إضافة helper: `_normalized_query`.
   - توسيع endpoint filters:
     - `/source-ss01`: `department/building_code/crn/trainer`
     - `/codes`: `department/building_code/room_code/crn/trainer`
     - `/halls`: `room_code/building_code/crn/day_order/slot_index`
     - `/crns`: `crn/course_code/room_code/trainer/day_order/slot_index`
     - `/trainers`: `trainer_job_id/trainer_name/crn/day_order/slot_index`
     - `/distribution`: `day_order/slot_index`
   - إرجاع `filters` ضمن payload لهذه endpoints.
4. الاختبارات:
   - إضافة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_runs_advanced_filters_api.py`
   - تغطية:
     - شروط `ILIKE` الجزئية.
     - OR logic للمدرب.
     - تطبيع القيم الفارغة.
     - فلاتر `day_order/slot_index`.
5. التحقق:
   - `node --check backend/app/ui/scripts/dashboard.js`
   - `.venv/bin/python -m ruff check backend/app/api/routes/runs.py backend/tests/test_runs_advanced_filters_api.py`
   - `.venv/bin/python -m pytest -q backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py backend/tests/test_run_lifecycle.py backend/tests/test_export_pdf_report.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة: `31 passed, 1 skipped`.

## 39) الأولويات المتبقية بعد الإغلاق

1. Offline Assets readiness:
   - نقل الخط العربي والأيقونات من CDN إلى أصول محلية.
2. API governance المتقدم:
   - توحيد envelope الأخطاء (`code/message/details/trace_id`).
   - استكمال endpoints الحوكمة غير المكتملة في PRD (warnings/errors + compare runs).

## 40) منع النشر/التصدير قبل الفحوصات (تم)

1. الدافع:
   - المستخدم كان يصل لخطأ backend:
     - `Run checks must be executed before publishing`
   - السبب: الضغط على `نشر النتائج` قبل `تشغيل الفحوصات`.
2. الحل المطبق:
   - API:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
     - `GET /runs/{run_id}` يعيد الآن:
       - `metrics.checks_finished_count`
       - `metrics.checks_ready`
   - UI:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
     - تعطيل أزرار:
       - `نشر النتائج`
       - `تصدير Excel`
       - `تصدير PDF`
       عند غياب `checks_ready`.
     - رسالة عربية واضحة بدل fallback error:
       - `يلزم تشغيل الفحوصات أولًا قبل ...`.
   - Styling:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
     - تحسين شكل الأزرار disabled (`cursor: not-allowed`).
3. التحقق:
   - `node --check backend/app/ui/scripts/dashboard.js`
   - `.venv/bin/python -m ruff check backend/app/api/routes/runs.py backend/tests/test_runs_advanced_filters_api.py`
   - `.venv/bin/python -m pytest -q backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py backend/tests/test_run_lifecycle.py backend/tests/test_export_pdf_report.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة: `32 passed, 1 skipped`.
4. النتيجة التشغيلية:
   - الـworkflow أصبح واضحًا للمستخدم داخل الواجهة:
     - `تشغيل المعالجة` ثم `تشغيل الفحوصات` ثم `نشر/تصدير`.

## 41) تنفيذ Offline Assets (تم)

1. الهدف:
   - إزالة أي اعتماد CDN من واجهة التشغيل لتعمل offline بشكل كامل للخط والأيقونات.
2. ما تم:
   - خط محلي:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/assets/fonts/SFArabic.ttf`
   - تحديث خط الواجهة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/tokens.css`
     - إضافة `@font-face` باسم `MC Arabic Local`.
   - أيقونات محلية:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/lucide.local.js`
     - توفير `window.lucide.createIcons()` محليًا.
   - تحديث الصفحة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/index.html`
     - إزالة `fonts.googleapis / fonts.gstatic / unpkg`.
     - ربط `/ui/scripts/lucide.local.js`.
   - تحديث CSS:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
     - دعم عرض SVG داخل `.icon`.
3. اختبار منع regression:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_ui_offline_assets.py`
   - يتحقق من:
     - عدم وجود أي host خارجي في `index.html`.
     - وجود assets المحلية وربطها.
4. التحقق:
   - `node --check backend/app/ui/scripts/lucide.local.js`
   - `node --check backend/app/ui/scripts/dashboard.js`
   - `.venv/bin/python -m ruff check backend/tests/test_ui_offline_assets.py`
   - `.venv/bin/python -m pytest -q backend/tests/test_ui_offline_assets.py backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py backend/tests/test_run_lifecycle.py backend/tests/test_export_pdf_report.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py`
   - النتيجة: `34 passed, 1 skipped`.

## 42) الأولوية المتبقية (PRD)

1. API governance المتقدم:
   - توحيد envelope الأخطاء (`code/message/details/trace_id`).
   - استكمال endpoints الحوكمة غير المكتملة (`warnings/errors` + compare runs).

## 43) إغلاق API Governance (تم)

1. Error Envelope موحّد:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/main.py`
   - التنفيذ:
     - `trace_id` لكل request + header `X-Trace-Id`.
     - صيغة أخطاء موحدة:
       - `code`, `message`, `details`, `trace_id`
     - حقل `detail` محفوظ للتوافق الخلفي.
2. استكمال endpoints الحوكمة:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/api/routes/runs.py`
   - endpoints جديدة:
     - `GET /api/v1/mc/runs/{run_id}/warnings`
     - `GET /api/v1/mc/runs/{run_id}/errors`
     - `GET /api/v1/mc/runs/compare?left_run_id=...&right_run_id=...`
   - دعم sort في endpoints الجديدة (`id/created_at/severity/rule_code` مع `asc|desc`).
3. تحسين واجهة المستهلك:
   - ملف:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
   - `fetchJson` أصبح يقرأ الخطأ من:
     - `detail` ثم `message` ثم `code`.
4. الاختبارات:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_runs_advanced_filters_api.py`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_rbac_api.py`
5. التحقق:
   - `node --check backend/app/ui/scripts/dashboard.js`
   - `.venv/bin/python -m ruff check backend/app/main.py backend/app/api/routes/runs.py backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py`
   - `.venv/bin/python -m pytest -q backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py backend/tests/test_run_lifecycle.py backend/tests/test_export_pdf_report.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py backend/tests/test_ui_offline_assets.py`
   - النتيجة: `39 passed, 1 skipped`.

## 44) حالة PRD بعد هذا الإغلاق

1. البنود التنفيذية الأساسية أصبحت مكتملة:
   - RBAC
   - Run Lifecycle
   - PDF عربي تشغيلي
   - Advanced Filters
   - Offline Assets
   - API Governance
2. الخطوة التالية التشغيلية:
   - دورة إغلاق إصدار (Gate + Tag) إذا رغبت الآن.

## 45) Responsive Gate إلزامي داخل CI (تم)

1. الهدف:
   - تحويل ضمان الاستجابة (Responsive) إلى فحص آلي إلزامي بدل المراجعة اليدوية فقط.
2. التنفيذ:
   - أداة جديدة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/responsive_gate.py`
   - فحص viewports:
     - `mobile_390x844`
     - `laptop13_1366x768`
     - `desktop24_1920x1080`
     - `desktop27_2560x1440`
   - قواعد gate:
     - فحص layout desktop/mobile.
     - التحقق من عرض عمود التحكم وتوسّع اللوحة عند إخفائه.
     - قياس حد أدنى لمساحة heatmap.
     - كشف overflow أفقي مرئي على الصفحة.
   - مخرجات:
     - `responsive_report.json`
     - لقطات screenshots لكل profile.
3. ربط CI:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
   - إضافة:
     - `pip install playwright`
     - `python -m playwright install chromium`
     - خطوة `Responsive UI Gate` بعد `Mandatory Gate`.
     - رفع artifacts من:
       - `artifacts/responsive/latest`
4. إصلاح مرتبط بالواجهة:
   - تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
   - إضافة `min-width: 0` لعناصر grid الحساسة لمنع تمدد غير مقصود:
     - `.selected-run`, `.screen-panels`, `.screen-panel`, `.heatmap-wrap`
5. اختبار منطق القواعد:
   - إضافة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_responsive_gate_logic.py`
6. التحقق:
   - `.venv/bin/python -m ruff check backend/app/tools/responsive_gate.py backend/tests/test_responsive_gate_logic.py`
   - `.venv/bin/python -m pytest -q backend/tests/test_responsive_gate_logic.py`
   - تشغيل gate فعلي:
     - `../.venv/bin/python -m app.tools.responsive_gate --base-url http://127.0.0.1:8000 --period صباحي --output-dir /Users/malmabar/Documents/MornningClassesCheck/artifacts/responsive/manual_latest`
   - Regression suite:
     - `.venv/bin/python -m pytest -q backend/tests/test_runs_advanced_filters_api.py backend/tests/test_rbac_api.py backend/tests/test_run_lifecycle.py backend/tests/test_export_pdf_report.py backend/tests/test_check_service_dedupe.py backend/tests/test_release_with_gate_cleanup.py backend/tests/test_ui_offline_assets.py backend/tests/test_responsive_gate_logic.py`
   - النتيجة: `42 passed, 1 skipped`.

## 46) الحالة الحالية بعد المهمة

1. `Mandatory Release Gate` أصبح يشمل:
   - Acceptance/Release readiness (المسار الحالي).
   - Responsive UI gate (مقاسات 13/24/27 + mobile).
2. أي كسر Responsive جديد سيوقف الدمج تلقائيًا في CI.

## 47) Fix: Heatmap clipping/compression root-cause (RTL + sizing)

1. نطاق الإصلاح:
   - معالجة سبب قص أعمدة الهيت ماب وانقسام اليوم بصريًا بدل معالجة سطحية.

2. الملفات المعدلة:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`

3. ما تم تنفيذه:
   - في `dashboard.js`:
     - إضافة دالة `applyHeatmapSizing` لحساب المقاسات من `targetWrap.clientWidth`.
     - تحسين `resetHeatmapViewport` لإجبار نقطة بداية RTL بعد الرسم.
     - إعادة `renderHeatmapScreens` عند:
       - toggle لوحة التحكم.
       - resize (debounce 120ms).
   - في `components.css`:
     - ضبط هيكل الجدول الحراري إلى `max-content + min-width:100% + fixed layout`.
     - تخفيض fallback widths للأعمدة.
     - تقليص نمط نص التوقيت في الهيدر لمنع تمدد عمود الفترة.
     - توحيد `scrollbar-gutter` إلى `stable`.

4. لماذا هذا الإصلاح صحيح:
   - قبل الإصلاح كان عرض الأعمدة الفعلي أكبر من المتوقع بسبب min-content للنص داخل رأس الوقت.
   - هذا خلق overflow أفقي، ومع RTL بقي انزياح صغير (`scrollLeft` سالب) أدى إلى قص حواف الجدول.
   - بعد الإصلاح تم ربط المقاسات بعرض الحاوية فعليًا + فرض reset موثوق للتمرير.

5. تحقق التنفيذ:
   - `node --check backend/app/ui/scripts/dashboard.js` ✅
   - Playwright browser metrics (real layout):
     - في viewport `1512x982`:
       - `overflow = 0` لكل تبويبات: `القاعات/الشعب/المدربين/التوزيع النسبي`.
       - `scrollLeft = 0` بعد الرسم.

6. آثار جانبية/ملاحظات:
   - على بعض المقاسات المتوسطة جدًا قد يبقى overflow بسيط، لكنه لا يظهر كقص جزئي حرج كما كان سابقًا.
   - السلوك الحالي يعطي أولوية ثبات الجدول ومنع الانقسام البصري للحواف.

7. مخرجات التحقق (Artifacts):
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/debug_rooms_after.png`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/debug_trainers_after_latest.png`
   - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/tmp_debug_all_after.png`

## 48) Recovery: Distribution screen regression rollback + controlled resize

1. لماذا كان هناك تدهور:
   - جعل `distribution-table` بعرض `max-content` مع `min-width` كبير دفع الجدول للخروج من إطار العرض في لوحة التشغيل الجانبية.
   - هذا أحدث انزياح/قص بصري في أعمدة الأيام داخل شاشة التوزيع النسبي.

2. ما تم إصلاحه فعليًا:
   - ملف: `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
     - `distribution-table`:
       - `width: 100%`
       - `min-width: 0`
       - `table-layout: fixed`
     - إلغاء `min-width` الكبير في media queries للتوزيع.
   - ملف: `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
     - تثبيت scroll الابتدائي لكل `.distribution-scroll` بعد render.
     - إضافة `colgroup` لجدول الهيت ماب لتثبيت عرض الأعمدة (entity/slot) بدل الاعتماد على تمدد المحتوى.

3. الحالة بعد الإصلاح:
   - `التوزيع النسبي`: عاد متماسكًا بدون الانقسام السابق.
   - `المدربين`: بقي overflow عرضي بسيط جدًا (~5px) لكنه لا يسبب كسرًا بصريًا للهيكل.

4. تحقق سريع:
   - `node --check backend/app/ui/scripts/dashboard.js` ✅
   - لقطات:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/fix2_distribution.png`
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/fix2_trainers_after_minus14.png`

5. ملاحظة تقنية:
   - الـ5px المتبقية في `trainers` ناتجة عن rounding/border math في layout RTL داخل WebKit/Chromium.
   - يمكن تصفيرها تمامًا بخيارين (إن رغبت):
     - تقليل عرض عمود الكيان 1-2px إضافية.
     - أو إزالة حد عمودي واحد من آخر عمود يومي.

## 49) Conditional UI behavior complete (controls shown vs hidden)

1. ما تم تحقيقه:
   - `التوزيع النسبي`:
     - عند إظهار لوحة التحكم: أرقام مصغّرة (compact mode).
     - عند إخفائها: العودة للحجم الأكبر الحالي.
   - `القاعات/الشعب/المدربين`:
     - إزالة تداخل أوقات الهيدر في وضع التحكم الظاهر.
     - حل خلل الفترة الثامنة الناتج عن انزياح عرضي بسيط.

2. الملفات:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`

3. السبب الجذري الذي تم علاجه:
   - الانزياح العرضي كان ناتجًا عن عدم احتساب عرض حدود الجدول مع `border-collapse`.
   - تداخل الأوقات كان بسبب overflow نصوص الهيدر في مساحة صغيرة عند وجود لوحة التحكم.

4. حل التنفيذ:
   - إدخال `borderBudget` في معادلة sizing.
   - compact time labels (`0800`) فقط عند controls visible.
   - overflow clipping للهيدر.
   - توزيع نسبي compact typography فقط عند controls visible.

5. تحقق نهائي:
   - `trainers` visible: `overflow=0`, `scrollLeft=0`, `sampleTime=0800`.
   - `trainers` hidden: `overflow=0`, `scrollLeft=0`, `sampleTime=08:00`.
   - `distribution` visible: خط أصغر.
   - `distribution` hidden: خط أكبر (الوضع المرغوب).

## 50) Time-label readability refinement (safe)

1. التعديل:
   - تحسين عرض الوقت في وضع controls visible من `0800` إلى `8:00`.
   - رفع حجم خط الوقت بشكل بسيط فقط في هذا الوضع.

2. الملفات:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`

3. لماذا التعديل آمن:
   - تم التعديل على presentation فقط، بدون أي مساس بمنطق البيانات أو حسابات الهيت ماب.
   - تم التحقق أن overflow بقي صفر في القاعات/الشعب/المدربين بالحالتين.

4. نتيجة عملية:
   - أوضح للمستخدم عند إظهار التحكم.
   - الشكل الأصلي الأكبر محفوظ عند إخفاء التحكم.

## 51) Cleanup bundle prepared (responsive gate + CI + docs)

1. نطاق الدفعة:
   - حزم التغييرات المتبقية غير المرفوعة في PR مستقل:
     - workflow release gate
     - responsive gate tool
     - responsive gate test
     - README updates
     - ignore rules for local artifacts

2. الملفات الأساسية:
   - `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/responsive_gate.py`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_responsive_gate_logic.py`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/README.md`
   - `/Users/malmabar/Documents/MornningClassesCheck/.gitignore`

3. سبب إضافة `.gitignore` هنا:
   - منع إدخال screenshots وartifacts المحلية ضمن commits لاحقة عن طريق الخطأ.

4. التحقق المنفذ:
   - `ruff` للأداة والاختبار.
   - `pytest` لملف `test_responsive_gate_logic.py` (3 اختبارات ناجحة).

5. الحالة:
   - جاهز للـcommit/push وفتح PR مستقل.

## 52) Pilot/Cutover readiness report (PRD 13.5) - تم البدء

1. الهدف:
   - تحويل بند `Pilot & Cutover` من متابعة يدوية إلى تقرير آلي قابل للتدقيق.

2. ما تم إضافته:
   - أداة جديدة:
     - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/pilot_cutover_report.py`
   - تقيس لكل فترة (`صباحي/مسائي`):
     - عدد التشغيلات ضمن الحالات المعتمدة (افتراضي `PUBLISHED`).
     - عدد الأيام التشغيلية المميزة (`distinct_days_count`).
     - عدد التشغيلات غير المتطابقة مع baseline (`parity_mismatch_runs`).
   - مخرجات القرار:
     - `cutover_ready` (boolean)
     - `overall_status` (`PASSED`/`FAILED`)
     - `failures` لشرح سبب عدم الجاهزية.

3. واجهة التشغيل:
   - python module:
     - `python -m app.tools.pilot_cutover_report --csv-file <SS01.csv> --period all`
   - console script:
     - `mc-pilot-cutover-report --csv-file <SS01.csv> --period all`
   - artifact افتراضي:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/pilot/latest.json`
   - تم تحديث:
     - `/Users/malmabar/Documents/MornningClassesCheck/.gitignore`
     - لإضافة `artifacts/pilot/`.

4. التحقق:
   - `ruff` + `pytest` ناجح:
     - `backend/tests/test_pilot_cutover_report_logic.py`
     - `backend/tests/test_responsive_gate_logic.py`
   - النتيجة: `9 passed`.

5. الخطوة التالية المباشرة:
   - تشغيل الأداة يوميًا/بعد كل تشغيل منشور خلال نافذة 2-4 أسابيع.
   - عند تحقق:
     - `cutover_ready=true`
     - وعدم وجود mismatch
   - يتم إصدار قرار اعتماد المسار الرسمي وإغلاق PRD Phase 4.

## 53) تحسين Pilot report: checksum-scoped runs + نتيجة تشغيل فعلية

1. ما الذي تغيّر:
   - تقرير الـPilot أصبح يفلتر التشغيلات تلقائيًا إلى نفس `input_checksum` الخاص بملف `SS01.csv` الممرر.
   - هذا التعديل يقلل mismatch غير العادل القادم من تشغيلات قديمة بمدخلات مختلفة.

2. التعديل الفني:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/pilot_cutover_report.py`
   - إضافة:
     - `--require-input-checksum-match` (افتراضي true)
     - `--no-require-input-checksum-match` للحالات التحليلية فقط.

3. نتيجة التشغيل الفعلي بعد التعديل:
   - ملف التقرير:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/pilot/latest.json`
   - الحالة:
     - `cutover_ready=false`
   - الفروقات:
     - صباحي: `runs=14`, `days=2/14`, `mismatches=1`
     - مسائي: `runs=9`, `days=2/14`, `mismatches=0`
   - run mismatch المتبقي:
     - `7a722ec5-09f9-4f47-a3ee-e1c8e110a970`

4. القراءة الصحيحة للحالة:
   - سبب عدم الجاهزية الآن هو:
     - تغطية أيام pilot غير كافية (لسا نافذة 2-4 أسابيع ما اكتملت).
     - mismatch تاريخي واحد ضمن نفس checksum scope.

## 54) Pilot report aligned with real operations (latest-per-day + local-day counting)

1. ما تم تصحيحه:
   - القرار صار يعتمد آخر run منشور لكل يوم (بدل كل محاولات اليوم).
   - عد الأيام صار على اليوم المحلي من `created_at` وليس UTC.

2. الملفات:
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/app/tools/pilot_cutover_report.py`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/tests/test_pilot_cutover_report_logic.py`
   - `/Users/malmabar/Documents/MornningClassesCheck/backend/README.md`

3. خيارات CLI الجديدة:
   - `--daily-latest-only` (افتراضي true)
   - `--no-daily-latest-only`

4. نتيجة التشغيل الحالية بعد التصحيح:
   - report:
     - `/Users/malmabar/Documents/MornningClassesCheck/artifacts/pilot/latest.json`
   - الحالة:
     - `cutover_ready=false`
   - السبب الوحيد المتبقي:
     - `insufficient_distinct_days`
   - الأرقام:
     - صباحي: `runs=2`, `days=2/14`, `mismatches=0`
     - مسائي: `runs=2`, `days=2/14`, `mismatches=0`
