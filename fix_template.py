with open('Light/templates/waste_history.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix literal `n back to actual newlines
content = content.replace('`n', '\n')

# Now fix any remaining template tag issues
import re
content = re.sub(
    r"{% extends 'base\.html' %}\s*{% block title %}Waste History - TRASH2CASH{% endblock[\r\n\s]*%}\s*{% block extra_css %}",
    "{% extends 'base.html' %}\n\n{% block title %}Waste History - TRASH2CASH{% endblock %}\n\n{% block extra_css %}",
    content,
    flags=re.MULTILINE
)

content = re.sub(
    r"{% endblock %}\s*{% block content %}",
    "{% endblock %}\n\n{% block content %}",
    content
)

with open('Light/templates/waste_history.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Template fixed successfully!")
