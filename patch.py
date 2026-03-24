import re
import os

# --- PATCH STYLE.CSS ---
css_path = 'style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace :root
css = css.replace(
    '--card-radius: 16px;\n}',
    '--card-radius: 16px;\n    --accent: #4F8EF7;\n    --accent-glow: rgba(79, 142, 247, 0.15);\n}'
)

# Replace .logo
css = css.replace(
    '.logo {\n    font-size: 24px;\n    font-weight: 700;\n    color: var(--primary);\n    text-decoration: none;\n    letter-spacing: 1px;\n}',
    '.logo {\n    font-size: clamp(14px, 2vw, 20px);\n    font-weight: 700;\n    color: var(--primary);\n    text-decoration: none;\n    letter-spacing: 1px;\n    white-space: nowrap;\n    overflow: hidden;\n    text-overflow: ellipsis;\n    max-width: 220px;\n}'
)

# Replace .section-title span
css = css.replace(
    'color: var(--text-main);\n    -webkit-text-stroke: 0;',
    'color: var(--accent);\n    -webkit-text-stroke: 0;'
)

# Replace #hero padding
css = css.replace(
    '#hero {\n    position: relative;\n    min-height: 100vh;\n    padding: 140px 5%;',
    '#hero {\n    position: relative;\n    min-height: 100vh;\n    padding: 160px 5% 140px;'
)

# Replace .hero-title
css = css.replace(
    'font-size: 80px;\n    font-weight: 800;\n    letter-spacing: -3px;',
    'font-size: clamp(36px, 7vw, 80px);\n    font-weight: 800;\n    letter-spacing: clamp(-1px, -0.03em, -3px);'
)

# Replace .hero-subtitle
css = css.replace(
    '.hero-subtitle {\n    font-size: 24px;',
    '.hero-subtitle {\n    font-size: clamp(16px, 2.5vw, 24px);'
)

# Replace .typewriter border
css = css.replace(
    'border-right: 2px solid var(--text-muted);',
    'border-right: 2px solid var(--accent);'
)
css = css.replace(
    '50% { border-color: var(--text-muted) }',
    '50% { border-color: var(--accent) }'
)

# Replace .social-icon hover border
css = css.replace(
    'border-color: rgba(255, 255, 255, 0.2);',
    'border-color: var(--accent);'
)

# Replace .role-map
css = css.replace(
    'padding-bottom: 20px;\n    scrollbar-width: none;',
    'padding-bottom: 60px;\n    scrollbar-width: none;'
)

# Replace .role-card
css = css.replace(
    '.role-card {\n    padding: 15px 25px;',
    '.role-card {\n    flex: 1 1 0;\n    min-width: 130px;\n    max-width: 180px;\n    text-align: center;\n    justify-content: center;\n    padding: 15px 25px;'
)

# Replace .role-node
css = css.replace(
    'height: 2px;\n    width: 30px;',
    'height: 2px;\n    width: 40px;'
)

# Replace .project-title and hover
css = css.replace(
    '.project-title {\n    font-size: 22px;\n    font-weight: 600;\n    margin-bottom: 15px;\n}',
    '.project-title {\n    font-size: 20px;\n    font-weight: 600;\n    margin-bottom: 15px;\n    transition: color 0.3s ease;\n}\n\n.project-card:hover .project-title {\n    color: var(--accent);\n}'
)

# Replace .project-desc
css = css.replace(
    '.project-desc {\n    color: var(--text-muted);\n    font-size: 15px;\n    line-height: 1.6;',
    '.project-desc {\n    color: var(--text-muted);\n    font-size: 14px;\n    line-height: 1.7;'
)

# Replace .timeline-date background
css = css.replace(
    'background-color: var(--primary);\n    font-size: 12px;\n    font-weight: 700;\n    text-transform: uppercase;',
    'background-color: var(--accent);\n    font-size: 12px;\n    font-weight: 700;\n    text-transform: uppercase;'
)

# Replace .social-link hover
css = css.replace(
    'background: var(--primary);\n    color: var(--bg-color);\n    transform: translateY(-5px);\n    box-shadow: 0 5px 15px rgba(0, 201, 167, 0.4);',
    'background: var(--accent);\n    color: var(--bg-color);\n    transform: translateY(-5px);\n    box-shadow: 0 5px 15px var(--accent-glow);'
)

new_skills_css = """/* =========================================
   ADDED SKILLS CSS
========================================= */
.skills-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    max-width: 900px;
    margin: 0 auto;
}

.skill-card {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 16px;
    padding: 24px 28px;
    border-radius: 12px;
    transition: all 0.3s ease;
}

.skill-card i {
    font-size: 28px;
    color: var(--accent);
    width: 36px;
    text-align: center;
}

.skill-card span {
    font-size: 15px;
    font-weight: 500;
    color: var(--text-main);
}

.skill-card.glass-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 20px var(--accent-glow);
}

/* =========================================
   NEW COMPONENT & MOBILE MENU CSS
========================================= */
.btn-primary {
    background: var(--accent);
    color: #ffffff;
    padding: 14px 32px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 15px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 0 20px var(--accent-glow);
}
.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(79,142,247,0.35);
}
.btn-outline {
    border: 1px solid var(--accent);
    color: var(--accent);
    background: transparent;
    padding: 12px 28px;
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.3s ease;
    display: inline-block;
}
.btn-outline:hover {
    background: var(--accent);
    color: #fff;
    box-shadow: 0 4px 15px var(--accent-glow);
}

/* Hamburger Menu */
.hamburger {
    display: none;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    padding: 5px;
    background: transparent;
    border: none;
}
.hamburger span {
    width: 24px;
    height: 2px;
    background: var(--text-main);
    border-radius: 2px;
    transition: all 0.3s ease;
}
@media (max-width: 768px) {
    .hamburger { display: flex; }
    .nav-links {
        display: none;
        position: absolute;
        top: 70px;
        left: 0;
        right: 0;
        background: rgba(10,10,10,0.97);
        flex-direction: column;
        padding: 20px;
        gap: 20px;
        border-bottom: 1px solid var(--card-border);
    }
    .nav-links.open { display: flex; }
    
    .skills-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
@media (max-width: 480px) {
    .skills-grid {
        grid-template-columns: 1fr;
    }
}
"""

css = re.sub(r'/\* =========================================\n   ADDED SKILLS CSS.*', new_skills_css, css, flags=re.DOTALL)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# --- PATCH INDEX.HTML ---
html_path = 'index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add hamburger toggle
html = html.replace(
    '<a href="#hero" class="logo">RAGHAVARAJAN S U.</a>\n        <ul class="nav-links">',
    '<a href="#hero" class="logo">RAGHAVARAJAN S U.</a>\n        <button class="hamburger" id="hamburger" aria-label="Toggle Menu">\n            <span></span><span></span><span></span>\n        </button>\n        <ul class="nav-links">'
)

# Hero greeting
html = html.replace(
    '<span class="hero-greeting">RAGHAVARAJAN S U\'s</span>',
    '<span class="hero-greeting">Hi, I\'m Raghavarajan</span>'
)

# Replace Skills Section
new_skills_html = """<!-- Skills Section -->
        <section id="skills">
            <h2 class="section-title fade-in"><span>Tech Stack</span></h2>
            <div class="skills-grid fade-in">
                <div class="skill-card glass-card">
                    <i class="fa-brands fa-python"></i>
                    <span>Python</span>
                </div>
                <div class="skill-card glass-card">
                    <i class="fa-solid fa-database"></i>
                    <span>SQL</span>
                </div>
                <div class="skill-card glass-card">
                    <i class="fa-solid fa-table"></i>
                    <span>Excel</span>
                </div>
                <div class="skill-card glass-card">
                    <i class="fa-solid fa-chart-pie"></i>
                    <span>Power BI</span>
                </div>
                <div class="skill-card glass-card">
                    <i class="fa-solid fa-magnifying-glass-chart"></i>
                    <span>Data Analysis</span>
                </div>

                <div class="skill-card glass-card">
                    <i class="fa-solid fa-chart-line"></i>
                    <span>Statistics</span>
                </div>
                <div class="skill-card glass-card">
                    <i class="fa-solid fa-file-csv"></i>
                    <span>Pandas</span>
                </div>

            </div>
        </section>"""

html = re.sub(r'<!-- Skills Section -->.*?</section>', new_skills_html, html, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

# --- PATCH MAIN.JS ---
js_path = 'js/main.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

hamburger_js = """
// Hamburger Menu Toggle
const hamburger = document.getElementById('hamburger');
if (hamburger) {
    hamburger.addEventListener('click', () => {
        document.querySelector('.nav-links').classList.toggle('open');
    });
}
"""
if "Hamburger Menu Toggle" not in js:
    with open(js_path, 'a', encoding='utf-8') as f:
        f.write(hamburger_js)

print("Patch applied successfully")
