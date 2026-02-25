(() => {
  const ICON_MARKUP = {
    default: "<circle cx='12' cy='12' r='8'></circle><path d='M9 12h6'></path>",
    "activity": "<polyline points='22 12 18 12 15 21 9 3 6 12 2 12'></polyline>",
    "badge-check": "<circle cx='12' cy='12' r='9'></circle><path d='M9 12l2 2 4-4'></path>",
    "book-open-text": "<path d='M3 5a3 3 0 0 1 3-3h6v18H6a3 3 0 0 0-3 3z'></path><path d='M21 5a3 3 0 0 0-3-3h-6v18h6a3 3 0 0 1 3 3z'></path><path d='M8 8h2'></path><path d='M8 12h2'></path>",
    "calendar-days": "<rect x='3' y='4' width='18' height='17' rx='2'></rect><path d='M8 2v4M16 2v4M3 9h18'></path>",
    "chevrons-up-down": "<path d='M7 15l5 5 5-5'></path><path d='M7 9l5-5 5 5'></path>",
    "clipboard-list": "<rect x='5' y='4' width='14' height='17' rx='2'></rect><path d='M9 4h6v3H9zM9 10h6M9 14h6M9 18h4'></path>",
    "copy": "<rect x='9' y='9' width='11' height='11' rx='2'></rect><rect x='4' y='4' width='11' height='11' rx='2'></rect>",
    "file-json": "<path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'></path><path d='M14 2v6h6'></path><path d='M10 16c-1 0-1-1-1-2s0-2-1-2c1 0 1-1 1-2s0-2 1-2M14 8c1 0 1 1 1 2s0 2 1 2c-1 0-1 1-1 2s0 2-1 2'></path>",
    "file-spreadsheet": "<path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'></path><path d='M14 2v6h6'></path><path d='M8 13h8M8 17h8M12 13v6'></path>",
    "file-text": "<path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'></path><path d='M14 2v6h6'></path><path d='M8 13h8M8 17h8M8 9h3'></path>",
    "file-up": "<path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'></path><path d='M14 2v6h6'></path><path d='M12 17V11'></path><path d='M9.5 13.5L12 11l2.5 2.5'></path>",
    "inbox": "<path d='M22 12v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-6'></path><path d='M2 12l3-7a2 2 0 0 1 2-1h10a2 2 0 0 1 2 1l3 7'></path><path d='M7 12h10v2a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2z'></path>",
    "layers-3": "<path d='M12 3l9 5-9 5-9-5 9-5z'></path><path d='M3 12l9 5 9-5'></path><path d='M3 16l9 5 9-5'></path>",
    "layout-grid": "<rect x='3' y='3' width='18' height='18' rx='2'></rect><path d='M3 12h18M12 3v18'></path>",
    "layout-template": "<rect x='3' y='3' width='18' height='18' rx='2'></rect><path d='M9 3v18M9 9h12'></path>",
    "panel-right-close": "<rect x='3' y='3' width='18' height='18' rx='2'></rect><path d='M15 3v18'></path><path d='M10 12l3-3v6z'></path>",
    "panel-right-open": "<rect x='3' y='3' width='18' height='18' rx='2'></rect><path d='M9 3v18'></path><path d='M14 12l-3-3v6z'></path>",
    "panel-top-close": "<rect x='3' y='3' width='18' height='18' rx='2'></rect><path d='M3 9h18'></path><path d='M10 14l2-2 2 2'></path>",
    "play": "<polygon points='8 5 19 12 8 19 8 5'></polygon>",
    "refresh-ccw": "<path d='M3 12a9 9 0 0 1 15-6'></path><path d='M3 4v6h6'></path><path d='M21 12a9 9 0 0 1-15 6'></path>",
    "refresh-cw": "<path d='M21 12a9 9 0 0 1-15 6'></path><path d='M21 20v-6h-6'></path><path d='M3 12a9 9 0 0 1 15-6'></path>",
    "send": "<path d='M22 2L11 13'></path><path d='M22 2L15 22l-4-9-9-4z'></path>",
    "shield-alert": "<path d='M12 3l8 3v6c0 5-3.5 7.5-8 9-4.5-1.5-8-4-8-9V6z'></path><path d='M12 8v5'></path><circle cx='12' cy='16' r='1'></circle>",
    "shield-check": "<path d='M12 3l8 3v6c0 5-3.5 7.5-8 9-4.5-1.5-8-4-8-9V6z'></path><path d='M9 12l2 2 4-4'></path>",
    "sun-moon": "<path d='M12 3a7 7 0 1 0 9 9 8 8 0 1 1-9-9z'></path>",
    "table-properties": "<rect x='3' y='4' width='18' height='16' rx='2'></rect><path d='M3 10h18M9 4v16M15 4v16'></path>",
    "triangle-alert": "<path d='M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z'></path><path d='M12 9v4'></path><circle cx='12' cy='16' r='1'></circle>",
    "upload-cloud": "<path d='M20 16.6A4.5 4.5 0 0 0 18 8a6 6 0 0 0-11.6 2A4 4 0 0 0 6 18h12'></path><path d='M12 17V10'></path><path d='M9.5 12.5L12 10l2.5 2.5'></path>",
    "user-cog": "<circle cx='10' cy='8' r='3'></circle><path d='M4 20a6 6 0 0 1 12 0'></path><circle cx='18' cy='17' r='2.5'></circle><path d='M18 13.5v1M18 19.5v1M15.5 17h1M19.5 17h1'></path>",
    "workflow": "<circle cx='6' cy='6' r='2'></circle><circle cx='18' cy='6' r='2'></circle><circle cx='12' cy='18' r='2'></circle><path d='M8 6h8M7 8l4 8M17 8l-4 8'></path>"
  };

  function buildSvgMarkup(name) {
    const body = ICON_MARKUP[name] || ICON_MARKUP.default;
    return `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>${body}</svg>`;
  }

  function createIcons(options = {}) {
    const root = options.root || document;
    const nodes = root.querySelectorAll("[data-lucide]");
    nodes.forEach((node) => {
      const name = node.getAttribute("data-lucide");
      if (!name) return;
      node.innerHTML = buildSvgMarkup(name);
      node.setAttribute("data-lucide-rendered", "true");
    });
  }

  window.lucide = window.lucide || {};
  window.lucide.createIcons = createIcons;
})();
