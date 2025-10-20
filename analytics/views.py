# analytics/views.py
import os
from django.http import HttpResponse
from .tasks import process_data_analysis
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe # Necesario para mostrar el HTML sin sanitizar

# Nota: csrf_exempt es solo para pruebas rápidas. En producción, usa {% csrf_token %} y render.
@csrf_exempt 
def upload_file_view(request):
    # Lógica que se ejecuta cuando el usuario SUBE el archivo
    if request.method == 'POST':
        uploaded_file = request.FILES.get('data_file')
        user_email = request.POST.get('email')
        
        # 1. Guardar archivo temporalmente
        # (Usamos os.urandom(8).hex() para generar un nombre único)
        temp_file_path = f"D:\\Temp\\{uploaded_file.name}_{os.urandom(8).hex()}"
        
        # NOTA: Asegúrate de que el directorio C:\Temp existe en tu Windows, o cámbialo a algo como "/tmp/"
        # Para evitar problemas de permisos, a veces es mejor guardarlo temporalmente en el mismo directorio del proyecto.
        # Por simplicidad, usemos el directorio actual para guardar el archivo temporal.
        temp_file_path = uploaded_file.name 
        with open(temp_file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # 2. DELEGAR la tarea pesada a Celery (INSTANTÁNEO)
        task = process_data_analysis.delay(user_email, temp_file_path)
        
        # 3. Respuesta INMEDIATA al usuario (código 202: Aceptado)
        return HttpResponse(f"""
            <h1>Análisis Solicitado</h1>
            <p>Tu archivo ha sido aceptado y el análisis ha comenzado.</p>
            <p><strong>ID de Tarea:</strong> {task.id}</p>
            <p>Recibirás un correo electrónico cuando el proceso de 15 segundos finalice.</p>
        """, status=202)

    # Lógica que se ejecuta cuando el usuario SOLICITA el formulario (método GET)
    html_form = """
        <h1>Subir Archivo para Análisis Masivo</h1>
        <form method="post" enctype="multipart/form-data">
            <label for="email">Email de Notificación:</label>
            <input type="email" name="email" required><br><br>
            <label for="data_file">Archivo CSV (10,000 filas):</label>
            <input type="file" name="data_file" accept=".csv" required><br><br>
            <button type="submit">Iniciar Análisis Asíncrono</button>
        </form>
    """
    return HttpResponse(mark_safe(html_form))