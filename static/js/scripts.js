// ============================================
// StreamPoint - Scripts principales
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================
    // Auto-hide alerts después de 5 segundos
    // ============================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // ============================================
    // Smooth scroll para enlaces internos
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ============================================
    // Confirmación antes de eliminar/cancelar
    // ============================================
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // ============================================
    // Formateo de precios en tiempo real
    // ============================================
    const priceElements = document.querySelectorAll('.price-format');
    priceElements.forEach(element => {
        const price = parseFloat(element.textContent);
        if (!isNaN(price)) {
            element.textContent = new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP',
                minimumFractionDigits: 0
            }).format(price);
        }
    });

    // ============================================
    // Tooltips de Bootstrap
    // ============================================
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ============================================
    // Validación de formularios
    // ============================================
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // ============================================
    // Toggle de visibilidad de contraseña
    // ============================================
    const passwordToggles = document.querySelectorAll('.toggle-password');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = document.querySelector(this.getAttribute('data-target'));
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });

    // ============================================
    // Animación de contador para estadísticas
    // ============================================
    const animateCounter = (element, target, duration = 1000) => {
        let current = 0;
        const increment = target / (duration / 16);
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = Math.floor(target);
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    };

    const counters = document.querySelectorAll('.counter-animate');
    const observerOptions = {
        threshold: 0.5
    };

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                animateCounter(entry.target, target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    counters.forEach(counter => counterObserver.observe(counter));

    // ============================================
    // Filtro de búsqueda en tiempo real
    // ============================================
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const filter = this.value.toLowerCase();
            const items = document.querySelectorAll('.searchable-item');
            
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(filter)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // ============================================
    // Loading spinner para formularios
    // ============================================
    const submitButtons = document.querySelectorAll('[data-loading]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                this.disabled = true;
                const originalText = this.innerHTML;
                this.innerHTML = '<span class="loading"></span> Procesando...';
                
                // Restaurar después de 5 segundos (timeout de seguridad)
                setTimeout(() => {
                    this.disabled = false;
                    this.innerHTML = originalText;
                }, 5000);
            }
        });
    });

    // ============================================
    // Cálculo de puntos en tiempo real
    // ============================================
    const calculatePoints = (price, isFirstPurchase = false) => {
        // Configuración: 10 puntos = $1 COP
        const pointsPerPeso = 10;
        const firstPurchaseMultiplier = 1.5;
        
        let points = Math.floor(price / pointsPerPeso);
        if (isFirstPurchase) {
            points = Math.floor(points * firstPurchaseMultiplier);
        }
        
        return points;
    };

    // Mostrar puntos estimados en planes
    const planPrices = document.querySelectorAll('[data-plan-price]');
    planPrices.forEach(element => {
        const price = parseFloat(element.getAttribute('data-plan-price'));
        const isFirst = element.hasAttribute('data-first-purchase');
        const points = calculatePoints(price, isFirst);
        
        const pointsBadge = element.querySelector('.points-estimate');
        if (pointsBadge) {
            pointsBadge.textContent = `+${points} puntos`;
        }
    });

    // ============================================
    // Actualización de fecha de vencimiento
    // ============================================
    const updateExpirationDate = (startDate, duration) => {
        const durationMap = {
            'mensual': 30,
            'trimestral': 90,
            'semestral': 180,
            'anual': 365
        };
        
        const days = durationMap[duration] || 30;
        const expDate = new Date(startDate);
        expDate.setDate(expDate.getDate() + days);
        
        return expDate.toLocaleDateString('es-CO');
    };

    // ============================================
    // Copiar al portapapeles
    // ============================================
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const text = this.getAttribute('data-copy');
            navigator.clipboard.writeText(text).then(() => {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Copiado';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            });
        });
    });

    // ============================================
    // Prevenir doble clic en formularios
    // ============================================
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                setTimeout(() => {
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    });

    // ============================================
    // Actualizar contador de días restantes
    // ============================================
    const updateDaysRemaining = () => {
        const expirationElements = document.querySelectorAll('[data-expiration-date]');
        
        expirationElements.forEach(element => {
            const expDate = new Date(element.getAttribute('data-expiration-date'));
            const today = new Date();
            const diffTime = expDate - today;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            
            const badge = element.querySelector('.days-remaining');
            if (badge) {
                if (diffDays < 0) {
                    badge.textContent = 'Vencida';
                    badge.className = 'badge bg-danger days-remaining';
                } else if (diffDays <= 7) {
                    badge.textContent = `${diffDays} días`;
                    badge.className = 'badge bg-warning days-remaining';
                } else {
                    badge.textContent = `${diffDays} días`;
                    badge.className = 'badge bg-success days-remaining';
                }
            }
        });
    };

    // Actualizar al cargar y cada minuto
    updateDaysRemaining();
    setInterval(updateDaysRemaining, 60000);

    // ============================================
    // Animación de entrada para cards
    // ============================================
    const cards = document.querySelectorAll('.card-custom, .service-card');
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    entry.target.style.transition = 'all 0.5s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                cardObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => cardObserver.observe(card));

});

// ============================================
// Funciones globales útiles
// ============================================

// Formatear número como moneda
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
}

// Mostrar notificación toast
function showNotification(message, type = 'success') {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.getElementById('toastContainer').appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Confirmar acción
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

console.log('StreamPoint JS cargado correctamente ✓');