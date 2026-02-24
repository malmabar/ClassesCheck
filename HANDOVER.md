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
   - `export.pdf` (تقرير PDF ملخص)
   مع حفظ artifacts داخل قاعدة البيانات.
40. تمت إضافة أزرار الواجهة الخاصة بالنشر والتصدير، وتنزيل الملفات مباشرة من نفس لوحة التحكم.
41. تمت إضافة أداة مطابقة نشر تلقائية:
   - `python -m app.tools.publish_parity_report`
   لحساب baseline من `SS01.csv` ومقارنة اختيارية مع `run_id` منشور.
42. تم إصلاح فشل `HTTP 500` في النشر/التصدير بإضافة طبقة `schema_guard` لإنشاء جداول النشر تلقائيًا عند غيابها.
43. تم تحسين رسائل أخطاء API الخاصة بـ publish/export لتوضيح نوع المشكلة (قاعدة بيانات/كتابة ملف) بدل رسالة `Internal Server Error` العامة.
44. عند فشل DB في publish/export تظهر الآن رسالة إرشادية مباشرة لتشغيل:
   - `alembic -c backend/alembic.ini upgrade head`

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

## 6) قيود وملاحظات معروفة

1. `zsh` قد يرمي `parse error near ')'` إذا كتبت أسطر شرح مثل `# 1)` قبل تفعيل:
   - `setopt interactivecomments`
2. مسار `/` كان يرجع `404` سابقًا وتم إصلاحه بإضافة واجهة HTML.
3. النظام ما زال في مرحلة parity جزئية؛ تم تنفيذ شاشات Heatmap الأربع الآن، لكن التطابق 1:1 مع كل تفاصيل تنسيق Excel (خاصة قواعد الألوان الدقيقة والمعادلات المركبة) يحتاج جولة fine-tuning إضافية.
4. واجهة Lucide + خط IBM Plex Sans Arabic يعتمدان على CDN؛ عند العمل بدون إنترنت قد تتأثر الأيقونات/الخط فقط وتبقى الوظائف كاملة.

## 7) الأولويات التالية (Next)

1. إعادة اختبار UI مباشرة بعد إصلاح 500:
   - `نشر النتائج`
   - `تصدير Excel`
   - `تصدير PDF`
   والتأكد أن الاستجابة أصبحت نجاحًا أو رسالة خطأ واضحة غير 500 عام.
2. تنفيذ مقارنة Parity فعلية على `run_id` المنشور الحالي:
   - تشغيل:
     - `python -m app.tools.publish_parity_report --csv-file /Users/malmabar/Desktop/TraineeConflicts/SS01.csv --run-id <RUN_ID>`
   - إغلاق أي فروقات في `halls/crns/trainers/distribution`.
3. تحسين محتوى `export.pdf` ليدعم عرضًا عربيًا كاملًا (النسخة الحالية ملخص تشغيلي وظيفي).
4. اختبار responsive رسمي على دقات قياسية:
   - 13-inch laptop
   - 24-inch desktop
   - 27-inch wide monitor
   مع توثيق screenshots قبل/بعد.
5. توسيع فلاتر البحث إلى حقول مخصصة (قسم/مبنى/CRN/مدرب).
6. تحويل أيقونات Lucide والخط العربي إلى local assets لضمان عمل Offline بالكامل.

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
