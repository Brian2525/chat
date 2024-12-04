from django.shortcuts import render, redirect
import requests
from .models import  AssistantDescription
from .forms import VisitorForm, ChatForm
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from . import utils
import os 

from openai import OpenAI


client = OpenAI(api_key=settings.OPENAI_API_KEY)
assist=AssistantDescription.objects.get(id=1)


'''
def chat_view(request):
    # Initialize variables
    visitor = None
    messages = []
    conversation = None

    # Check if visitor is in session
    visitor_id = request.session.get('visitor_id')
    if visitor_id:
        visitor = Visitor.objects.get(id=visitor_id)

    if request.method == 'POST':
        # Handle Visitor Form
        if not visitor:
            visitor_form = VisitorForm(request.POST)
            if visitor_form.is_valid():
                visitor = visitor_form.save()
                request.session['visitor_id'] = visitor.id
                return redirect('chat_view')
        else:
            chat_form = ChatForm(request.POST)
            if chat_form.is_valid():
                # Get or create conversation
                conversation_id = request.session.get('conversation_id')
                if conversation_id:
                    conversation = Conversation.objects.filter(conversation_id=conversation_id, visitor=visitor).first()
                else:
                    conversation = Conversation(visitor=visitor)
                    conversation.save()
                    request.session['conversation_id'] = str(conversation.conversation_id)
                # Save user's message
                user_message_content = chat_form.cleaned_data['message']
                user_message = Message(conversation=conversation, sender='user', content=user_message_content)
                user_message.save()
                # Prepare messages for OpenAI API
                # Prepare messages for OpenAI API
                messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
                openai_messages = []
                # Include the assistant description
                assistant_description = assist.description
                
                
                if assistant_description:
                    openai_messages.append({'role': 'system', 'content': assistant_description})
                else:
                    openai_messages.append({'role': 'system', 'content': 'You are a helpful assistant.'})
                for msg in messages:
                    openai_messages.append({'role': msg.sender, 'content': msg.content})
                # Call OpenAI API
                 # Replace with your actual API key
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=openai_messages
                )
                
                respuesta= response.choices[0].message
                print(respuesta.content)
                assistant_reply = respuesta.content
                print(assistant_reply)

                # Save assistant's message
                assistant_message = Message(conversation=conversation, sender='assistant', content=assistant_reply)
                assistant_message.save()
                return redirect('chat_view')
    else:
        if visitor:
            chat_form = ChatForm()
            conversation_id = request.session.get('conversation_id')
            if conversation_id:
                conversation = Conversation.objects.filter(conversation_id=conversation_id, visitor=visitor).first()
                if conversation:
                    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
        else:
            visitor_form = VisitorForm()
            chat_form = None

    context = {
        'visitor_form': visitor_form if not visitor else None,
        'chat_form': chat_form if visitor else None,
        'messages': messages,
    }
    return render(request, 'chat/chat.html', context)
'''









def GetResponse(text):
    assistant_description = assist.description
    try:
        completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", 'content':assistant_description},
                            {"role": "user", "content": text}
                        ]
                                        )
        response= (completion.choices[0].message)
        respuesta= response.content
        return respuesta


    except Exception as exception: 
        print(exception)
        return "error" 






#GET 
def verify_token(request):
    try:
        if request.method == "GET":
            accessToken = "153ASD51AD1ASD1545476A68"
            token = request.GET.get("hub.verify_token")
            challenge = request.GET.get("hub.challenge")

            # Check if both token and challenge exist, and if token matches
            if token and challenge and token == accessToken:
                return HttpResponse(challenge)
            else:
                # Return a 400 status code if conditions are not met
                return HttpResponse(status=400)

    except Exception as e:
        # Log the error and return 400 status code if any exception occurs
        print(f"Error: {e}")
        return HttpResponse(status=400)
    

#POST
@csrf_exempt
def receive_message(request):
    try:
        print("intenta")
        if request.method == "POST":
            print("si POST ")
            body = json.loads(request.body)  # Cargar el JSON del cuerpo de la solicitud
            entry = (body["entry"][0])
            changes = (entry["changes"][0])
            value = changes["value"]
            message = (value["messages"])[0]  # Corrección aquí, asegúrate de que existe "messages"
            number=message["from"]
            print(number)
            

            text= utils.TextUser(message)
            #ProcessMessage(text, number )
            print(text)
            responseGPT=GetResponse(text)
            print(responseGPT)
            if responseGPT!="error": 
                data=utils.TextMessage(responseGPT, number)
                print(data)
            else: 
                data=utils.TextMessage("Lo siento ocurrio un problema", number)
            

            sendMessageWhatsapp(data)


           
            # Responder con "EVENT_RECEIVED" en el cuerpo de la respuesta
            return HttpResponse("EVENT_RECEIVED", status=200)
         
        return HttpResponse("Method Not Allowed", status=405)
    
    except KeyError as e:
        print(f"Clave no encontrada: {e}")
        return HttpResponse("EVENT_RECEIVED", status=200)
    
    except json.JSONDecodeError:
        print("Error al decodificar JSON")
        return HttpResponse("EVENT_RECEIVED", status=400)
    
    except Exception as e:
        print(f"Error inesperado: {e}")
        return HttpResponse("EVENT_RECEIVED", status=500)




def GenerateMessage(text, number):
    if "text" in text:
        data=utils.TextMessage("Text", number)
    if "format" in text: 
        data=utils.TextFormatMessage(number)
    if "image" in text: 
        data=utils.ImageMessage(number)
    if "audio" in text: 
        data=utils.AudioMessage(number)
    if "document" in text: 
        data=utils.DocumentMessage(number)
    
     
    sendMessageWhatsapp (data)



def sendMessageWhatsapp(data): 
    try: 
        print("1")
        token = settings.WHATSAPP_TOKEN
        print("2")
        api_url = "https://graph.facebook.com/v20.0/248148378380644/messages"
        
       #https://graph.facebook.com/v21.0/461768510359019/messages - este es el que se usa con el numero de illutio
       #https://graph.facebook.com/v20.0/248148378380644/messages - este es el que se usa con el numero TEST de Whatsapp
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        print("3")
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        
        print("4")
        if response.status_code == 200:
            return True 
        print("5")
        print(f"Error en la respuesta: {response.status_code} - {response.text}")
        return False 
        print("6")
    except Exception as exception: 
        print(f"Error al enviar el mensaje de WhatsApp: {exception}")
        return False

