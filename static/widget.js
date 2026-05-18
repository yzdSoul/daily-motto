/**
 * Widget Theme Manager
 * - Auto-detect system color scheme via prefers-color-scheme
 * - Manual toggle button to override
 * - Persist choice in localStorage
 */
(function() {
  const STORAGE_KEY = 'widget-theme';

  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function getSavedTheme() {
    return localStorage.getItem(STORAGE_KEY);
  }

  function applyTheme(theme) {
    const html = document.documentElement;
    html.classList.remove('light', 'dark');
    html.classList.add(theme);
  }

  function setTheme(theme) {
    applyTheme(theme);
    localStorage.setItem(STORAGE_KEY, theme);
  }

  function toggleTheme() {
    const current = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    setTheme(current === 'dark' ? 'light' : 'dark');
  }

  // Initialize
  const saved = getSavedTheme();
  if (saved) {
    applyTheme(saved);
  } else {
    applyTheme(getSystemTheme());
  }

  // Listen for system theme changes (only when no saved override)
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (!getSavedTheme()) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  // Expose toggle function for the button
  window.widgetToggleTheme = toggleTheme;
})();
