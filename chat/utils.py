
def TextUser(message): 
    try:
        text = ""
        typeMessage = message.get("type", "")

        if typeMessage == "text": 
            text = message.get("text", {}).get("body", "")
            
        elif typeMessage == "interactive": 
            interactiveObject = message.get("interactive", {})
            typeInteractive = interactiveObject.get("type", "")
            print(typeInteractive)

            if typeInteractive == "button_reply": 
                text = interactiveObject.get("button_reply", {}).get("title", "")
            elif typeInteractive == "list_reply": 
                text = interactiveObject.get("list_reply", {}).get("title", "")
            else:
                print("sin mensaje")

        else: 
            print("sin mensaje")
        
        print(text)
        return text

    except Exception as e:
        print(f"Ocurrió un error en TextUser: {e}")
        return ""
    

def TextMessage(text, number): 
        data= {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": text
            }
        }
        return data 
        
      
def TextFormatMessage(number): 
        data= {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": "*Hola usuario* - _Hola usuario_ - ''' hola usuario ''' "
                }
            }
        return data 

def ImageMessage(number): 
        data= {
                "messaging_product": "whatsapp",    
                "to": number,
                "type": "image",
                "image": {
                    "link": "https://illut.io/wp-content/uploads/2023/07/augmented_reality_home-395x268.png"
                }
            }
        return data 

def AudioMessage(number): 
        data= {
                "messaging_product": "whatsapp",    
                "to": number,
                "type": "audio",
                "audio": {
                    "link": "https://realidadaumentada.app/illutio/audio.mp3"
                }
            }
        return data 

def VideoMessage(number): 
        data= {
                "messaging_product": "whatsapp",    
                "to": number,
                "type": "video",
                "video": {
                    "link": "https://realidadaumentada.app/illutio/audio.mp3"
                }
            }
        return data 

def DocumentMessage(number): 
        data= {
                "messaging_product": "whatsapp",    
                "to": number,
                "type": "document",
                "document": {
                    "link": "https://realidadaumentada.app/illutio/ra_servicios.pdf"
                }
            }
        return data 