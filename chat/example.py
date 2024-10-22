from openai import OpenAI

client = OpenAI(api_key="sk-Maxh5gGsn3pF9L6A_hr4UXsQYB2aUXETuVGZpL8ODeT3BlbkFJZ3DtkTo9Aju-RVVSdSgdEWcVX4Yl7dx6MDOCYQ4rUA"
)
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


my_thread = client.beta.threads.retrieve("thread_N5C8zAuG5Keij5MejKkjDM96")
print(my_thread)

'''
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content":  "como puedo guardar la respuesta de chatgpt api en un modelo de django, explicame paso a paso"
        }
    ]
)


respuesta= completion.choices[0].message
print(respuesta)
'''