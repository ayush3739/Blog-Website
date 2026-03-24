/* ══════════════════════════════════════════════════════════════════
   BlogPy - Unified JavaScript
   Theme toggle functionality for all pages
══════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  const html = document.documentElement;
  const STORAGE_KEY = 'blogpy-theme';

  /**
   * Initialize theme on page load
   */
  function initTheme() {
    // Check localStorage for saved preference, default to 'dark'
    const savedTheme = localStorage.getItem(STORAGE_KEY) || 'dark';

    // Apply theme class
    if (savedTheme === 'dark') {
      html.classList.add('dark');
      html.classList.remove('light');
    } else {
      html.classList.add('light');
      html.classList.remove('dark');
    }

    // Update icon if theme toggle button exists
    updateThemeIcon(savedTheme);
  }

  /**
   * Toggle between light and dark themes
   */
  function toggleTheme() {
    const isDark = html.classList.contains('dark');
    const newTheme = isDark ? 'light' : 'dark';

    // Toggle classes
    if (isDark) {
      html.classList.replace('dark', 'light');
    } else {
      html.classList.replace('light', 'dark');
    }

    // Save preference
    localStorage.setItem(STORAGE_KEY, newTheme);

    // Update icon
    updateThemeIcon(newTheme);
  }

  /**
   * Update theme toggle icon based on current theme
   * @param {string} theme - Current theme ('light' or 'dark')
   */
  function updateThemeIcon(theme) {
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      // Update icon text
      toggleBtn.textContent = theme === 'dark' ? 'light_mode' : 'dark_mode';
    }
  }

  /**
   * Setup event listeners
   */
  function setupEventListeners() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggleTheme);
    }
  }

  /**
   * Initialize on DOM ready
   */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initTheme();
      setupEventListeners();
    });
  } else {
    initTheme();
    setupEventListeners();
  }

  // Expose toggleTheme to global scope for inline onclick handlers (if needed)
  window.toggleTheme = toggleTheme;
})();
