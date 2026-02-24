# PROJECT EXECUTION BLUEPRINT - Morning Classes Check

> خطة تنفيذ حية (Living Plan) محدثة حسب التقدم الفعلي.

## 1) الهدف

تحقيق تطابق وظيفي كامل مع Excel (`Parity 1:1`) ثم تحسين تجربة العرض والتحليل داخل واجهة ويب عربية RTL.

## 2) الحالة العامة

1. المرحلة الحالية: **Phase 2.5 (UI Heatmap Parity) - جاري**
2. التقدم التقريبي: **66%**
3. الإنجاز الفعلي حتى الآن:
   - Import SS01
   - Derived Codes
   - Checks Engine
   - Dashboard RTL
   - Gov-Tech Glass UI System (Tokens + Components + Icons)
   - Premium Neo-Glass refresh (Right Control Rail + Left Run Report)
   - Luxury Dark theme contract (Charcoal + Emerald + Soft Silver)
   - Global Period Filter
   - Multi-screen Heatmaps (Rooms/CRNs/Trainers/Distribution) with shared filters

## 3) خطة المراحل

## Phase 0 - Baseline (مكتمل)
1. تثبيت baseline للملف المرجعي.
2. تحليل الشيتات والمعادلات والأسماء المعرفة.

## Phase 1 - Data Foundation (مكتمل)
1. تأسيس قاعدة البيانات والجداول الأساسية.
2. بناء importer لملف SS01.
3. حفظ run history والسجلات.

## Phase 2 - Rule Parity (جاري)
1. مكتمل:
   - `mc_codes`
   - `mc_issues` وقواعد الفحص الأساسية
2. متبقي:
   - `mc_rooms`
   - `mc_crns`
   - `mc_trainers`
   - `mc_distribution`
3. معيار الخروج من المرحلة:
   - نتائج parity مقبولة مقابل Excel في الجداول الأربع أعلاه.

## Phase 3 - UI Parity + Heatmaps (منفذ جزئيًا)
1. مكتمل:
   - شاشة `Rooms` Heatmap.
   - شاشة `CRNs` Heatmap.
   - شاشة `Trainers` Heatmap.
   - شاشة `التوزيع النسبي` (binary + count + percent).
   - فلاتر Heatmap موحدة (فترة/إشغال/بحث) على كل الشاشات.
2. متبقي:
   - مطابقة 1:1 دقيقة مع Excel في ترتيب الأعمدة والتنسيقات الخاصة.
   - إضافة حالات فلترة متقدمة موجهة لكل شاشة.
3. اعتماد design tokens موحد لكل التبويبات (`tokens.css` + `components.css`).
4. تثبيت layout rule للوحة الرئيسية:
   - التحكم يمين، التقرير يسار، مع RTL كامل.

## Phase 4 - Publish/Export (مخطط)
1. نشر outputs immutable مرتبطة بـ`run_id`.
2. تصدير Excel/PDF.
3. تحسين traceability.

## Phase 5 - Pilot + Cutover (مخطط)
1. تشغيل متوازي مع Excel.
2. قياس الفروقات وإغلاقها.
3. اعتماد رسمي.

## 4) المتطلبات الإلزامية الحاكمة للتنفيذ

1. Parity قبل أي تحسينات غير ضرورية.
2. العربية RTL افتراضيًا في كل الواجهات.
3. Global Period Filter إلزامي على كل الصفحات.
4. توثيق مستمر إلزامي:
   - `WORKLOG.md`
   - `HANDOVER.md`
   - `PRD + CHANGELOG`

## 5) قائمة العمل المباشرة (Next Sprint)

1. تحسين المطابقة الدقيقة Heatmap مع Excel (ترتيب/ألوان/ملخصات).
2. إضافة فلاتر متخصصة لكل شاشة (مبنى/قسم/نوع شعبة/مدرب).
3. إضافة اختبارات parity snapshot على عينات Beta6.
4. تحويل أيقونات Lucide إلى local vendor لتفادي الاعتماد على CDN.
5. تثبيت مرجع تصميم حي في:
   - `/Users/malmabar/Documents/MornningClassesCheck/UI_SPEC_GOVTECH_GLASS.md`
