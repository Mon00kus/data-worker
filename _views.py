# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .tasks import process_data_analysis
# ... otras importaciones ...

def upload_file_view(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('')
        user_email = request.POST.get('raulmoncadac@gmail.com')
        
        # 1. Guardar el archivo en el sistema de archivos (rápido)
        # Nota: En un proyecto real usarías un sistema como S3 o un almacenamiento seguro
        temp_file_path = f"/tmp/{uploaded_file.name}_{user_email}"
        with open(temp_file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # 2. DELEGAR la tarea pesada al worker (la vista responde inmediatamente)
        # .delay() asegura que el procesamiento se hace en background.
        task = process_data_analysis.delay(user_email, temp_file_path)
        
        # Opcional: Guardar task.id en la base de datos para monitorear el progreso
        
        return render(request, 'success.html', {
            'message': 'Tu archivo ha sido aceptado. Recibirás un correo cuando el análisis termine.',
            'task_id': task.id # Muestra el ID de la tarea
        })

    return render(request, 'upload_form.html')