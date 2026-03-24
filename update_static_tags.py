import re
import sys

filepath = 'templates/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add {% load static %} at the very top
if '{% load static %}' not in content:
    content = '{% load static %}\n' + content

# Regex replacements for href and src
content = re.sub(r'href="style\.css"', r'href="{% static \'style.css\' %}"', content)
content = re.sub(r'href="(css/[^"]+)"', r'href="{% static \'\1\' %}"', content)
content = re.sub(r'src="(js/[^"]+)"', r'src="{% static \'\1\' %}"', content)
content = re.sub(r'src="(img/[^"]+)"', r'src="{% static \'\1\' %}"', content)
content = re.sub(r'href="(assets/[^"]+)"', r'href="{% static \'\1\' %}"', content)
content = re.sub(r'src="(assets/[^"]+)"', r'src="{% static \'\1\' %}"', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html to use Django static tags.")
