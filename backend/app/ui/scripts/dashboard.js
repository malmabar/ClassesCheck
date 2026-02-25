document.addEventListener("DOMContentLoaded", () => {
  let selectedRunId = null;
  let resultCollapsed = false;
  let currentScreen = "rooms";
  let cachedCodesRows = [];
  let cachedHeatmapRows = [];
  let controlsPanelHidden = false;
  let selectedRunChecksReady = false;
  let uiBusy = false;

  const DAY_LABEL_BY_ORDER = {
    1: "الأحد",
    2: "الاثنين",
    3: "الثلاثاء",
    4: "الأربعاء",
    5: "الخميس",
  };

  const DAY_ORDER_BY_NAME = {
    الاحد: 1,
    الأحد: 1,
    "الاحد ": 1,
    الاثنين: 2,
    الإثنين: 2,
    الثلاثاء: 3,
    الاربعاء: 4,
    الأربعاء: 4,
    الخميس: 5,
  };

  const SLOT_TIME_RANGES = {
    صباحي: [
      ["08:00", "08:50"],
      ["09:00", "09:50"],
      ["10:00", "10:50"],
      ["11:00", "11:40"],
      ["12:30", "13:20"],
      ["13:21", "14:10"],
      ["14:15", "15:05"],
      ["15:06", "15:56"],
    ],
    مسائي: [
      ["16:00", "16:50"],
      ["16:51", "17:41"],
      ["17:50", "18:40"],
      ["18:41", "19:31"],
      ["19:40", "20:30"],
      ["20:31", "21:21"],
      ["21:30", "22:20"],
      ["22:21", "23:11"],
    ],
  };

  const SCHEDULE_BY_PERIOD = {
    صباحي: SLOT_TIME_RANGES.صباحي.map(([startLabel, endLabel], index) => {
      const startHhmm = clockLabelToHhmm(startLabel);
      const endHhmm = clockLabelToHhmm(endLabel);
      return {
        slot: index + 1,
        startLabel,
        endLabel,
        startHhmm,
        endHhmm,
        startMin: hhmmToMinutes(startHhmm),
        endMin: hhmmToMinutes(endHhmm),
      };
    }),
    مسائي: SLOT_TIME_RANGES.مسائي.map(([startLabel, endLabel], index) => {
      const startHhmm = clockLabelToHhmm(startLabel);
      const endHhmm = clockLabelToHhmm(endLabel);
      return {
        slot: index + 1,
        startLabel,
        endLabel,
        startHhmm,
        endHhmm,
        startMin: hhmmToMinutes(startHhmm),
        endMin: hhmmToMinutes(endHhmm),
      };
    }),
  };

  const SLOT_BY_HHMM = Object.values(SCHEDULE_BY_PERIOD).reduce((acc, rows) => {
    rows.forEach((slot) => {
      acc[slot.startHhmm] = slot.slot;
    });
    return acc;
  }, {});

  const DEFAULT_DAYS = [1, 2, 3, 4, 5];
  const DEFAULT_SLOTS = [1, 2, 3, 4, 5, 6, 7, 8];
  const MAX_HEATMAP_ROWS = 180;
  const HEATMAP_SCREEN_KEYS = ["rooms", "crns", "trainers", "distribution"];

  const els = {
    healthDot: document.getElementById("healthDot"),
    healthText: document.getElementById("healthText"),
    globalPeriod: document.getElementById("globalPeriod"),
    runList: document.getElementById("runList"),
    result: document.getElementById("result"),
    createdBy: document.getElementById("createdBy"),
    selectedRunText: document.getElementById("selectedRunText"),
    codesCount: document.getElementById("codesCount"),
    issuesCount: document.getElementById("issuesCount"),
    runStatus: document.getElementById("runStatus"),
    runPeriod: document.getElementById("runPeriod"),
    codesBody: document.getElementById("codesBody"),
    issuesBody: document.getElementById("issuesBody"),
    codesEmpty: document.getElementById("codesEmpty"),
    issuesEmpty: document.getElementById("issuesEmpty"),
    refreshRuns: document.getElementById("refreshRuns"),
    refreshSelected: document.getElementById("refreshSelected"),
    runPipeline: document.getElementById("runPipeline"),
    runChecks: document.getElementById("runChecks"),
    publishRun: document.getElementById("publishRun"),
    exportXlsx: document.getElementById("exportXlsx"),
    exportPdf: document.getElementById("exportPdf"),
    importSemester: document.getElementById("importSemester"),
    importPeriod: document.getElementById("importPeriod"),
    importFile: document.getElementById("importFile"),
    importSs01: document.getElementById("importSs01"),
    copyResult: document.getElementById("copyResult"),
    toggleResult: document.getElementById("toggleResult"),
    resultState: document.getElementById("resultState"),
    resultTime: document.getElementById("resultTime"),
    selectedRunMeta: document.getElementById("selectedRunMeta"),
    themeToggle: document.getElementById("themeToggle"),
    themeText: document.getElementById("themeText"),
    densityToggle: document.getElementById("densityToggle"),
    densityText: document.getElementById("densityText"),
    bentoGrid: document.querySelector(".bento-grid"),
    controlsPanel: document.querySelector(".controls-panel"),
    toggleControlsPanel: document.getElementById("toggleControlsPanel"),
    toggleControlsText: document.getElementById("toggleControlsText"),
    heatmapPeriodFilter: document.getElementById("heatmapPeriodFilter"),
    heatmapOccupancyFilter: document.getElementById("heatmapOccupancyFilter"),
    heatmapSearchFilter: document.getElementById("heatmapSearchFilter"),
    heatmapDepartmentFilter: document.getElementById("heatmapDepartmentFilter"),
    heatmapBuildingFilter: document.getElementById("heatmapBuildingFilter"),
    heatmapCrnFilter: document.getElementById("heatmapCrnFilter"),
    heatmapTrainerFilter: document.getElementById("heatmapTrainerFilter"),
    screenTabs: Array.from(document.querySelectorAll(".screen-tab")),
    screenPanels: Array.from(document.querySelectorAll("[data-screen-panel]")),
    roomsSummary: document.getElementById("roomsSummary"),
    roomsHeatmapWrap: document.getElementById("roomsHeatmapWrap"),
    crnsSummary: document.getElementById("crnsSummary"),
    crnsHeatmapWrap: document.getElementById("crnsHeatmapWrap"),
    trainersSummary: document.getElementById("trainersSummary"),
    trainersHeatmapWrap: document.getElementById("trainersHeatmapWrap"),
    distributionSummary: document.getElementById("distributionSummary"),
    distributionHeatmapWrap: document.getElementById("distributionHeatmapWrap"),
  };

  const HEATMAP_TARGETS = {
    rooms: { summary: els.roomsSummary, wrap: els.roomsHeatmapWrap, title: "القاعات" },
    crns: { summary: els.crnsSummary, wrap: els.crnsHeatmapWrap, title: "الشعب" },
    trainers: { summary: els.trainersSummary, wrap: els.trainersHeatmapWrap, title: "المدربين" },
    distribution: { summary: els.distributionSummary, wrap: els.distributionHeatmapWrap, title: "التوزيع النسبي" },
  };

  const GLOBAL_PERIOD_STORAGE_KEY = "mc_global_period_filter";
  const THEME_STORAGE_KEY = "mc_ui_theme";
  const DENSITY_STORAGE_KEY = "mc_ui_density";
  const CONTROLS_PANEL_STORAGE_KEY = "mc_controls_panel_hidden";

  function renderLucideIcons() {
    if (window.lucide && typeof window.lucide.createIcons === "function") {
      window.lucide.createIcons();
    }
  }

  function normalizeDigitChars(value) {
    const map = {
      "٠": "0",
      "١": "1",
      "٢": "2",
      "٣": "3",
      "٤": "4",
      "٥": "5",
      "٦": "6",
      "٧": "7",
      "٨": "8",
      "٩": "9",
      "۰": "0",
      "۱": "1",
      "۲": "2",
      "۳": "3",
      "۴": "4",
      "۵": "5",
      "۶": "6",
      "۷": "7",
      "۸": "8",
      "۹": "9",
    };
    return String(value || "").replace(/[٠-٩۰-۹]/g, (d) => map[d] || d);
  }

  function hhmmToMinutes(hhmm) {
    if (!Number.isInteger(hhmm)) return null;
    const hours = Math.floor(hhmm / 100);
    const minutes = hhmm % 100;
    if (hours < 0 || hours > 23 || minutes < 0 || minutes > 59) return null;
    return hours * 60 + minutes;
  }

  function clockLabelToHhmm(label) {
    const normalized = normalizeDigitChars(label).trim();
    const match = normalized.match(/^(\d{1,2})[:.](\d{2})$/);
    if (!match) return null;
    const hours = Number.parseInt(match[1], 10);
    const minutes = Number.parseInt(match[2], 10);
    if (!Number.isFinite(hours) || !Number.isFinite(minutes)) return null;
    if (hours < 0 || hours > 23 || minutes < 0 || minutes > 59) return null;
    return hours * 100 + minutes;
  }

  function parseTokenToHhmm(token) {
    const normalized = normalizeDigitChars(token).trim();
    const clock = normalized.match(/^(\d{1,2})[:.](\d{2})$/);
    if (clock) {
      return clockLabelToHhmm(`${clock[1]}:${clock[2]}`);
    }

    const digits = normalized.replace(/[^0-9]/g, "");
    if (digits.length === 3) {
      return clockLabelToHhmm(`${digits.slice(0, 1)}:${digits.slice(1)}`);
    }
    if (digits.length === 4) {
      return clockLabelToHhmm(`${digits.slice(0, 2)}:${digits.slice(2)}`);
    }
    return null;
  }

  function extractHhmmTokens(textValue) {
    const normalized = normalizeDigitChars(textValue);
    const matches = normalized.match(/\d{1,2}[:.]\d{2}|\d{3,4}/g) || [];
    return matches
      .map(parseTokenToHhmm)
      .filter((value) => Number.isInteger(value));
  }

  function statusClass(status) {
    const s = String(status || "").toUpperCase();
    if (s === "SUCCEEDED" || s === "PUBLISHED") return "state-pill--ok";
    if (s === "RUNNING" || s === "VALIDATING" || s === "CREATED") return "state-pill--warn";
    return "state-pill--err";
  }

  function statusLabel(status) {
    const s = String(status || "").toUpperCase();
    const labels = {
      CREATED: "تم الإنشاء",
      VALIDATING: "قيد التحقق",
      RUNNING: "قيد التنفيذ",
      FAILED: "فشل",
      SUCCEEDED: "ناجح",
      PUBLISHED: "منشور",
    };
    return labels[s] || s || "-";
  }

  function severityClass(severity) {
    const s = String(severity || "").toUpperCase();
    if (s === "ERROR" || s === "HIGH" || s === "CRITICAL") return "table-chip--err";
    if (s === "WARNING" || s === "WARN" || s === "MEDIUM") return "table-chip--warn";
    return "table-chip--ok";
  }

  function buildChip(text, className = "table-chip--neutral") {
    const chip = document.createElement("span");
    chip.className = `table-chip ${className}`;
    chip.textContent = text == null || text === "" ? "-" : String(text);
    return chip;
  }

  async function fetchJson(url, options = {}) {
    const res = await fetch(url, options);
    const text = await res.text();
    let payload;
    try {
      payload = text ? JSON.parse(text) : {};
    } catch {
      payload = { raw: text };
    }

    if (!res.ok) {
      const detail =
        payload && (payload.detail || payload.message || payload.code)
          ? payload.detail || payload.message || payload.code
          : `HTTP ${res.status}`;
      throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    }
    return payload;
  }

  async function fetchAllPages(baseUrl, pageSize = 500, maxPages = 50) {
    let page = 1;
    let total = 0;
    const items = [];

    while (page <= maxPages) {
      const payload = await fetchJson(`${baseUrl}?page=${page}&size=${pageSize}`);
      const pageItems = payload.items || [];
      total = payload.total || total;
      items.push(...pageItems);

      if (!payload.has_next || pageItems.length === 0) {
        break;
      }
      page += 1;
    }

    return {
      items,
      total: total || items.length,
    };
  }

  function resultToneLabel(tone) {
    const labels = {
      success: "ناجح",
      error: "فشل",
      info: "معلومة",
    };
    return labels[tone] || labels.info;
  }

  function setResultMeta(tone = "info") {
    if (!els.resultState || !els.resultTime) return;
    els.resultState.className = `state-pill ${
      tone === "success" ? "state-pill--ok" : tone === "error" ? "state-pill--err" : "state-pill--warn"
    }`;
    els.resultState.textContent = resultToneLabel(tone);
    els.resultTime.textContent = new Date().toLocaleTimeString("ar-SA", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    });
  }

  function putResult(value, tone = "info") {
    els.result.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
    setResultMeta(tone);
  }

  function formatDateTime(value) {
    if (!value) return null;
    const dt = new Date(value);
    if (Number.isNaN(dt.getTime())) return null;
    return dt.toLocaleString("ar-SA", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function normalizeArabicText(value) {
    return normalizeDigitChars(String(value || ""))
      .normalize("NFKD")
      .replace(/[\u0610-\u061A\u064B-\u065F\u0670]/g, "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  function parseDigits(value) {
    const digits = normalizeDigitChars(value).replace(/[^0-9]/g, "").slice(0, 4);
    if (!digits) return null;
    const parsed = Number.parseInt(digits, 10);
    return Number.isFinite(parsed) ? parsed : null;
  }

  function normalizeDayOrder(dayOrder, dayName) {
    if (Number.isInteger(dayOrder) && dayOrder >= 1 && dayOrder <= 5) return dayOrder;
    const normalized = String(dayName || "").trim();
    if (!normalized) return null;
    return DAY_ORDER_BY_NAME[normalized] || DAY_ORDER_BY_NAME[normalized.replace(/\s+/g, "")] || null;
  }

  function getScheduleForPeriod(period) {
    if (period === "مسائي") return SCHEDULE_BY_PERIOD.مسائي;
    return SCHEDULE_BY_PERIOD.صباحي;
  }

  function currentHeatmapPeriodValue() {
    return els.heatmapPeriodFilter?.value === "مسائي" ? "مسائي" : "صباحي";
  }

  function findSlotByTime(period, hhmm) {
    const schedule = getScheduleForPeriod(period);
    const exact = schedule.find((slot) => slot.startHhmm === hhmm);
    if (exact) return exact.slot;

    const minutes = hhmmToMinutes(hhmm);
    if (minutes == null) return null;
    const overlap = schedule.find((slot) => minutes >= slot.startMin && minutes < slot.endMin);
    return overlap ? overlap.slot : null;
  }

  function normalizeSlotIndex(slotIndex, timeHhmm, timeValue, period) {
    if (Number.isInteger(slotIndex) && slotIndex >= 1 && slotIndex <= 8) return slotIndex;

    if (Number.isInteger(timeHhmm)) {
      const byPeriod = findSlotByTime(period, timeHhmm);
      if (byPeriod) return byPeriod;
      if (SLOT_BY_HHMM[timeHhmm]) return SLOT_BY_HHMM[timeHhmm];
    }

    const parsed = parseDigits(timeValue);
    if (parsed) {
      const byPeriod = findSlotByTime(period, parsed);
      if (byPeriod) return byPeriod;
      if (SLOT_BY_HHMM[parsed]) return SLOT_BY_HHMM[parsed];
    }
    return null;
  }

  function derivePeriodFlags(row) {
    const sectionType = String(row.section_type || "");
    const hasMorningWord = sectionType.includes("صباح");
    const hasEveningWord = sectionType.includes("مسائ");
    const isMorning = Boolean(row.is_morning || hasMorningWord);
    const isEvening = Boolean(row.is_evening || hasEveningWord);
    return { isMorning, isEvening };
  }

  function resolveTimeRange(row) {
    const tokens = extractHhmmTokens(row.time_value);
    let firstCandidate = tokens[0] || null;
    if (!Number.isInteger(firstCandidate) && Number.isInteger(row.time_hhmm)) {
      firstCandidate = row.time_hhmm;
    }
    const secondCandidate = tokens.length > 1 ? tokens[1] : null;

    let startCandidate = firstCandidate;
    let endCandidate = secondCandidate;
    let startMin = hhmmToMinutes(startCandidate);
    let endMin = hhmmToMinutes(endCandidate);

    // بعض ملفات SS01 تكتب الوقت بصيغة "النهاية - البداية" (مثل: 1130 - 0900).
    // نطبع المدى زمنيًا بحيث start <= end قبل حساب التداخل مع الفترات.
    if (startMin != null && endMin != null && endMin < startMin) {
      [startCandidate, endCandidate] = [endCandidate, startCandidate];
      [startMin, endMin] = [endMin, startMin];
    }

    return {
      startHhmm: Number.isInteger(startCandidate) ? startCandidate : null,
      endHhmm: Number.isInteger(endCandidate) ? endCandidate : null,
      startMin,
      endMin,
    };
  }

  function collectOverlappingSlots(period, timeRange) {
    const slots = new Set();
    if (timeRange.startMin == null) {
      return slots;
    }

    const schedule = getScheduleForPeriod(period);
    const effectiveEnd = timeRange.endMin != null && timeRange.endMin > timeRange.startMin
      ? timeRange.endMin
      : timeRange.startMin + 1;

    schedule.forEach((slot) => {
      const overlaps = timeRange.startMin < slot.endMin && effectiveEnd > slot.startMin;
      if (overlaps) slots.add(slot.slot);
    });

    return slots;
  }

  function inferPeriodFromTimeRange(timeRange) {
    const morningSlots = collectOverlappingSlots("صباحي", timeRange);
    const eveningSlots = collectOverlappingSlots("مسائي", timeRange);

    if (morningSlots.size !== eveningSlots.size) {
      return morningSlots.size > eveningSlots.size ? "صباحي" : "مسائي";
    }

    const hhmmRef = Number.isInteger(timeRange.startHhmm)
      ? timeRange.startHhmm
      : Number.isInteger(timeRange.endHhmm)
        ? timeRange.endHhmm
        : null;
    if (Number.isInteger(hhmmRef)) {
      return hhmmRef >= 1600 ? "مسائي" : "صباحي";
    }

    return null;
  }

  function resolveRowPeriod(row, periodFlags, timeRange) {
    const byTime = inferPeriodFromTimeRange(timeRange);
    if (byTime) return byTime;

    if (periodFlags.isMorning && !periodFlags.isEvening) return "صباحي";
    if (periodFlags.isEvening && !periodFlags.isMorning) return "مسائي";

    const sectionText = String(row.section_type || "");
    if (sectionText.includes("صباح")) return "صباحي";
    if (sectionText.includes("مسائ")) return "مسائي";

    const periodText = String(row.period || "");
    if (periodText.includes("صباح")) return "صباحي";
    if (periodText.includes("مسائ")) return "مسائي";

    return currentHeatmapPeriodValue();
  }

  function resolveSlotIndices(row, period, timeRange) {
    const alternatePeriod = period === "مسائي" ? "صباحي" : "مسائي";
    let slots = collectOverlappingSlots(period, timeRange);
    const alternateSlots = collectOverlappingSlots(alternatePeriod, timeRange);
    if (alternateSlots.size > slots.size) {
      slots = alternateSlots;
    }

    const fallbackSlot = normalizeSlotIndex(row.slot_index, row.time_hhmm, row.time_value, period);

    if (!slots.size && Number.isInteger(timeRange.startHhmm)) {
      const byStart = findSlotByTime(period, timeRange.startHhmm);
      const byAlternateStart = findSlotByTime(alternatePeriod, timeRange.startHhmm);
      if (byStart) {
        slots.add(byStart);
      } else if (byAlternateStart) {
        slots.add(byAlternateStart);
      }
    }

    if (!slots.size && Number.isInteger(fallbackSlot)) {
      slots.add(fallbackSlot);
    }

    return Array.from(slots).sort((a, b) => a - b);
  }

  function buildHeatmapRows(rawRows) {
    return rawRows.map((row) => {
      const dayOrder = normalizeDayOrder(row.day_order, row.day_name);
      const periodFlags = derivePeriodFlags(row);
      const timeRange = resolveTimeRange(row);
      const resolvedPeriod = resolveRowPeriod(row, periodFlags, timeRange);
      const slotIndices = resolveSlotIndices(row, resolvedPeriod, timeRange);

      return {
        ...row,
        dayOrder,
        slotIndex: slotIndices[0] || null,
        slotIndices,
        resolvedPeriod,
        timeRangeStart: timeRange.startHhmm,
        timeRangeEnd: timeRange.endHhmm,
        isMorning: periodFlags.isMorning || resolvedPeriod === "صباحي",
        isEvening: periodFlags.isEvening || resolvedPeriod === "مسائي",
      };
    });
  }

  function applyTheme(theme) {
    const resolved = theme === "light" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", resolved);

    if (els.themeText) {
      els.themeText.textContent = resolved === "dark" ? "داكن" : "فاتح";
    }
    if (els.themeToggle) {
      const next = resolved === "dark" ? "تبديل إلى الوضع الفاتح" : "تبديل إلى الوضع الداكن";
      els.themeToggle.setAttribute("aria-label", next);
      els.themeToggle.setAttribute("title", next);
    }
  }

  function applyDensity(density) {
    const resolved = density === "comfortable" ? "comfortable" : "compact";
    document.documentElement.setAttribute("data-density", resolved);

    if (els.densityText) {
      els.densityText.textContent = resolved === "compact" ? "مضغوط" : "مريح";
    }
    if (els.densityToggle) {
      const next = resolved === "compact" ? "تبديل إلى عرض مريح" : "تبديل إلى عرض مضغوط";
      els.densityToggle.setAttribute("aria-label", next);
      els.densityToggle.setAttribute("title", next);
    }
  }

  function initThemeAndDensity() {
    const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
    const savedDensity = localStorage.getItem(DENSITY_STORAGE_KEY);
    const systemDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;

    applyTheme(savedTheme === "light" || savedTheme === "dark" ? savedTheme : systemDark ? "dark" : "light");
    applyDensity(savedDensity === "comfortable" || savedDensity === "compact" ? savedDensity : "compact");
  }

  async function copyResultToClipboard() {
    const payload = els.result.textContent || "";
    if (!payload.trim()) return;

    try {
      await navigator.clipboard.writeText(payload);
      if (els.copyResult) {
        els.copyResult.setAttribute("title", "تم النسخ");
        setTimeout(() => els.copyResult?.setAttribute("title", "نسخ الاستجابة"), 1200);
      }
      setResultMeta("success");
    } catch {
      if (els.copyResult) {
        els.copyResult.setAttribute("title", "تعذر النسخ");
        setTimeout(() => els.copyResult?.setAttribute("title", "نسخ الاستجابة"), 1200);
      }
      setResultMeta("error");
    }
  }

  function toggleResultPanel() {
    resultCollapsed = !resultCollapsed;
    els.result.classList.toggle("is-collapsed", resultCollapsed);
    if (els.toggleResult) {
      const label = resultCollapsed ? "توسيع الاستجابة" : "طي الاستجابة";
      els.toggleResult.setAttribute("title", label);
      els.toggleResult.setAttribute("aria-label", label);
    }
  }

  function applyControlsPanelVisibility(hidden) {
    controlsPanelHidden = Boolean(hidden);
    els.bentoGrid?.classList.toggle("controls-hidden", controlsPanelHidden);

    if (!els.toggleControlsPanel) return;

    const label = controlsPanelHidden ? "إظهار التحكم" : "إخفاء التحكم";
    els.toggleControlsPanel.setAttribute("aria-label", label);
    els.toggleControlsPanel.setAttribute("title", label);
    if (els.toggleControlsText) {
      els.toggleControlsText.textContent = label;
    }

    const icon = els.toggleControlsPanel.querySelector("i");
    if (icon) {
      icon.setAttribute("data-lucide", controlsPanelHidden ? "panel-right-open" : "panel-right-close");
      renderLucideIcons();
    }
  }

  function currentPeriodFilterValue() {
    return els.globalPeriod.value === "مسائي" ? "مسائي" : "صباحي";
  }

  function currentPeriodFilterLabel() {
    return currentPeriodFilterValue();
  }

  function resetSelectedView() {
    els.selectedRunText.textContent = "لم يتم اختيار تشغيل.";
    if (els.selectedRunMeta) els.selectedRunMeta.textContent = "آخر تحديث: --";
    els.runStatus.textContent = "-";
    els.runPeriod.textContent = "-";
    els.codesCount.textContent = "-";
    els.issuesCount.textContent = "-";
    els.codesBody.innerHTML = "";
    els.issuesBody.innerHTML = "";
    els.codesEmpty.style.display = "grid";
    els.issuesEmpty.style.display = "grid";

    cachedCodesRows = [];
    cachedHeatmapRows = [];
    selectedRunChecksReady = false;
    clearHeatmapPanels();
    syncActionButtons();
  }

  function checksPreconditionMessage(actionLabel) {
    return `يلزم تشغيل الفحوصات أولًا قبل ${actionLabel}.`;
  }

  function syncActionButtons() {
    const hasSelection = Boolean(selectedRunId);
    const checksReady = hasSelection && selectedRunChecksReady;

    [els.refreshRuns, els.refreshSelected, els.runPipeline, els.runChecks, els.importSs01].forEach((btn) => {
      if (!btn) return;
      btn.disabled = uiBusy;
    });

    if (els.publishRun) {
      els.publishRun.disabled = uiBusy || !checksReady;
      const publishHint = !hasSelection
        ? "اختر تشغيلًا أولًا"
        : checksReady
          ? "نشر النتائج"
          : checksPreconditionMessage("نشر النتائج");
      els.publishRun.title = publishHint;
      els.publishRun.setAttribute("aria-label", publishHint);
    }

    if (els.exportXlsx) {
      els.exportXlsx.disabled = uiBusy || !checksReady;
      const xlsxHint = !hasSelection
        ? "اختر تشغيلًا أولًا"
        : checksReady
          ? "تصدير Excel"
          : checksPreconditionMessage("تصدير Excel");
      els.exportXlsx.title = xlsxHint;
      els.exportXlsx.setAttribute("aria-label", xlsxHint);
    }

    if (els.exportPdf) {
      els.exportPdf.disabled = uiBusy || !checksReady;
      const pdfHint = !hasSelection
        ? "اختر تشغيلًا أولًا"
        : checksReady
          ? "تصدير PDF"
          : checksPreconditionMessage("تصدير PDF");
      els.exportPdf.title = pdfHint;
      els.exportPdf.setAttribute("aria-label", pdfHint);
    }
  }

  function setButtonState(isLoading) {
    uiBusy = Boolean(isLoading);
    syncActionButtons();
  }

  function parseDownloadName(contentDisposition, fallback = "download.bin") {
    const value = String(contentDisposition || "");
    const utf8Match = value.match(/filename\*=UTF-8''([^;]+)/i);
    if (utf8Match && utf8Match[1]) {
      try {
        return decodeURIComponent(utf8Match[1]);
      } catch {
        return utf8Match[1];
      }
    }
    const plainMatch = value.match(/filename=\"?([^\";]+)\"?/i);
    if (plainMatch && plainMatch[1]) {
      return plainMatch[1];
    }
    return fallback;
  }

  async function fetchFile(url, options = {}) {
    const res = await fetch(url, options);
    if (!res.ok) {
      const text = await res.text();
      let detail = text;
      try {
        const payload = text ? JSON.parse(text) : {};
        detail = payload?.detail || text || `HTTP ${res.status}`;
      } catch {
        detail = text || `HTTP ${res.status}`;
      }
      throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    }

    const blob = await res.blob();
    const fileName = parseDownloadName(
      res.headers.get("content-disposition"),
      options.fallbackName || "download.bin",
    );
    const contentType = res.headers.get("content-type") || blob.type || "application/octet-stream";
    return { blob, fileName, contentType };
  }

  function triggerFileDownload(blob, fileName) {
    const objectUrl = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = objectUrl;
    link.download = fileName || "download.bin";
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(objectUrl), 1500);
  }

  function setCurrentScreen(screenKey) {
    if (!HEATMAP_SCREEN_KEYS.includes(screenKey)) return;
    currentScreen = screenKey;

    els.screenTabs.forEach((tab) => {
      const active = tab.dataset.screen === currentScreen;
      tab.classList.toggle("active", active);
      tab.setAttribute("aria-selected", active ? "true" : "false");
    });

    els.screenPanels.forEach((panel) => {
      const active = panel.dataset.screenPanel === currentScreen;
      panel.classList.toggle("active", active);
      panel.hidden = !active;
    });
  }

  function initScreenTabs() {
    els.screenTabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        setCurrentScreen(tab.dataset.screen);
        renderHeatmapScreens();
      });
    });
    setCurrentScreen(currentScreen);
  }

  function makeSummaryChip(label, value) {
    const chip = document.createElement("span");
    chip.className = "summary-chip";
    chip.innerHTML = `${label}: <strong>${value}</strong>`;
    return chip;
  }

  function renderSummary(targetSummary, items) {
    if (!targetSummary) return;
    targetSummary.innerHTML = "";
    items.forEach(({ label, value }) => {
      targetSummary.appendChild(makeSummaryChip(label, value));
    });
  }

  function renderHeatmapEmpty(targetWrap, title, message = "لا توجد بيانات مطابقة للفلاتر الحالية.") {
    if (!targetWrap) return;
    targetWrap.innerHTML = "";
    const empty = document.createElement("div");
    empty.className = "heatmap-empty";
    empty.innerHTML = `
      <i data-lucide="layout-template"></i>
      <p>${title}</p>
      <small>${message}</small>
    `;
    targetWrap.appendChild(empty);
  }

  function clearHeatmapPanels() {
    Object.values(HEATMAP_TARGETS).forEach((target) => {
      if (target.summary) {
        target.summary.innerHTML = "";
      }
      renderHeatmapEmpty(target.wrap, `لا توجد بيانات لشاشة ${target.title}.`);
    });
    renderLucideIcons();
  }

  function matchesPeriodFilter(codeRow) {
    const filter = currentHeatmapPeriodValue();
    if (filter === "صباحي") {
      return codeRow.resolvedPeriod === "صباحي" || Boolean(codeRow.isMorning);
    }
    return codeRow.resolvedPeriod === "مسائي" || Boolean(codeRow.isEvening);
  }

  function matchesRowSearchFilter(codeRow, searchFilter) {
    if (!searchFilter) return true;
    const haystack = normalizeArabicText(
      [
        codeRow.room_code,
        codeRow.building_code,
        codeRow.crn,
        codeRow.course_code,
        codeRow.course_name,
        codeRow.trainer_name,
        codeRow.trainer_job_id,
        codeRow.department,
        codeRow.section_type,
      ]
        .filter(Boolean)
        .join(" "),
    );
    return haystack.includes(searchFilter);
  }

  function matchesAdvancedHeatmapFilters(codeRow, filters) {
    if (filters.department) {
      const department = normalizeArabicText(codeRow.department || "");
      if (!department.includes(filters.department)) return false;
    }

    if (filters.building) {
      const building = normalizeArabicText(codeRow.building_code || "");
      if (!building.includes(filters.building)) return false;
    }

    if (filters.crn) {
      const crn = normalizeArabicText(codeRow.crn || "");
      if (!crn.includes(filters.crn)) return false;
    }

    if (filters.trainer) {
      const trainerHaystack = normalizeArabicText(
        [codeRow.trainer_name, codeRow.trainer_job_id].filter(Boolean).join(" "),
      );
      if (!trainerHaystack.includes(filters.trainer)) return false;
    }

    return true;
  }

  function activeHeatmapRows() {
    const searchFilter = normalizeArabicText(els.heatmapSearchFilter?.value || "");
    const advancedFilters = {
      department: normalizeArabicText(els.heatmapDepartmentFilter?.value || ""),
      building: normalizeArabicText(els.heatmapBuildingFilter?.value || ""),
      crn: normalizeArabicText(els.heatmapCrnFilter?.value || ""),
      trainer: normalizeArabicText(els.heatmapTrainerFilter?.value || ""),
    };

    return cachedHeatmapRows.filter(
      (row) =>
        matchesPeriodFilter(row) &&
        matchesRowSearchFilter(row, searchFilter) &&
        matchesAdvancedHeatmapFilters(row, advancedFilters),
    );
  }

  function cellKey(dayOrder, slotIndex) {
    return `${dayOrder}-${slotIndex}`;
  }

  function getEntityDescriptor(screenKey, row) {
    if (screenKey === "rooms") {
      const roomCode = String(row.room_code || "غير-محدد");
      const buildingCode = String(row.building_code || "-");
      const roomCapacity = row.room_capacity == null ? "-" : row.room_capacity;
      return {
        key: `${buildingCode}|${roomCode}`,
        title: `قاعة ${roomCode}`,
        meta: `المبنى ${buildingCode} | السعة ${roomCapacity}`,
        sortValue: `${buildingCode}-${roomCode}`,
      };
    }

    if (screenKey === "crns") {
      const crn = String(row.crn || row.course_code || `ROW-${row.id || ""}`);
      const course = row.course_name || row.course_code || "-";
      const section = row.section_type || "-";
      return {
        key: crn,
        title: `شعبة ${crn}`,
        meta: `${course} | ${section}`,
        sortValue: crn,
      };
    }

    if (screenKey === "trainers") {
      const trainerId = String(row.trainer_job_id || row.trainer_name || `ROW-${row.id || ""}`);
      const trainerName = row.trainer_name || "مدرب غير محدد";
      const department = row.department || "-";
      return {
        key: trainerId,
        title: trainerName,
        meta: `الرقم الوظيفي ${trainerId} | ${department}`,
        sortValue: `${trainerName}-${trainerId}`,
      };
    }

    return null;
  }

  function enrichEntityRows(entitiesMap, dayOrders, slots) {
    const totalCells = dayOrders.length * slots.length;
    return Array.from(entitiesMap.values()).map((entity) => {
      let occupiedCells = 0;
      let conflictCells = 0;

      dayOrders.forEach((dayOrder) => {
        slots.forEach((slotIndex) => {
          const count = entity.cells.get(cellKey(dayOrder, slotIndex)) || 0;
          if (count > 0) occupiedCells += 1;
          if (count > 1) conflictCells += 1;
        });
      });

      return {
        ...entity,
        occupiedCells,
        conflictCells,
        emptyCells: totalCells - occupiedCells,
        occupancyRate: totalCells ? Math.round((occupiedCells * 100) / totalCells) : 0,
      };
    });
  }

  function matchesOccupancyFilter(entityRow, occupancyFilter) {
    if (occupancyFilter === "occupied") return entityRow.occupiedCells > 0;
    if (occupancyFilter === "empty") return entityRow.occupiedCells === 0;
    if (occupancyFilter === "conflict") return entityRow.conflictCells > 0;
    return true;
  }

  function buildEntityHeatmapData(screenKey, codeRows) {
    const entitiesMap = new Map();
    const dayOrders = [...DEFAULT_DAYS];
    const slots = [...DEFAULT_SLOTS];
    const scheduleSlots = getScheduleForPeriod(currentHeatmapPeriodValue());
    const occupancyFilter = els.heatmapOccupancyFilter?.value || "all";

    codeRows.forEach((row) => {
      const descriptor = getEntityDescriptor(screenKey, row);
      if (!descriptor) return;

      if (!entitiesMap.has(descriptor.key)) {
        entitiesMap.set(descriptor.key, {
          ...descriptor,
          cells: new Map(),
          sourceRows: 0,
          invalidRows: 0,
        });
      }

      const entity = entitiesMap.get(descriptor.key);
      entity.sourceRows += 1;

      const resolvedSlots = Array.isArray(row.slotIndices)
        ? row.slotIndices.filter((slotIndex) => Number.isInteger(slotIndex) && slotIndex >= 1 && slotIndex <= 8)
        : [];

      if (!row.dayOrder || resolvedSlots.length === 0) {
        entity.invalidRows += 1;
        return;
      }

      resolvedSlots.forEach((slotIndex) => {
        const key = cellKey(row.dayOrder, slotIndex);
        entity.cells.set(key, (entity.cells.get(key) || 0) + 1);
      });
    });

    const allRows = enrichEntityRows(entitiesMap, dayOrders, slots).sort((a, b) =>
      a.sortValue.localeCompare(b.sortValue, "ar"),
    );

    const afterOccupancy = allRows.filter((row) => matchesOccupancyFilter(row, occupancyFilter));
    const rows = afterOccupancy.slice(0, MAX_HEATMAP_ROWS);

    const summary = {
      totalEntities: allRows.length,
      visibleEntities: afterOccupancy.length,
      displayedEntities: rows.length,
      occupiedCells: rows.reduce((sum, row) => sum + row.occupiedCells, 0),
      conflictCells: rows.reduce((sum, row) => sum + row.conflictCells, 0),
      avgOccupancy:
        rows.length > 0
          ? Math.round(rows.reduce((sum, row) => sum + row.occupancyRate, 0) / rows.length)
          : 0,
    };

    return { dayOrders, slots, scheduleSlots, rows, summary };
  }

  function formatPercentValue(value) {
    if (!Number.isFinite(value)) return "0%";
    return `${Math.round(value)}%`;
  }

  function trainerEntityKey(row) {
    const byId = String(row.trainer_job_id || "").trim();
    if (byId) return byId;
    const byName = String(row.trainer_name || "").trim();
    if (byName) return byName;
    return "";
  }

  function buildDistributionHeatmapData(codeRows) {
    const dayOrders = [...DEFAULT_DAYS];
    const slots = [...DEFAULT_SLOTS];
    const trainerByCell = new Map();
    const uniqueTrainers = new Set();

    codeRows.forEach((row) => {
      if (!row.dayOrder || !Array.isArray(row.slotIndices) || row.slotIndices.length === 0) return;

      const trainerKey = trainerEntityKey(row);
      if (!trainerKey) return;
      uniqueTrainers.add(trainerKey);

      const validSlots = Array.from(
        new Set(
          row.slotIndices.filter((slotIndex) => Number.isInteger(slotIndex) && slotIndex >= 1 && slotIndex <= 8),
        ),
      );
      if (!validSlots.length) return;

      validSlots.forEach((slotIndex) => {
        const key = cellKey(row.dayOrder, slotIndex);
        if (!trainerByCell.has(key)) {
          trainerByCell.set(key, new Set());
        }
        trainerByCell.get(key).add(trainerKey);
      });
    });

    const weeklyCounts = new Map();
    const weeklyRatios = new Map();
    const dailyRatios = new Map();
    const dailyRatiosText = new Map();
    const weeklyHalfRatios = new Map();
    const dailyHalfRatios = new Map();
    const weeklyDayRatios = new Map();
    const dailyDayRatios = new Map();
    const slotRatios = new Map();
    const dayCounts = new Map();

    let totalOccupiedLoads = 0;
    let occupiedCells = 0;
    let maxCount = 0;
    let minCount = Number.POSITIVE_INFINITY;

    dayOrders.forEach((dayOrder) => {
      let dayCount = 0;
      slots.forEach((slotIndex) => {
        const key = cellKey(dayOrder, slotIndex);
        const count = (trainerByCell.get(key) || new Set()).size;
        weeklyCounts.set(key, count);
        dayCount += count;
        totalOccupiedLoads += count;
        if (count > 0) occupiedCells += 1;
        if (count > maxCount) maxCount = count;
        if (count < minCount) minCount = count;
      });
      dayCounts.set(dayOrder, dayCount);
    });

    if (!Number.isFinite(minCount)) minCount = 0;

    dayOrders.forEach((dayOrder) => {
      const dayTotal = dayCounts.get(dayOrder) || 0;
      let weeklyHalfA = 0;
      let weeklyHalfB = 0;
      let dailyHalfA = 0;
      let dailyHalfB = 0;

      slots.forEach((slotIndex) => {
        const key = cellKey(dayOrder, slotIndex);
        const count = weeklyCounts.get(key) || 0;
        const weeklyRatio = totalOccupiedLoads > 0 ? (count / totalOccupiedLoads) * 100 : 0;
        const dailyRatio = dayTotal > 0 ? (count / dayTotal) * 100 : null;

        weeklyRatios.set(key, weeklyRatio);
        dailyRatios.set(key, dailyRatio);
        dailyRatiosText.set(key, dayTotal > 0 ? formatPercentValue(dailyRatio) : "لا");

        if (slotIndex <= 4) {
          weeklyHalfA += weeklyRatio;
          dailyHalfA += Number.isFinite(dailyRatio) ? dailyRatio : 0;
        } else {
          weeklyHalfB += weeklyRatio;
          dailyHalfB += Number.isFinite(dailyRatio) ? dailyRatio : 0;
        }
      });

      weeklyHalfRatios.set(`${dayOrder}-first`, weeklyHalfA);
      weeklyHalfRatios.set(`${dayOrder}-second`, weeklyHalfB);
      dailyHalfRatios.set(`${dayOrder}-first`, dailyHalfA);
      dailyHalfRatios.set(`${dayOrder}-second`, dailyHalfB);

      const weeklyDayRatio = weeklyHalfA + weeklyHalfB;
      weeklyDayRatios.set(dayOrder, weeklyDayRatio);
      dailyDayRatios.set(dayOrder, totalOccupiedLoads > 0 ? (dayTotal / totalOccupiedLoads) * 100 : 0);
    });

    let firstPeriodRatio = 0;
    let secondPeriodRatio = 0;
    slots.forEach((slotIndex) => {
      let slotTotal = 0;
      dayOrders.forEach((dayOrder) => {
        slotTotal += weeklyRatios.get(cellKey(dayOrder, slotIndex)) || 0;
      });
      slotRatios.set(slotIndex, slotTotal);
      if (slotIndex <= 4) {
        firstPeriodRatio += slotTotal;
      } else {
        secondPeriodRatio += slotTotal;
      }
    });

    return {
      dayOrders,
      slots,
      weeklyCounts,
      weeklyRatios,
      weeklyHalfRatios,
      weeklyDayRatios,
      dailyRatiosText,
      dailyHalfRatios,
      dailyDayRatios,
      slotRatios,
      firstPeriodRatio,
      secondPeriodRatio,
      summary: {
        sourceRows: codeRows.length,
        uniqueTrainers: uniqueTrainers.size,
        occupiedCells,
        totalCells: dayOrders.length * slots.length,
        totalOccupiedLoads,
        maxCount,
      },
      heatScale: {
        minCount,
        maxCount,
      },
    };
  }

  function parseHexColor(hexValue) {
    const normalized = String(hexValue || "").replace("#", "").trim();
    if (normalized.length !== 6) return [0, 0, 0];
    return [
      Number.parseInt(normalized.slice(0, 2), 16),
      Number.parseInt(normalized.slice(2, 4), 16),
      Number.parseInt(normalized.slice(4, 6), 16),
    ];
  }

  function mixColor(a, b, ratio) {
    const safe = Math.max(0, Math.min(1, ratio));
    return [
      Math.round(a[0] + (b[0] - a[0]) * safe),
      Math.round(a[1] + (b[1] - a[1]) * safe),
      Math.round(a[2] + (b[2] - a[2]) * safe),
    ];
  }

  function colorToRgbText(rgb) {
    return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
  }

  function excelWeeklyHeatColor(value, minCount, maxCount) {
    const minColor = parseHexColor("FF8989");
    const midColor = parseHexColor("E9F5DB");
    const maxColor = parseHexColor("FFE38B");

    if (!Number.isFinite(value)) {
      return colorToRgbText(midColor);
    }
    if (!Number.isFinite(minCount) || !Number.isFinite(maxCount) || maxCount <= minCount) {
      return colorToRgbText(midColor);
    }

    const normalized = (value - minCount) / (maxCount - minCount);
    const clamped = Math.max(0, Math.min(1, normalized));
    if (clamped <= 0.5) {
      return colorToRgbText(mixColor(minColor, midColor, clamped / 0.5));
    }
    return colorToRgbText(mixColor(midColor, maxColor, (clamped - 0.5) / 0.5));
  }

  function createHeatCell(value, kind) {
    const cell = document.createElement("span");
    cell.className = "heat-cell";

    if (value == null || value === "") {
      cell.classList.add("heat-cell--empty");
      cell.textContent = "-";
      return cell;
    }

    const numeric = Number(value);
    if (kind === "percent") {
      const safe = Number.isFinite(numeric) ? numeric : 0;
      cell.classList.add("heat-cell--percent");
      cell.textContent = `${safe}%`;
      return cell;
    }

    if (!Number.isFinite(numeric) || numeric <= 0) {
      cell.classList.add("heat-cell--empty");
      cell.textContent = "0";
      return cell;
    }

    if (numeric === 1) {
      cell.classList.add("heat-cell--occupied");
      cell.textContent = "1";
      return cell;
    }

    cell.classList.add("heat-cell--conflict");
    cell.textContent = String(numeric);
    return cell;
  }

  function renderHeatmapTable(targetWrap, options) {
    if (!targetWrap) return;
    const { dayOrders, slots, scheduleSlots, rows, entityHeader } = options;
    targetWrap.innerHTML = "";

    if (!rows.length) {
      renderHeatmapEmpty(targetWrap, "لا توجد صفوف مطابقة.", "جرّب تعديل الفلاتر أو تشغيل المعالجة.");
      return;
    }

    const table = document.createElement("table");
    table.className = "heatmap-table";

    const thead = document.createElement("thead");
    const dayRow = document.createElement("tr");
    const slotNumberRow = document.createElement("tr");
    const slotStartRow = document.createElement("tr");
    const slotEndRow = document.createElement("tr");

    const entityTh = document.createElement("th");
    entityTh.className = "entity-col";
    entityTh.rowSpan = 4;
    entityTh.textContent = entityHeader;
    dayRow.appendChild(entityTh);

    const scheduleBySlot = (scheduleSlots || []).reduce((acc, row) => {
      acc[row.slot] = row;
      return acc;
    }, {});

    dayOrders.forEach((dayOrder) => {
      const isAltDay = dayOrder === 2 || dayOrder === 4;
      const dayTh = document.createElement("th");
      dayTh.colSpan = slots.length;
      dayTh.className = `day-group${isAltDay ? " day-alt" : ""}`;
      dayTh.textContent = DAY_LABEL_BY_ORDER[dayOrder] || String(dayOrder);
      dayRow.appendChild(dayTh);

      slots.forEach((slotIndex) => {
        const isDayStart = slotIndex === slots[0];
        const schedule = scheduleBySlot[slotIndex];

        const numberTh = document.createElement("th");
        numberTh.className = `slot-header slot-number${isDayStart ? " day-start" : ""}${isAltDay ? " day-alt" : ""}`;
        numberTh.textContent = String(slotIndex);
        slotNumberRow.appendChild(numberTh);

        const startTh = document.createElement("th");
        startTh.className = `slot-header slot-time${isDayStart ? " day-start" : ""}${isAltDay ? " day-alt" : ""}`;
        startTh.textContent = schedule ? schedule.startLabel : "-";
        slotStartRow.appendChild(startTh);

        const endTh = document.createElement("th");
        endTh.className = `slot-header slot-time${isDayStart ? " day-start" : ""}${isAltDay ? " day-alt" : ""}`;
        endTh.textContent = schedule ? schedule.endLabel : "-";
        slotEndRow.appendChild(endTh);
      });
    });

    thead.appendChild(dayRow);
    thead.appendChild(slotNumberRow);
    thead.appendChild(slotStartRow);
    thead.appendChild(slotEndRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    rows.forEach((row) => {
      const tr = document.createElement("tr");

      const labelTh = document.createElement("th");
      labelTh.scope = "row";

      const title = document.createElement("span");
      title.className = "heatmap-entity-title";
      title.textContent = row.title;

      const meta = document.createElement("span");
      meta.className = "heatmap-entity-meta";
      meta.textContent = row.meta || "-";

      labelTh.appendChild(title);
      labelTh.appendChild(meta);
      tr.appendChild(labelTh);

      dayOrders.forEach((dayOrder) => {
        const isAltDay = dayOrder === 2 || dayOrder === 4;
        slots.forEach((slotIndex) => {
          const td = document.createElement("td");
          if (slotIndex === slots[0]) {
            td.classList.add("day-start");
          }
          if (isAltDay) {
            td.classList.add("day-alt");
          }
          const value = row.cells.get(cellKey(dayOrder, slotIndex)) ?? 0;
          const numericValue = Number(value);
          if (row.kind !== "percent" && Number.isFinite(numericValue)) {
            if (numericValue === 1) {
              td.classList.add("cell-occupied-solid");
            } else if (numericValue > 1) {
              td.classList.add("cell-conflict-solid");
            }
          }
          td.appendChild(createHeatCell(value, row.kind || "binary"));
          tr.appendChild(td);
        });
      });

      tbody.appendChild(tr);
    });

    table.appendChild(tbody);
    targetWrap.appendChild(table);
  }

  function renderEntityScreen(screenKey, codeRows, entityHeader) {
    const target = HEATMAP_TARGETS[screenKey];
    if (!target) return;

    const data = buildEntityHeatmapData(screenKey, codeRows);
    renderSummary(target.summary, [
      { label: "إجمالي الصفوف", value: data.summary.totalEntities },
      { label: "مطابقة للفلاتر", value: data.summary.visibleEntities },
      { label: "خلايا مشغولة", value: data.summary.occupiedCells },
      { label: "خلايا متعارضة", value: data.summary.conflictCells },
      { label: "متوسط الإشغال", value: `${data.summary.avgOccupancy}%` },
    ]);

    if (data.summary.displayedEntities < data.summary.visibleEntities) {
      target.summary?.appendChild(
        makeSummaryChip("الحد الأقصى المعروض", `${data.summary.displayedEntities}/${data.summary.visibleEntities}`),
      );
    }

    renderHeatmapTable(target.wrap, {
      dayOrders: data.dayOrders,
      slots: data.slots,
      scheduleSlots: data.scheduleSlots,
      rows: data.rows,
      entityHeader,
    });
  }

  function renderDistributionScreen(codeRows) {
    const target = HEATMAP_TARGETS.distribution;
    if (!target) return;

    const data = buildDistributionHeatmapData(codeRows);
    renderSummary(target.summary, [
      { label: "صفوف المصدر", value: data.summary.sourceRows },
      { label: "المدربون الفريدون", value: data.summary.uniqueTrainers },
      { label: "إجمالي الإشغال", value: data.summary.totalOccupiedLoads },
      { label: "خلايا مشغولة", value: data.summary.occupiedCells },
      { label: "أعلى كثافة", value: data.summary.maxCount },
      {
        label: "نسبة الإشغال",
        value: formatPercentValue(
          data.summary.totalCells ? (data.summary.occupiedCells / data.summary.totalCells) * 100 : 0,
        ),
      },
    ]);

    target.wrap.innerHTML = "";
    if (!data.summary.uniqueTrainers) {
      renderHeatmapEmpty(target.wrap, "لا توجد بيانات مدربين بعد الفلترة.", "جرّب تعديل الفلاتر أو استيراد ملف جديد.");
      return;
    }

    const sections = document.createElement("div");
    sections.className = "distribution-sheet";

    function buildDayHeaderRow(dayOrders, slots) {
      const row = document.createElement("tr");
      dayOrders.forEach((dayOrder) => {
        const th = document.createElement("th");
        th.colSpan = slots.length;
        th.className = `dist-day-group${dayOrder === 2 || dayOrder === 4 ? " day-alt" : ""}`;
        th.textContent = DAY_LABEL_BY_ORDER[dayOrder] || String(dayOrder);
        row.appendChild(th);
      });
      return row;
    }

    function buildSlotsHeaderRow(dayOrders, slots) {
      const row = document.createElement("tr");
      dayOrders.forEach((dayOrder) => {
        const isAltDay = dayOrder === 2 || dayOrder === 4;
        slots.forEach((slotIndex) => {
          const th = document.createElement("th");
          th.className = `dist-slot-head${slotIndex === slots[0] ? " day-start" : ""}${isAltDay ? " day-alt" : ""}`;
          th.textContent = String(slotIndex);
          row.appendChild(th);
        });
      });
      return row;
    }

    function buildSlotValuesRow(dayOrders, slots, valueGetter, options = {}) {
      const row = document.createElement("tr");
      dayOrders.forEach((dayOrder) => {
        const isAltDay = dayOrder === 2 || dayOrder === 4;
        slots.forEach((slotIndex) => {
          const td = document.createElement("td");
          td.className = `dist-cell${slotIndex === slots[0] ? " day-start" : ""}${isAltDay ? " day-alt" : ""}${
            options.className ? ` ${options.className}` : ""
          }`;
          const key = cellKey(dayOrder, slotIndex);
          const raw = valueGetter(key, dayOrder, slotIndex);
          const text = options.formatter ? options.formatter(raw, key, dayOrder, slotIndex) : String(raw ?? "");
          td.textContent = text;
          if (options.heat) {
            td.style.background = excelWeeklyHeatColor(
              Number(raw) || 0,
              data.heatScale.minCount,
              data.heatScale.maxCount,
            );
          }
          row.appendChild(td);
        });
      });
      return row;
    }

    function buildHalfRow(dayOrders, firstGetter, secondGetter) {
      const row = document.createElement("tr");
      dayOrders.forEach((dayOrder) => {
        const isAltDay = dayOrder === 2 || dayOrder === 4;
        const first = document.createElement("td");
        first.colSpan = 4;
        first.className = `dist-cell dist-half${isAltDay ? " day-alt" : ""} day-start`;
        first.textContent = formatPercentValue(firstGetter(dayOrder));
        row.appendChild(first);

        const second = document.createElement("td");
        second.colSpan = 4;
        second.className = `dist-cell dist-half${isAltDay ? " day-alt" : ""}`;
        second.textContent = formatPercentValue(secondGetter(dayOrder));
        row.appendChild(second);
      });
      return row;
    }

    function buildDayTotalRow(dayOrders, dayGetter) {
      const row = document.createElement("tr");
      dayOrders.forEach((dayOrder) => {
        const isAltDay = dayOrder === 2 || dayOrder === 4;
        const td = document.createElement("td");
        td.colSpan = 8;
        td.className = `dist-cell dist-day-total${isAltDay ? " day-alt" : ""} day-start`;
        td.textContent = formatPercentValue(dayGetter(dayOrder));
        row.appendChild(td);
      });
      return row;
    }

    function buildSectionCard(titleText, buildBody) {
      const card = document.createElement("section");
      card.className = "distribution-block";

      const title = document.createElement("h4");
      title.className = "distribution-block-title";
      title.textContent = titleText;
      card.appendChild(title);

      const scroller = document.createElement("div");
      scroller.className = "distribution-scroll";

      const table = document.createElement("table");
      table.className = "distribution-table";
      const tbody = document.createElement("tbody");
      buildBody(tbody);
      table.appendChild(tbody);
      scroller.appendChild(table);
      card.appendChild(scroller);

      return card;
    }

    sections.appendChild(
      buildSectionCard("التوزيع الأسبوعي", (tbody) => {
        tbody.appendChild(buildDayHeaderRow(data.dayOrders, data.slots));
        tbody.appendChild(buildSlotsHeaderRow(data.dayOrders, data.slots));
        tbody.appendChild(
          buildSlotValuesRow(data.dayOrders, data.slots, (key) => data.weeklyCounts.get(key) || 0, {
            className: "dist-weekly-count",
            heat: true,
          }),
        );
        tbody.appendChild(
          buildSlotValuesRow(data.dayOrders, data.slots, (key) => data.weeklyRatios.get(key) || 0, {
            className: "dist-weekly-percent",
            formatter: (raw) => formatPercentValue(raw),
          }),
        );
        tbody.appendChild(
          buildHalfRow(
            data.dayOrders,
            (dayOrder) => data.weeklyHalfRatios.get(`${dayOrder}-first`) || 0,
            (dayOrder) => data.weeklyHalfRatios.get(`${dayOrder}-second`) || 0,
          ),
        );
        tbody.appendChild(buildDayTotalRow(data.dayOrders, (dayOrder) => data.weeklyDayRatios.get(dayOrder) || 0));
      }),
    );

    sections.appendChild(
      buildSectionCard("التوزيع اليومي", (tbody) => {
        tbody.appendChild(buildDayHeaderRow(data.dayOrders, data.slots));
        tbody.appendChild(buildSlotsHeaderRow(data.dayOrders, data.slots));
        tbody.appendChild(
          buildSlotValuesRow(data.dayOrders, data.slots, (key) => data.weeklyCounts.get(key) || 0, {
            className: "dist-daily-count",
          }),
        );
        tbody.appendChild(
          buildSlotValuesRow(data.dayOrders, data.slots, (key) => data.dailyRatiosText.get(key) || "لا", {
            className: "dist-daily-percent",
            formatter: (raw) => String(raw),
          }),
        );
        tbody.appendChild(
          buildHalfRow(
            data.dayOrders,
            (dayOrder) => data.dailyHalfRatios.get(`${dayOrder}-first`) || 0,
            (dayOrder) => data.dailyHalfRatios.get(`${dayOrder}-second`) || 0,
          ),
        );
        tbody.appendChild(buildDayTotalRow(data.dayOrders, (dayOrder) => data.dailyDayRatios.get(dayOrder) || 0));
      }),
    );

    sections.appendChild(
      buildSectionCard("توزيع الفترات", (tbody) => {
        const slotRow = document.createElement("tr");
        data.slots.forEach((slotIndex) => {
          const th = document.createElement("th");
          th.colSpan = 5;
          th.className = "dist-slot-group";
          th.textContent = String(slotIndex);
          slotRow.appendChild(th);
        });
        tbody.appendChild(slotRow);

        const ratioRow = document.createElement("tr");
        data.slots.forEach((slotIndex) => {
          const td = document.createElement("td");
          td.colSpan = 5;
          td.className = "dist-cell dist-slot-ratio";
          td.textContent = formatPercentValue(data.slotRatios.get(slotIndex) || 0);
          ratioRow.appendChild(td);
        });
        tbody.appendChild(ratioRow);

        const splitRow = document.createElement("tr");
        const first = document.createElement("td");
        first.colSpan = 20;
        first.className = "dist-cell dist-slot-total";
        first.textContent = formatPercentValue(data.firstPeriodRatio);
        splitRow.appendChild(first);

        const second = document.createElement("td");
        second.colSpan = 20;
        second.className = "dist-cell dist-slot-total";
        second.textContent = formatPercentValue(data.secondPeriodRatio);
        splitRow.appendChild(second);
        tbody.appendChild(splitRow);
      }),
    );

    target.wrap.appendChild(sections);
  }

  function renderHeatmapScreens() {
    const filteredRows = activeHeatmapRows();
    if (currentScreen === "rooms") {
      renderEntityScreen("rooms", filteredRows, "القاعة");
    } else if (currentScreen === "crns") {
      renderEntityScreen("crns", filteredRows, "الشعبة");
    } else if (currentScreen === "trainers") {
      renderEntityScreen("trainers", filteredRows, "المدرب");
    } else if (currentScreen === "distribution") {
      renderDistributionScreen(filteredRows);
    }
    renderLucideIcons();
  }

  function updateHeatmapSource(rows) {
    cachedCodesRows = rows;
    cachedHeatmapRows = buildHeatmapRows(rows);
    renderHeatmapScreens();
  }

  async function refreshHealth() {
    try {
      const data = await fetchJson("/health");
      els.healthDot.className = "status-dot ok";
      els.healthText.textContent = `${data.status} | ${data.environment}`;
    } catch (err) {
      els.healthDot.className = "status-dot err";
      els.healthText.textContent = `خطأ في الخدمة: ${err.message}`;
    }
  }

  async function loadRuns(options = {}) {
    const suppressResult = Boolean(options && options.suppressResult);
    try {
      setButtonState(true);
      const period = currentPeriodFilterValue();
      const periodQuery = `&period=${encodeURIComponent(period)}`;
      const data = await fetchJson(`/api/v1/mc/runs?page=1&size=50${periodQuery}`);
      const items = data.items || [];

      if (items.length && (!selectedRunId || !items.some((r) => r.id === selectedRunId))) {
        selectedRunId = items[0].id;
      } else if (!items.length) {
        selectedRunId = null;
      }

      renderRuns(items);
      if (selectedRunId) {
        await loadSelectedRun();
      } else {
        resetSelectedView();
      }

      if (!suppressResult) {
        putResult(
          {
            message: "تم تحميل التشغيلات",
            period_filter: currentPeriodFilterLabel(),
            total: data.total,
          },
          "success",
        );
      }
    } catch (err) {
      putResult(`فشل تحميل التشغيلات: ${err.message}`, "error");
    } finally {
      setButtonState(false);
    }
  }

  function renderRuns(items) {
    els.runList.innerHTML = "";
    if (!items.length) {
      const empty = document.createElement("div");
      empty.className = "empty-state glass-soft";
      empty.innerHTML = `
        <i data-lucide="inbox"></i>
        <p>لا توجد تشغيلات مطابقة للفلتر الحالي.</p>
        <small>غيّر فلتر الفترة أو استورد بيانات جديدة.</small>
      `;
      els.runList.appendChild(empty);
      renderLucideIcons();
      return;
    }

    items.forEach((run) => {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "run-item";
      card.dataset.runId = run.id;
      if (selectedRunId === run.id) {
        card.classList.add("active");
      }
      card.addEventListener("click", () => selectRun(run.id));

      const top = document.createElement("div");
      top.className = "run-item-top";

      const idWrap = document.createElement("div");
      idWrap.className = "run-id-wrap";

      const icon = document.createElement("i");
      icon.setAttribute("data-lucide", "workflow");
      icon.className = "icon";

      const id = document.createElement("span");
      id.className = "run-id";
      id.textContent = run.id;

      idWrap.appendChild(icon);
      idWrap.appendChild(id);

      const badge = document.createElement("span");
      badge.className = `state-pill ${statusClass(run.status)}`;
      badge.textContent = statusLabel(run.status);

      top.appendChild(idWrap);
      top.appendChild(badge);

      const meta = document.createElement("div");
      meta.className = "run-meta";

      const semester = document.createElement("span");
      semester.textContent = `الفصل: ${run.semester || "-"}`;

      const period = document.createElement("span");
      period.textContent = `الفترة: ${run.period || "-"}`;

      meta.appendChild(semester);
      meta.appendChild(period);

      card.appendChild(top);
      card.appendChild(meta);
      els.runList.appendChild(card);
    });

    renderLucideIcons();
  }

  async function selectRun(runId) {
    selectedRunId = runId;
    selectedRunChecksReady = false;
    syncActionButtons();
    document.querySelectorAll(".run-item").forEach((item) => {
      item.classList.toggle("active", item.dataset.runId === runId);
    });
    await loadSelectedRun();
  }

  async function loadSelectedRun() {
    if (!selectedRunId) {
      resetSelectedView();
      return;
    }

    const requestedRunId = selectedRunId;
    els.selectedRunText.textContent = `معرف التشغيل: ${requestedRunId}`;

    try {
      const [runData, codesData, issuesData] = await Promise.all([
        fetchJson(`/api/v1/mc/runs/${requestedRunId}`),
        fetchAllPages(`/api/v1/mc/runs/${requestedRunId}/codes`),
        fetchAllPages(`/api/v1/mc/runs/${requestedRunId}/issues`),
      ]);

      if (selectedRunId !== requestedRunId) {
        return;
      }

      const run = runData.run || {};
      const codesItems = codesData.items || [];
      const issuesItems = issuesData.items || [];
      selectedRunChecksReady = Boolean(runData?.metrics?.checks_ready);
      syncActionButtons();

      if ((run.period === "صباحي" || run.period === "مسائي") && els.heatmapPeriodFilter) {
        els.heatmapPeriodFilter.value = run.period;
      }
      if ((run.period === "صباحي" || run.period === "مسائي") && els.importPeriod) {
        els.importPeriod.value = run.period;
      }
      if (run.semester && els.importSemester && !String(els.importSemester.value || "").trim()) {
        els.importSemester.value = run.semester;
      }

      els.runStatus.textContent = statusLabel(run.status);
      els.runPeriod.textContent = run.period || "-";
      if (els.selectedRunMeta) {
        const stamped = formatDateTime(run.updated_at || run.created_at || run.finished_at || run.started_at);
        els.selectedRunMeta.textContent = stamped ? `آخر تحديث: ${stamped}` : "آخر تحديث: --";
      }
      els.codesCount.textContent = String(codesData.total || codesItems.length);
      els.issuesCount.textContent = String(issuesData.total || issuesItems.length);

      renderCodes(codesItems);
      renderIssues(issuesItems);
      updateHeatmapSource(codesItems);
    } catch (err) {
      selectedRunChecksReady = false;
      syncActionButtons();
      putResult(`فشل تحميل التشغيل المحدد: ${err.message}`, "error");
    }
  }

  function renderCodes(items) {
    els.codesBody.innerHTML = "";
    els.codesEmpty.style.display = items.length ? "none" : "grid";

    items.forEach((row) => {
      const tr = document.createElement("tr");

      const idTd = document.createElement("td");
      idTd.textContent = row.id == null ? "" : String(row.id);

      const crnTd = document.createElement("td");
      crnTd.textContent = row.crn == null ? "" : String(row.crn);

      const dayTd = document.createElement("td");
      dayTd.appendChild(buildChip(row.day_name || "-", "table-chip--neutral"));

      const timeTd = document.createElement("td");
      timeTd.textContent = row.time_value == null ? "" : String(row.time_value);

      const roomTd = document.createElement("td");
      roomTd.appendChild(buildChip(row.room_code || "-", "table-chip--ok"));

      const trainerTd = document.createElement("td");
      trainerTd.textContent = row.trainer_name || "";

      tr.appendChild(idTd);
      tr.appendChild(crnTd);
      tr.appendChild(dayTd);
      tr.appendChild(timeTd);
      tr.appendChild(roomTd);
      tr.appendChild(trainerTd);

      els.codesBody.appendChild(tr);
    });
  }

  function renderIssues(items) {
    els.issuesBody.innerHTML = "";
    els.issuesEmpty.style.display = items.length ? "none" : "grid";

    items.forEach((row) => {
      const tr = document.createElement("tr");

      const idTd = document.createElement("td");
      idTd.textContent = row.id == null ? "" : String(row.id);

      const ruleTd = document.createElement("td");
      const ruleChip = document.createElement("span");
      ruleChip.className = "table-chip table-chip--warn";
      ruleChip.textContent = row.rule_code || "-";
      ruleTd.appendChild(ruleChip);

      const severityTd = document.createElement("td");
      const severityChip = document.createElement("span");
      severityChip.className = `table-chip ${severityClass(row.severity)}`;
      severityChip.textContent = row.severity || "-";
      severityTd.appendChild(severityChip);

      const messageTd = document.createElement("td");
      messageTd.textContent = row.message || "";

      tr.appendChild(idTd);
      tr.appendChild(ruleTd);
      tr.appendChild(severityTd);
      tr.appendChild(messageTd);

      els.issuesBody.appendChild(tr);
    });
  }

  async function runPipeline() {
    if (!selectedRunId) {
      putResult("اختر تشغيلًا أولًا.", "info");
      return;
    }

    try {
      setButtonState(true);
      const data = await fetchJson("/api/v1/mc/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          run_id: selectedRunId,
          created_by: els.createdBy.value || "واجهة-ويب",
        }),
      });

      putResult(data, "success");
      await loadRuns();
    } catch (err) {
      putResult(`فشل تشغيل المعالجة: ${err.message}`, "error");
    } finally {
      setButtonState(false);
    }
  }

  async function runChecks() {
    if (!selectedRunId) {
      putResult("اختر تشغيلًا أولًا.", "info");
      return;
    }

    try {
      setButtonState(true);
      const data = await fetchJson("/api/v1/mc/checks/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          run_id: selectedRunId,
          created_by: els.createdBy.value || "واجهة-ويب",
        }),
      });

      putResult(data, "success");
      await loadRuns();
    } catch (err) {
      putResult(`فشل تشغيل الفحوصات: ${err.message}`, "error");
    } finally {
      setButtonState(false);
    }
  }

  async function publishSelectedRun() {
    if (!selectedRunId) {
      putResult("اختر تشغيلًا أولًا.", "info");
      return;
    }
    if (!selectedRunChecksReady) {
      putResult(checksPreconditionMessage("نشر النتائج"), "info");
      return;
    }

    try {
      setButtonState(true);
      const actor = encodeURIComponent(els.createdBy.value || "واجهة-ويب");
      const data = await fetchJson(`/api/v1/mc/runs/${selectedRunId}/publish?created_by=${actor}`, {
        method: "POST",
      });
      putResult(data, "success");
      await loadRuns({ suppressResult: true });
      await loadSelectedRun();
    } catch (err) {
      const rawMessage = String(err?.message || "");
      if (rawMessage.includes("Run checks must be executed before publishing")) {
        putResult(checksPreconditionMessage("نشر النتائج"), "info");
        return;
      }
      putResult(`فشل نشر النتائج: ${rawMessage}`, "error");
    } finally {
      setButtonState(false);
    }
  }

  async function exportSelectedRun(kind) {
    if (!selectedRunId) {
      putResult("اختر تشغيلًا أولًا.", "info");
      return;
    }
    const normalizedKind = kind === "pdf" ? "pdf" : "xlsx";
    if (!selectedRunChecksReady) {
      const exportLabel = normalizedKind === "pdf" ? "تصدير PDF" : "تصدير Excel";
      putResult(checksPreconditionMessage(exportLabel), "info");
      return;
    }
    const endpoint =
      normalizedKind === "pdf"
        ? `/api/v1/mc/runs/${selectedRunId}/export.pdf`
        : `/api/v1/mc/runs/${selectedRunId}/export.xlsx`;
    const fallbackName = normalizedKind === "pdf" ? "mc_export.pdf" : "mc_export.xlsx";

    try {
      setButtonState(true);
      const actor = encodeURIComponent(els.createdBy.value || "واجهة-ويب");
      const { blob, fileName } = await fetchFile(`${endpoint}?created_by=${actor}`, {
        method: "GET",
        fallbackName,
      });
      triggerFileDownload(blob, fileName);
      putResult(
        {
          message: normalizedKind === "pdf" ? "تم إنشاء ملف PDF." : "تم إنشاء ملف Excel.",
          run_id: selectedRunId,
          file_name: fileName,
        },
        "success",
      );
      await loadSelectedRun();
    } catch (err) {
      const rawMessage = String(err?.message || "");
      if (rawMessage.includes("Run checks must be executed before publishing")) {
        const exportLabel = normalizedKind === "pdf" ? "تصدير PDF" : "تصدير Excel";
        putResult(checksPreconditionMessage(exportLabel), "info");
        return;
      }
      putResult(
        normalizedKind === "pdf"
          ? `فشل تصدير PDF: ${rawMessage}`
          : `فشل تصدير Excel: ${rawMessage}`,
        "error",
      );
    } finally {
      setButtonState(false);
    }
  }

  async function importSs01() {
    const file = els.importFile?.files?.[0];
    if (!file) {
      putResult("اختر ملف CSV أولًا للاستيراد.", "info");
      return;
    }

    const semester = String(els.importSemester?.value || "").trim();
    if (!semester) {
      putResult("أدخل الفصل قبل الاستيراد.", "info");
      return;
    }

    const period = els.importPeriod?.value === "مسائي" ? "مسائي" : "صباحي";
    const createdBy = String(els.createdBy?.value || "واجهة-ويب").trim() || "واجهة-ويب";

    try {
      setButtonState(true);
      const formData = new FormData();
      formData.append("file", file, file.name);
      formData.append("semester", semester);
      formData.append("period", period);
      formData.append("created_by", createdBy);

      const importData = await fetchJson("/api/v1/mc/import/ss01", {
        method: "POST",
        body: formData,
      });
      const importedRunId = importData?.result?.run_id;
      if (!importedRunId) {
        throw new Error("الاستيراد نجح لكن لم يتم إرجاع معرف تشغيل.");
      }

      if (els.globalPeriod) {
        els.globalPeriod.value = period;
      }
      if (els.heatmapPeriodFilter) {
        els.heatmapPeriodFilter.value = period;
      }
      if (els.importPeriod) {
        els.importPeriod.value = period;
      }
      localStorage.setItem(GLOBAL_PERIOD_STORAGE_KEY, period);

      selectedRunId = importedRunId;
      let pipelineData = null;
      let pipelineError = null;

      try {
        pipelineData = await fetchJson("/api/v1/mc/run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            run_id: importedRunId,
            created_by: createdBy,
          }),
        });
      } catch (err) {
        pipelineError = err;
      }

      await loadRuns({ suppressResult: true });
      if (pipelineError) {
        putResult(
          {
            message: "تم استيراد SS01 لكن فشلت المعالجة التلقائية.",
            run_id: importedRunId,
            import_result: importData.result || {},
            pipeline_error: pipelineError.message,
          },
          "error",
        );
        return;
      }

      putResult(
        {
          message: "تم استيراد SS01 وتشغيل المعالجة تلقائيًا.",
          run_id: importedRunId,
          import_result: importData.result || {},
          pipeline_result: pipelineData?.result || {},
        },
        "success",
      );
    } catch (err) {
      putResult(`فشل استيراد SS01: ${err.message}`, "error");
    } finally {
      setButtonState(false);
    }
  }

  els.refreshRuns.addEventListener("click", loadRuns);
  els.refreshSelected.addEventListener("click", loadSelectedRun);
  els.runPipeline.addEventListener("click", runPipeline);
  els.runChecks.addEventListener("click", runChecks);
  els.publishRun?.addEventListener("click", publishSelectedRun);
  els.exportXlsx?.addEventListener("click", () => exportSelectedRun("xlsx"));
  els.exportPdf?.addEventListener("click", () => exportSelectedRun("pdf"));
  els.importSs01?.addEventListener("click", importSs01);
  els.copyResult?.addEventListener("click", copyResultToClipboard);
  els.toggleResult?.addEventListener("click", toggleResultPanel);
  els.themeToggle?.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    const next = current === "dark" ? "light" : "dark";
    applyTheme(next);
    localStorage.setItem(THEME_STORAGE_KEY, next);
  });
  els.densityToggle?.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-density") || "compact";
    const next = current === "compact" ? "comfortable" : "compact";
    applyDensity(next);
    localStorage.setItem(DENSITY_STORAGE_KEY, next);
  });
  els.toggleControlsPanel?.addEventListener("click", () => {
    const nextState = !controlsPanelHidden;
    applyControlsPanelVisibility(nextState);
    localStorage.setItem(CONTROLS_PANEL_STORAGE_KEY, String(nextState));
  });

  els.globalPeriod.addEventListener("change", async () => {
    localStorage.setItem(GLOBAL_PERIOD_STORAGE_KEY, currentPeriodFilterValue());
    if (els.heatmapPeriodFilter) {
      els.heatmapPeriodFilter.value = currentPeriodFilterValue();
    }
    if (els.importPeriod) {
      els.importPeriod.value = currentPeriodFilterValue();
    }
    renderHeatmapScreens();
    await loadRuns();
  });

  els.heatmapPeriodFilter?.addEventListener("change", renderHeatmapScreens);
  els.heatmapOccupancyFilter?.addEventListener("change", renderHeatmapScreens);
  els.heatmapSearchFilter?.addEventListener("input", renderHeatmapScreens);
  els.heatmapDepartmentFilter?.addEventListener("input", renderHeatmapScreens);
  els.heatmapBuildingFilter?.addEventListener("input", renderHeatmapScreens);
  els.heatmapCrnFilter?.addEventListener("input", renderHeatmapScreens);
  els.heatmapTrainerFilter?.addEventListener("input", renderHeatmapScreens);

  (async function init() {
    initThemeAndDensity();
    initScreenTabs();

    const savedPeriod = localStorage.getItem(GLOBAL_PERIOD_STORAGE_KEY);
    if (savedPeriod && ["صباحي", "مسائي"].includes(savedPeriod)) {
      els.globalPeriod.value = savedPeriod;
    } else {
      els.globalPeriod.value = "صباحي";
    }

    if (els.heatmapPeriodFilter) {
      els.heatmapPeriodFilter.value = currentPeriodFilterValue();
    }
    if (els.importPeriod) {
      els.importPeriod.value = currentPeriodFilterValue();
    }

    const savedControlsHidden = localStorage.getItem(CONTROLS_PANEL_STORAGE_KEY) === "true";
    applyControlsPanelVisibility(savedControlsHidden);

    clearHeatmapPanels();
    setButtonState(false);
    renderLucideIcons();
    setResultMeta("info");
    await refreshHealth();
    await loadRuns();
  })();
});
