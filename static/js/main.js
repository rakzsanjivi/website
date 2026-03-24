// Update Copyright Year
document.getElementById('year').textContent = new Date().getFullYear();

// Adaptive Colors using ColorThief (From Profile Image)
function initSceneWithAdaptiveColors() {
    const img = document.getElementById('profile-image');
    let primaryColor = '#00C9A7';
    let secondaryColor = '#F5A623';
    
    try {
        const colorThief = new ColorThief();
        if (img.complete) {
            extractColors(img, colorThief);
        } else {
            img.addEventListener('load', function() {
                extractColors(img, colorThief);
            });
        }
    } catch(e) {
        console.warn("ColorThief not loaded.", e);
        initParticles(primaryColor, secondaryColor);
    }

    function extractColors(image, thief) {
        try {
            const dominant = thief.getColor(image);
            const palette = thief.getPalette(image, 3);
            if (dominant && palette) {
                primaryColor = `rgb(${dominant[0]}, ${dominant[1]}, ${dominant[2]})`;
                secondaryColor = `rgb(${palette[1][0]}, ${palette[1][1]}, ${palette[1][2]})`;
                
                document.documentElement.style.setProperty('--primary', primaryColor);
                document.documentElement.style.setProperty('--secondary', secondaryColor);

                const rgbToHex = (r, g, b) => '#' + [r, g, b].map(x => {
                    const hex = x.toString(16);
                    return hex.length === 1 ? '0' + hex : hex;
                }).join('');
                
                primaryColor = rgbToHex(dominant[0], dominant[1], dominant[2]);
                secondaryColor = rgbToHex(palette[1][0], palette[1][1], palette[1][2]);
            }
        } catch(e) {
            console.warn("CORS error: couldn't extract colors from local file image natively without local server. Using defaults.", e);
        }
        initParticles(primaryColor, secondaryColor);
    }
}
initSceneWithAdaptiveColors();

// Navbar Scroll Effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Typewriter Effect
const phrases = ["Aspiring Data Analyst", "MCA Student", "Python Developer"];
let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;
const typewriterElement = document.getElementById("typewriter-text");

function type() {
    const currentPhrase = phrases[phraseIndex];
    
    if (isDeleting) {
        typewriterElement.textContent = currentPhrase.substring(0, charIndex - 1);
        charIndex--;
    } else {
        typewriterElement.textContent = currentPhrase.substring(0, charIndex + 1);
        charIndex++;
    }

    let typeSpeed = isDeleting ? 50 : 100;

    if (!isDeleting && charIndex === currentPhrase.length) {
        typeSpeed = 2000; // Pause at end of phrase
        isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        phraseIndex = (phraseIndex + 1) % phrases.length;
        typeSpeed = 500; // Pause before typing new phrase
    }

    setTimeout(type, typeSpeed);
}

// Start Typewriter
setTimeout(type, 1000);

// Fade In on Scroll Observer
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.15
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('appear');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// Interactive PNG Hover Parallax Effect (for any remaining interactives)
document.addEventListener('mousemove', function(e) {
    const interactives = document.querySelectorAll('.interactive-png');
    const xAxis = (window.innerWidth / 2 - e.pageX) / 25;
    const yAxis = (window.innerHeight / 2 - e.pageY) / 25;

    interactives.forEach(img => {
        img.style.transform = `translateY(${yAxis}px) translateX(${xAxis}px)`;
    });
});



// Initialize particles.js with adaptive colors
function initParticles(c1, c2) {
    if (typeof particlesJS !== 'undefined') {
        particlesJS("particles-js", {
            "particles": {
                "number": {
                    "value": 60,
                    "density": {
                        "enable": true,
                        "value_area": 800
                    }
                },
                "color": {
                    "value": [c1, c2, "#ffffff"]
                },
                "shape": {
                    "type": "circle",
                },
                "opacity": {
                    "value": 0.5,
                    "random": true,
                    "anim": {
                        "enable": true,
                        "speed": 1,
                        "opacity_min": 0.1,
                        "sync": false
                    }
                },
                "size": {
                    "value": 3,
                    "random": true,
                    "anim": {
                        "enable": false
                    }
                },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": c1,
                    "opacity": 0.2,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 1.5,
                    "direction": "none",
                    "random": true,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": {
                        "enable": true,
                        "mode": "grab"
                    },
                    "onclick": {
                        "enable": true,
                        "mode": "push"
                    },
                    "resize": true
                },
                "modes": {
                    "grab": {
                        "distance": 140,
                        "line_linked": {
                            "opacity": 0.5
                        }
                    },
                    "push": {
                        "particles_nb": 3
                    }
                }
            },
            "retina_detect": true
        });
    }
}

// Hamburger Menu Toggle
const hamburger = document.getElementById('hamburger');
if (hamburger) {
    hamburger.addEventListener('click', () => {
        document.querySelector('.nav-links').classList.toggle('open');
    });
}
