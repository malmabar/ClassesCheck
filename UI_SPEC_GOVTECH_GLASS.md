# UI Audit + UI Spec - Premium Gov-Tech Neo-Glass (Arabic RTL)

## A) UI Audit (Current Page)

### Files in scope
1. `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/index.html`
2. `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/tokens.css`
3. `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/styles/components.css`
4. `/Users/malmabar/Documents/MornningClassesCheck/backend/app/ui/scripts/dashboard.js`

### Current strengths
1. RTL layout موجود ويعمل.
2. توزيع الأعمدة صحيح (التحكم يمين / التشغيل المحدد يسار).
3. لوحة التشغيل مرتبطة فعليًا بالـAPI وتعرض البيانات.
4. وجود Lucide icons وحالات فراغ أساسية.

### Current UI issues (to fix)
1. الثيم الحالي أقرب للـlight وليس "Luxury Charcoal" المطلوب.
2. التباين في بعض الأسطح الزجاجية غير مثالي عند 100% zoom.
3. التسلسل الهرمي للأزرار يحتاج ضبط أدق (primary/secondary/ghost بشكل أوضح).
4. الطباعة العربية تحتاج scale أقوى (H1/H2/Section/body/muted).
5. الكونسول يحتاج status + timestamp واضحين أعلى JSON.
6. بعض الحدود تبدو boxy أكثر من اللازم بدل الاعتماد على depth/soft shadows.

---

## B) UI Spec (Before Coding)

## 1) Design Direction
1. هوية الواجهة: **Premium Gov-Tech Neo-Glass**.
2. ثيم إلزامي: **Charcoal + Emerald + Soft Silver**.
3. اتجاه عام: داكن فاخر + glass panels + تباين عال + حركة خفيفة.

## 2) Core Tokens (exact requested)
```css
--bg: #0B1220;
--bg2: #070B14;
--panel: rgba(255,255,255,0.08);
--panel2: rgba(255,255,255,0.06);
--panelBorder: rgba(255,255,255,0.12);
--text: #EAF0FF;
--muted: #A9B4C7;
--primary: #17C964;
--primaryHover: #0EA75A;
--accent: #D7DFEA;
--danger: #FF4D4F;
--warning: #F7B731;
--info: #3B82F6;
```

### Extended tokens
1. Radius scale: `--radius-sm/md/lg/xl/2xl/pill`.
2. Spacing scale: `--space-1..--space-9`.
3. Shadow scale: `--shadow-soft/mid/float`.
4. Blur token: `--glass-blur: 14px` (range 12–18).
5. Focus ring: emerald واضح.

## 3) Typography (Arabic first)
1. Font: **IBM Plex Sans Arabic** (fallback Tajawal).
2. H1: `36–44`, weight `700`.
3. H2: `22–28`, weight `600/700`.
4. Section title: `16–18`, weight `600`.
5. Body: `14–16`, weight `400/500`.
6. Muted: `12–13`, weight `400`.
7. Line-height: `1.5–1.7`.

## 4) Layout Rules (keep existing structure)
1. Main Bento grid بعمودين:
   - Left main: `التشغيل المحدد`.
   - Right rail: `التحكم بالتشغيلات`.
2. Right rail width: `clamp(360px, 30vw, 420px)`.
3. Right rail sticky في desktop.
4. Mobile: stack عمودي تدريجي.

## 5) Component Rules

### Cards
1. نفس radius/padding/shadow على كل البطاقات.
2. KPI card = icon capsule + label + value + subtext.
3. تقليل الحدود القاسية والاعتماد على depth.

### Buttons (strict hierarchy)
1. Primary الوحيد: `تشغيل المعالجة` (emerald filled).
2. Secondary outline: `تشغيل الفحوصات`.
3. Ghost/soft: `تحديث التشغيلات` + `تحديث المحدد`.
4. كل الأزرار نفس الارتفاع ونفس radius.

### Tables
1. Sticky modern header + subtle zebra + row hover.
2. Gridlines خفيفة جدًا.
3. Chips: اليوم/القاعة/الحالة/الشدة.
4. Empty state: icon + Arabic message + hint.

### Response Console
1. Header فيه:
   - title
   - status badge (Success/Fail/Info)
   - timestamp
   - actions (copy + expand/collapse)
2. JSON area fixed height + internal scroll + monospace.

### Run list
1. Cards زجاجية بactive indicator emerald.
2. Status pill واضح + hover/focus states.

## 6) Accessibility Rules
1. Contrast عالي بين النص والأسطح الزجاجية.
2. `:focus-visible` واضح.
3. `prefers-reduced-motion`.
4. `prefers-reduced-transparency` (solid mode).
5. `forced-colors` support.

## 7) Micro-interactions
1. Hover lift خفيف (2px).
2. Transitions قصيرة وهادئة.
3. بدون مؤثرات flashy.

---

## C) Excel-like Heatmap Screens (Latest Add-on)

1. تم اعتماد 4 شاشات تشغيل حرارية داخل قسم `التشغيل المحدد`:
   - القاعات
   - الشعب
   - المدربين
   - التوزيع النسبي
2. تم اعتماد فلاتر موحدة أعلى الشاشة الحرارية تؤثر على كل الشاشات:
   - الفترة
   - الإشغال
   - البحث النصي.
3. بنية الهِيت ماب:
   - 5 أيام (الأحد - الخميس)
   - 8 فترات
   - قيم `0/1` مع حالة `>1` للتعارض.
4. شاشة `التوزيع النسبي` تضيف:
   - إشغال ثنائي
   - عدد الشعب
   - نسبة مئوية.
5. أسلوب العرض:
   - رؤوس Sticky
   - صف الكيان Sticky
   - خلايا ملوّنة حسب الحالة (`empty/occupied/conflict/percent`)
   - ملخص علوي لكل شاشة (عدد الصفوف، المشغول، التعارض، متوسط الإشغال).
