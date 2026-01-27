web: /opt/venv/bin/python manage.py migrate && /opt/venv/bin/gunicorn Traffic.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-file - --access-logfile - --error-logfile -
