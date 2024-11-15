import time
from django.shortcuts import render, redirect
from .models import Thread, Message, Visitor 
from django.http import JsonResponse
import json
import os 
from django.conf import settings


from openai import OpenAI


ASSISTANT_ID= os.getenv('ASSIST_ID') 

client = OpenAI(api_key=settings.OPENAI_API_KEY)



def visitor_info(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        print(f"{name}")

        # Verificar si el visitante ya existe
        visitor, created = Visitor.objects.get_or_create(email=email, defaults={'name': name})

        # Guardar el visitor_id en la sesión
        request.session['visitor_id'] = visitor.id
        print(f"{visitor.id}")

        return redirect('chat')

    return render(request, 'chat/visitor_info.html')





def submit_message(client, assistant_id, thread_id, user_message):
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=user_message
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    print(f"{thread_id}, se ha creado el thread")
    return run



def wait_on_run(client, run, thread_id, timeout=30):
    start_time = time.time()
    while run.status in ["queued", "in_progress"]:
        if time.time() - start_time > timeout:
            raise TimeoutError("La solicitud tardó demasiado en completarse.")
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        print(f"{run.id}, se ha creado un run id, desde wait on run")
    if run.status != "succeeded":
        raise Exception(f"El run falló con el estado: {run.status}")
    return run




def chat(request):
    print("se ha inicializado")

    if 'visitor_id' not in request.session:
        print("visitor id ")
        return redirect('visitor_info')

    visitor = Visitor.objects.get(id=request.session['visitor_id'])

    # Verificar si el thread_id está en la sesión
    if 'thread_id' not in request.session:
        # Crear un nuevo hilo utilizando la API de OpenAI
        openai_thread = client.beta.threads.create()
        thread_id = openai_thread.id  # Asegúrate de que el objeto tenga un atributo 'id'
        # Guardar el hilo en la base de datos
        thread = Thread.objects.create(visitor=visitor, thread_id=thread_id)
        # Guardar el thread_id en la sesión
        request.session['thread_id'] = thread_id
    else:
        thread_id = request.session['thread_id']
        # Obtener el hilo de la base de datos
        thread = Thread.objects.get(thread_id=thread_id)


    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Es una solicitud AJAX
        data = json.loads(request.body)
        user_message_content = data.get('message')

        try:
            # Enviar el mensaje del usuario y crear una ejecución
            run = submit_message(client, ASSISTANT_ID, thread_id, user_message_content)
            print(f"se ha ejecutado run")

            # Esperar a que la ejecución esté completa
            run = wait_on_run(client, run, thread_id)
            print(f"se ha ejecutado wait on run")

            # Obtener la respuesta del asistente
            assistant_reply_content = run.results[0].messages[0].content[0].text.value
            print(f"se ha guardado la respuesta del asistente")

            # Guardar el mensaje del usuario en la base de datos
            Message.objects.create(thread=thread, role='user', content=user_message_content)
            print(f"Guardar el mensaje del usuario")

            # Guardar la respuesta del asistente en la base de datos
            Message.objects.create(thread=thread, role='assistant', content=assistant_reply_content)
            print(f"Guardar la respuesta del asistente en la base de datos")

            # Responder con la respuesta del asistente
            return JsonResponse({'assistant_reply': assistant_reply_content})
        except TimeoutError as e:
            return JsonResponse({'error': str(e)}, status=504)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # En caso de GET, mostrar los mensajes existentes
        messages = Message.objects.filter(thread=thread).order_by('created_at')
        return render(request, 'chat/chat.html', {'messages': messages, 'visitor': visitor})
