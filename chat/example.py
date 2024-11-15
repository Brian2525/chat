from openai import OpenAI
import os 


###listar asistentes 
'''
my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)
print(my_assistants.data)'''


##Asistente ID
''' 
my_assistant = client.beta.assistants.retrieve("asst_6tSMEXtaC23I2diV8Z5jdXWX")
print(my_assistant)

'''

'''message_thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Hola, quisiera un pollo "
    },
    {
      "role": "user",
      "content": "Hola tiene servicio?"
    },
  ]
)

print(message_thread)
'''

'''
my_thread = client.beta.threads.retrieve("thread_N5C8zAuG5Keij5MejKkjDM96")
print(my_thread)
'''


completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content":  "quiero que me digas hola en ingles"
        }
    ]
)


respuesta= completion.choices[0].message
respuesta_larga=completion.choices[0]
print(respuesta)
print(respuesta.content)
print(respuesta_larga)
