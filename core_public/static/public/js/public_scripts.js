// ============================================
// StreamPoint - Scripts para Core Public
// JavaScript específico para templates públicos
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================
    // CATÁLOGO - BÚSQUEDA EN TIEMPO REAL
    // ============================================
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const items = document.querySelectorAll('.searchable-item');
            let visibleCount = 0;

            items.forEach(function(item) {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.style.display = '';
                    item.classList.remove('hidden');
                    visibleCount++;
                } else {
                    item.style.display = 'none';
                    item.classList.add('hidden');
                }
            });

            // Mostrar mensaje si no hay resultados
            const noResultsMessage = document.getElementById('noResultsMessage');
            if (noResultsMessage) {
                if (visibleCount === 0) {
                    noResultsMessage.style.display = 'block';
                } else {
                    noResultsMessage.style.display = 'none';
                }
            }
        });
    }

    // ============================================
    // DETALLE SERVICIO - ANIMACIONES
    // ============================================
    const serviceCards = document.querySelectorAll('.service-card');
    if (serviceCards.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 100);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });

        serviceCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.5s ease';
            observer.observe(card);
        });
    }

    // ============================================
    // INFORMACIÓN PROYECTO - CONTADORES ANIMADOS
    // ============================================
    const counters = document.querySelectorAll('.counter-animate');
    if (counters.length > 0) {
        const animateCounter = (counter) => {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = 2000; // 2 segundos
            const increment = target / (duration / 16); // 60 fps
            let current = 0;
            
            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    counter.textContent = Math.floor(current).toLocaleString('es-CO');
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target.toLocaleString('es-CO');
                }
            };
            
            updateCounter();
        };
        
        // Observer para iniciar la animación cuando los contadores sean visibles
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        counters.forEach(counter => counterObserver.observe(counter));
    }

    // ============================================
    // SMOOTH SCROLL PARA ENLACES INTERNOS
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ============================================
    // TOOLTIPS PERSONALIZADOS (si Bootstrap está cargado)
    // ============================================
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // ============================================
    // LAZY LOADING PARA IMÁGENES
    // ============================================
    const images = document.querySelectorAll('img[loading="lazy"]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    // ============================================
    // ANIMACIÓN DE FADE-IN PARA ELEMENTOS
    // ============================================
    const fadeElements = document.querySelectorAll('.fade-in-up');
    if (fadeElements.length > 0) {
        const fadeObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    fadeObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        fadeElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s ease-out';
            fadeObserver.observe(el);
        });
    }

    // ============================================
    // MANEJO DE ERRORES DE CARGA DE IMÁGENES
    // ============================================
    const serviceLogo = document.querySelectorAll('.service-logo');
    serviceLogo.forEach(img => {
        img.addEventListener('error', function() {
            this.style.display = 'none';
            const fallback = document.createElement('div');
            fallback.className = 'service-logo d-flex align-items-center justify-content-center';
            fallback.innerHTML = '<i class="fas fa-play-circle" style="font-size: 4rem; color: var(--primary-color);"></i>';
            this.parentElement.appendChild(fallback);
        });
    });

    // ============================================
    // EFECTO PARALLAX SUAVE (OPCIONAL)
    // ============================================
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.parallax');
        
        parallaxElements.forEach(el => {
            const speed = el.dataset.speed || 0.5;
            el.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });

    // ============================================
    // PREVENIR DOBLE ENVÍO DE FORMULARIOS
    // ============================================
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Procesando...';
                
                // Rehabilitar después de 5 segundos por seguridad
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = submitBtn.dataset.originalText || 'Enviar';
                }, 5000);
            }
        });
    });

    // ============================================
    // COPIAR AL PORTAPAPELES (útil para códigos o enlaces)
    // ============================================
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.dataset.target;
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const textToCopy = targetElement.textContent || targetElement.value;
                
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check me-1"></i>¡Copiado!';
                    this.classList.add('btn-success');
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('btn-success');
                    }, 2000);
                });
            }
        });
    });

    console.log('✅ StreamPoint Public Scripts cargados correctamente');
});

// ============================================
// FUNCIÓN AUXILIAR: Formatear moneda COP
// ============================================
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
}

// ============================================
// FUNCIÓN AUXILIAR: Formatear números
// ============================================
function formatNumber(number) {
    return new Intl.NumberFormat('es-CO').format(number);
}

// ============================================
// FUNCIÓN AUXILIAR: Debounce para optimizar búsquedas
// ============================================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
