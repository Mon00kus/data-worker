import time
import pandas as pd
from celery import shared_task
from django.core.mail import send_mail

@shared_task(bind=True)
def process_data_analysis(self, user_email, file_path):
    # 6.1. Definición del trabajo a realizar
    try:
        # Lógica Pesada
        data = pd.read_csv(file_path)
        time.sleep(15)

        # Análisis y Email
        total_rows = len(data)
        average_value = data['value_column'].mean()
        subject = f"✅ Análisis Completado: {total_rows} registros"

        # 6.2. Enviar el correo electrónico
        send_mail(subject, "...", 'notifications@example.com', [user_email])

        return "Análisis finalizado"
    except Exception as exc:
        # 6.3. Manejo de Reintentos
        raise self.retry(exc=exc, countdown=60, max_retries=3)