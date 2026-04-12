// ========================================
// Roommate Dekho - Main JavaScript
// Professional UI Interactions
//=========================================

// Dark Mode Toggle
function initDarkMode() {
    const darkModeToggle = document.querySelector('.dark-mode-toggle');
    const body = document.body;

    // Check for saved preference
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode === 'enabled') {
        body.classList.add('dark-mode');
    }

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');

            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('darkMode', 'enabled');
            } else {
                localStorage.setItem('darkMode', 'disabled');
            }
        });
    }
}

// Smooth Scroll for Anchor Links
function initSmoothScroll() {
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
}

// Multi-Step Form Handler
class MultiStepForm {
    constructor(formElement) {
        this.form = formElement;
        this.steps = Array.from(formElement.querySelectorAll('.form-step'));
        this.currentStep = 0;
        this.progressSteps = Array.from(document.querySelectorAll('.progress-step'));

        this.init();
    }

    init() {
        this.showStep(0);
        this.attachEventListeners();
    }

    attachEventListeners() {
        // Next buttons
        this.form.querySelectorAll('.btn-next').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                if (this.validateStep(this.currentStep)) {
                    this.nextStep();
                }
            });
        });

        // Previous buttons
        this.form.querySelectorAll('.btn-prev').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.prevStep();
            });
        });
    }

    showStep(n) {
        this.steps.forEach((step, index) => {
            step.style.display = index === n ? 'block' : 'none';
        });

        // Update progress indicators
        this.progressSteps.forEach((step, index) => {
            if (index < n) {
                step.classList.add('complete');
                step.classList.remove('active');
            } else if (index === n) {
                step.classList.add('active');
                step.classList.remove('complete');
            } else {
                step.classList.remove('active', 'complete');
            }
        });

        // Resize map if on location step (step 5, index 4)
        if (n === 4 && map) {
            setTimeout(() => {
                map.invalidateSize();
            }, 100);
        }
    }

    nextStep() {
        if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
            this.showStep(this.currentStep);
            this.scrollToTop();
        }
    }

    prevStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.showStep(this.currentStep);
            this.scrollToTop();
        }
    }

    validateStep(stepIndex) {
        const currentStepElement = this.steps[stepIndex];
        const inputs = currentStepElement.querySelectorAll('input[required], select[required], textarea[required]');

        let isValid = true;
        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('error');

                // Show error message
                let errorMsg = input.parentElement.querySelector('.form-error');
                if (!errorMsg) {
                    errorMsg = document.createElement('div');
                    errorMsg.className = 'form-error';
                    errorMsg.textContent = 'This field is required';
                    input.parentElement.appendChild(errorMsg);
                }
            } else {
                input.classList.remove('error');
                const errorMsg = input.parentElement.querySelector('.form-error');
                if (errorMsg) errorMsg.remove();
            }
        });

        return isValid;
    }

    scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Filter and Sort for Results Page
class ResultsFilter {
    constructor() {
        this.results = Array.from(document.querySelectorAll('.match-card'));
        this.originalOrder = [...this.results];
        this.init();
    }

    init() {
        // Sort functionality
        const sortSelect = document.querySelector('#sort-select');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.sortResults(e.target.value);
            });
        }

        // Budget filter
        const budgetSlider = document.querySelector('#budget-filter');
        if (budgetSlider) {
            budgetSlider.addEventListener('input', (e) => {
                this.filterByBudget(parseInt(e.target.value));
            });
        }

        // Distance filter
        const distanceSlider = document.querySelector('#distance-filter');
        if (distanceSlider) {
            distanceSlider.addEventListener('input', (e) => {
                this.filterByDistance(parseFloat(e.target.value));
            });
        }
    }

    sortResults(sortBy) {
        const container = document.querySelector('.results-grid');
        if (!container) return;

        let sortedResults = [...this.results];

        switch (sortBy) {
            case 'best-match':
                sortedResults.sort((a, b) => {
                    const matchA = parseInt(a.dataset.compatibility);
                    const matchB = parseInt(b.dataset.compatibility);
                    return matchB - matchA;
                });
                break;

            case 'nearest':
                sortedResults.sort((a, b) => {
                    const distA = parseFloat(a.dataset.distance);
                    const distB = parseFloat(b.dataset.distance);
                    return distA - distB;
                });
                break;

            case 'budget':
                sortedResults.sort((a, b) => {
                    const budgetA = parseInt(a.dataset.budget);
                    const budgetB = parseInt(b.dataset.budget);
                    return budgetA - budgetB;
                });
                break;

            default:
                sortedResults = this.originalOrder;
        }

        // Re-append in new order
        container.innerHTML = '';
        sortedResults.forEach(result => container.appendChild(result));
    }

    filterByBudget(maxBudget) {
        this.results.forEach(card => {
            const budget = parseInt(card.dataset.budget);
            card.style.display = budget <= maxBudget ? 'block' : 'none';
        });
    }

    filterByDistance(maxDistance) {
        this.results.forEach(card => {
            const distance = parseFloat(card.dataset.distance);
            card.style.display = distance <= maxDistance ? 'block' : 'none';
        });
    }
}

// Image Upload Preview
function initImageUpload() {
    const imageInput = document.querySelector('input[type="file"][name="image"]');
    if (imageInput) {
        imageInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    // Create or update preview
                    let preview = document.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('div');
                        preview.className = 'image-preview';
                        imageInput.parentElement.appendChild(preview);
                    }

                    preview.innerHTML = `<img src="${event.target.result}" alt="Preview" style="width: 150px; height: 150px; object-fit: cover; border-radius: 12px; margin-top: 12px;">`;
                };
                reader.readAsDataURL(file);
            }
        });
    }
}

// Fade-in animation on scroll
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Compatibility Percentage Circle Animation
function animateCompatibilityCircle() {
    const circles = document.querySelectorAll('.compatibility-circle');

    circles.forEach(circle => {
        const percentage = parseInt(circle.dataset.percentage);
        const circumference = 2 * Math.PI * 45; // radius = 45
        const offset = circumference - (percentage / 100) * circumference;

        const progressCircle = circle.querySelector('.progress');
        if (progressCircle) {
            progressCircle.style.strokeDasharray = `${circumference} ${circumference}`;
            progressCircle.style.strokeDashoffset = circumference;

            setTimeout(() => {
                progressCircle.style.strokeDashoffset = offset;
            }, 100);
        }
    });
}

// Shortlist functionality
function initShortlist() {
    const shortlistBtns = document.querySelectorAll('.btn-shortlist');

    shortlistBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const userId = this.dataset.userId;

            // Toggle shortlist
            this.classList.toggle('active');

            // Save to localStorage
            let shortlisted = JSON.parse(localStorage.getItem('shortlisted') || '[]');

            if (this.classList.contains('active')) {
                if (!shortlisted.includes(userId)) {
                    shortlisted.push(userId);
                }
                this.innerHTML = '<svg>...</svg> Shortlisted';
            } else {
                shortlisted = shortlisted.filter(id => id !== userId);
                this.innerHTML = '<svg>...</svg> Shortlist';
            }

            localStorage.setItem('shortlisted', JSON.stringify(shortlisted));
        });
    });
}

// Hobby Tags Input
function initHobbyTags() {
    const hobbiesInput = document.querySelector('#hobbies-input');
    const tagsContainer = document.querySelector('#tag-container');

    if (hobbiesInput && tagsContainer) {
        const tags = [];

        hobbiesInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                const value = this.value.trim();

                if (value && !tags.includes(value)) {
                    tags.push(value);
                    addTag(value);
                    this.value = '';
                }
            }
        });

        function addTag(text) {
            const tag = document.createElement('span');
            tag.className = 'badge badge-primary';
            tag.innerHTML = `
        ${text}
        <button type="button" class="tag-remove" onclick="this.parentElement.remove()">×</button>
      `;
            tagsContainer.appendChild(tag);

            // Update hidden input
            updateHiddenInput();
        }

        function updateHiddenInput() {
            const hiddenInput = document.querySelector('#Hobbies');
            if (hiddenInput) {
                hiddenInput.value = tags.join(',');
                // Trigger change event for validation check
                const event = new Event('change');
                hiddenInput.dispatchEvent(event);
            }
        }
    }
}

// Map Initialization
let map;
let marker;

function initMap() {
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    // Default to Bhopal (User Requested)
    const defaultLat = 23.2599;
    const defaultLng = 77.4126;

    map = L.map('map').setView([defaultLat, defaultLng], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Click to pin
    map.on('click', function (e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;

        if (marker) {
            marker.setLatLng([lat, lng]);
        } else {
            marker = L.marker([lat, lng]).addTo(map);
        }

        // Update hidden inputs
        document.getElementById('latitude').value = lat;
        document.getElementById('longitude').value = lng;
    });
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initDarkMode();
    initSmoothScroll();
    initImageUpload();
    initScrollAnimations();
    animateCompatibilityCircle();
    initShortlist();
    initHobbyTags();
    initMap(); // Init map

    // Initialize multi-step form if present
    const multiStepForm = document.querySelector('.multi-step-form');
    if (multiStepForm) {
        new MultiStepForm(multiStepForm);
    }
    // ...

    // Initialize results filter if present
    const resultsGrid = document.querySelector('.results-grid');
    if (resultsGrid) {
        new ResultsFilter();
    }
});
