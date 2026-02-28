/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });

    // ================================
    // GLOBAL NOTIFICATION SYSTEM
    // ================================
    function showNotification(notification) {
        const toastEl = document.getElementById('globalToast');
        const toastTitle = document.getElementById('toastTitle');
        const toastMessage = document.getElementById('toastMessage');
        const toastIcon = document.getElementById('toastIcon');
        
        if (!toastEl || !toastTitle || !toastMessage) return;
        
        // Set notification content
        toastTitle.textContent = notification.title || 'Notification';
        toastMessage.innerHTML = notification.message || '';
        
        // Set icon based on type
        if (toastIcon) {
            toastIcon.className = 'fas me-2';
            if (notification.type === 'success') {
                toastIcon.classList.add('fa-check-circle', 'text-success');
            } else if (notification.type === 'error') {
                toastIcon.classList.add('fa-exclamation-circle', 'text-danger');
            } else if (notification.type === 'warning') {
                toastIcon.classList.add('fa-exclamation-triangle', 'text-warning');
            } else {
                toastIcon.classList.add('fa-info-circle', 'text-info');
            }
        }
        
        // Show the toast
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    }
    
    function checkPendingNotifications() {
        const pending = localStorage.getItem('pendingNotification');
        if (pending) {
            try {
                const notification = JSON.parse(pending);
                // Small delay to ensure page is fully rendered
                setTimeout(() => {
                    showNotification(notification);
                }, 300);
                // Clear the notification
                localStorage.removeItem('pendingNotification');
            } catch (e) {
                console.error('Error parsing notification:', e);
                localStorage.removeItem('pendingNotification');
            }
        }
    }
    
    // Check for pending notifications on page load
    checkPendingNotifications();
    
    // Listen for immediate notification requests (same-page)
    window.addEventListener('showPendingNotification', checkPendingNotifications);

    // ================================
    // DARK THEME TOGGLE FUNCTIONALITY
    // ================================
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const htmlElement = document.documentElement;

    // Function to set theme
    function setTheme(theme) {
        htmlElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        updateIcon(theme);
    }

    // Function to update icon based on theme
    function updateIcon(theme) {
        if (themeIcon) {
            if (theme === 'dark') {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
            } else {
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
            }
        }
    }

    // Check for saved theme preference or system preference
    function getPreferredTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        // Check system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    // Initialize theme on page load
    const currentTheme = getPreferredTheme();
    setTheme(currentTheme);

    // Toggle theme on button click
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    }

    // Listen for system theme changes
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            // Only change if user hasn't set a preference
            if (!localStorage.getItem('theme')) {
                setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    // ================================
    // CODE BLOCK COPY FUNCTIONALITY
    // ================================
    function initCodeBlocks() {
        const codeBlocks = document.querySelectorAll('pre');
        
        codeBlocks.forEach((pre) => {
            if (pre.parentElement.classList.contains('code-block-wrapper')) {
                return;
            }

            const wrapper = document.createElement('div');
            wrapper.className = 'code-block-wrapper';
            pre.parentNode.insertBefore(wrapper, pre);
            wrapper.appendChild(pre);
            
            const copyBtn = document.createElement('button');
            copyBtn.className = 'code-copy-btn';
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
            copyBtn.setAttribute('aria-label', 'Copy code to clipboard');
            wrapper.insertBefore(copyBtn, pre);
            
            copyBtn.addEventListener('click', async () => {
                const code = pre.querySelector('code') ? pre.querySelector('code').textContent : pre.textContent;
                
                try {
                    await navigator.clipboard.writeText(code);
                    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    copyBtn.classList.add('copied');
                    setTimeout(() => {
                        copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
                        copyBtn.classList.remove('copied');
                    }, 2000);
                } catch (err) {
                    const textArea = document.createElement('textarea');
                    textArea.value = code;
                    textArea.style.position = 'fixed';
                    textArea.style.left = '-9999px';
                    document.body.appendChild(textArea);
                    textArea.select();
                    try {
                        document.execCommand('copy');
                        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                        copyBtn.classList.add('copied');
                        setTimeout(() => {
                            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
                            copyBtn.classList.remove('copied');
                        }, 2000);
                    } catch (e) {
                        copyBtn.innerHTML = '<i class="fas fa-times"></i> Failed';
                        setTimeout(() => {
                            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
                        }, 2000);
                    }
                    document.body.removeChild(textArea);
                }
            });
        });
    }
    
    initCodeBlocks();

    // ================================
    // VISUAL IMPROVEMENTS
    // ================================

    // 3. Reading Progress Bar
    const progressBar = document.getElementById('readingProgress');
    if (progressBar) {
        window.addEventListener('scroll', () => {
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight - windowHeight;
            const scrolled = window.scrollY;
            const progress = (scrolled / documentHeight) * 100;
            progressBar.style.width = Math.min(progress, 100) + '%';
        });
    }

    // 4. Back to Top Button
    const backToTopBtn = document.getElementById('backToTop');
    if (backToTopBtn) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });

        // Scroll to top on click
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // 5. Image Lazy Loading
    function initLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.addEventListener('load', () => {
                            img.classList.add('loaded');
                            img.classList.remove('img-placeholder');
                        });
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.01
            });

            images.forEach(img => {
                img.classList.add('img-placeholder');
                imageObserver.observe(img);
            });
        } else {
            // Fallback for older browsers
            images.forEach(img => {
                img.src = img.dataset.src;
                img.classList.add('loaded');
            });
        }
    }

    initLazyLoading();

    // ================================
    // SHARE BUTTONS - COPY LINK
    // ================================
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    if (copyLinkBtn) {
        copyLinkBtn.addEventListener('click', async () => {
            const url = window.location.href;
            
            try {
                await navigator.clipboard.writeText(url);
                copyLinkBtn.innerHTML = '<i class="fas fa-check"></i>';
                copyLinkBtn.classList.add('copied');
                
                setTimeout(() => {
                    copyLinkBtn.innerHTML = '<i class="fas fa-link"></i>';
                    copyLinkBtn.classList.remove('copied');
                }, 2000);
            } catch (err) {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = url;
                textArea.style.position = 'fixed';
                textArea.style.left = '-9999px';
                document.body.appendChild(textArea);
                textArea.select();
                try {
                    document.execCommand('copy');
                    copyLinkBtn.innerHTML = '<i class="fas fa-check"></i>';
                    copyLinkBtn.classList.add('copied');
                    setTimeout(() => {
                        copyLinkBtn.innerHTML = '<i class="fas fa-link"></i>';
                        copyLinkBtn.classList.remove('copied');
                    }, 2000);
                } catch (e) {
                    console.error('Failed to copy link');
                }
                document.body.removeChild(textArea);
            }
        });
    }
})
