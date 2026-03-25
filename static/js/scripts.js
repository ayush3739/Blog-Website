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

/* ══════════════════════════════════════════════════════════════════
   Copy to Clipboard Functionality for Code Blocks
══════════════════════════════════════════════════════════════════ */

(function() {
  'use strict';

  /**
   * Copy text to clipboard using modern API with fallback
   * @param {string} text - Text to copy
   * @returns {Promise<boolean>} - Success status
   */
  async function copyToClipboard(text) {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        return true;
      } else {
        // Fallback for older browsers
        return fallbackCopyTextToClipboard(text);
      }
    } catch (err) {
      console.error('Failed to copy text: ', err);
      return false;
    }
  }

  /**
   * Fallback copy method for older browsers
   * @param {string} text - Text to copy
   * @returns {boolean} - Success status
   */
  function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      const successful = document.execCommand('copy');
      document.body.removeChild(textArea);
      return successful;
    } catch (err) {
      console.error('Fallback copy failed: ', err);
      document.body.removeChild(textArea);
      return false;
    }
  }

  /**
   * Create copy button element
   * @returns {HTMLElement} - Copy button element
   */
  function createCopyButton() {
    const button = document.createElement('button');
    button.className = 'code-copy-btn';
    button.setAttribute('aria-label', 'Copy code to clipboard');
    button.innerHTML = `
      <span class="material-symbols-outlined">content_copy</span>
      <span class="copy-text">Copy</span>
    `;
    return button;
  }

  /**
   * Handle copy button click
   * @param {Event} event - Click event
   */
  async function handleCopyClick(event) {
    event.preventDefault();
    const button = event.currentTarget;
    const codeBlock = button.closest('pre');
    const codeContent = codeBlock.querySelector('code') || codeBlock;

    // Get text content without HTML tags
    let textToCopy = codeContent.textContent || codeContent.innerText;

    // Remove any extra whitespace and normalize line endings
    textToCopy = textToCopy.replace(/^\s+|\s+$/g, '').replace(/\r\n/g, '\n');

    const success = await copyToClipboard(textToCopy);

    if (success) {
      // Visual feedback - change to checkmark
      button.classList.add('copied');
      const iconSpan = button.querySelector('.material-symbols-outlined');
      const textSpan = button.querySelector('.copy-text');

      iconSpan.textContent = 'check';
      textSpan.textContent = 'Copied!';

      // Reset after 2 seconds
      setTimeout(() => {
        button.classList.remove('copied');
        iconSpan.textContent = 'content_copy';
        textSpan.textContent = 'Copy';
      }, 2000);
    } else {
      // Error feedback
      const textSpan = button.querySelector('.copy-text');
      textSpan.textContent = 'Failed';
      setTimeout(() => {
        textSpan.textContent = 'Copy';
      }, 2000);
    }
  }

  /**
   * Add copy buttons to all code blocks
   */
  function addCopyButtonsToCodeBlocks() {
    const codeBlocks = document.querySelectorAll('.article-content pre');

    codeBlocks.forEach(codeBlock => {
      // Skip if button already exists
      if (codeBlock.querySelector('.code-copy-btn')) {
        return;
      }

      const copyButton = createCopyButton();
      copyButton.addEventListener('click', handleCopyClick);
      codeBlock.appendChild(copyButton);
    });
  }

  /**
   * Initialize copy functionality
   */
  function initCopyFunctionality() {
    // Add copy buttons to existing code blocks
    addCopyButtonsToCodeBlocks();

    // Watch for dynamically added content (like from AJAX)
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === 1) { // Element node
            // Check if the added node contains code blocks
            if (node.matches && node.matches('.article-content pre')) {
              addCopyButtonsToCodeBlocks();
            } else if (node.querySelector && node.querySelector('.article-content pre')) {
              addCopyButtonsToCodeBlocks();
            }
          }
        });
      });
    });

    // Start observing the document for changes
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  /**
   * Initialize on DOM ready
   */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCopyFunctionality);
  } else {
    initCopyFunctionality();
  }
})();
