import time
import pandas as pd
from celery import shared_task
from django.core.mail import send_mail

@shared_task(bind=True, max_retries=3)
def process_data_analysis(self, user_email, file_path):
    """
    Realiza un análisis simple de un archivo CSV usando Pandas.
    """
    try:
        # 1. Leer el archivo con Pandas
        data = pd.read_csv(file_path)
        
        # Simulación de un cálculo pesado (el tiempo de espera)
        # time.sleep(15) 
        
        # 2. ANÁLISIS REAL: contar registros y calcular el promedio de la columna 'value_column'
        total_rows = len(data)
        
        # Esta columna ('value_column') es la que estamos promediando
        average_value = data['value_column'].mean() 
        
        # 3. Calcular la región con más ventas (un análisis más complejo)
        top_region = data.groupby('region')['value_column'].sum().idxmax()
        
        # 4. Preparar el resultado y enviarlo por correo
        subject = f"✅ Análisis de Datos Completado: {total_rows} registros"
        message = (
            f"Hola,\n\n"
            f"Tu análisis de datos se completó con éxito:\n"
            f"- Total de Registros Procesados: {total_rows}\n"
            f"- Valor Promedio de Transacción: ${average_value:.2f}\n"
            f"- Región con Mayor Ingreso Total: {top_region}"
        )
        
        send_mail(subject, message, 'notifications@example.com', [user_email])
        
        return "Análisis y correo enviados"

    except Exception as exc:
        # Permite que la tarea se reintente si hay un error transitorio.
        raise self.retry(exc=exc, countdown=60)