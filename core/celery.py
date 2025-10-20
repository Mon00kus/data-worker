""" import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') """

import os
from celery import Celery

# 3.1. Establece la configuración de Django (usa el nombre 'core')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 3.2. Crea la instancia de la aplicación Celery
app = Celery('core')

# 3.3. Carga la configuración de Celery desde settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# 3.4. Descubre tareas automáticamente en todas las apps registradas
app.autodiscover_tasks()