from decouple import config
import requests

# Retrieve Environment Variables
ELEVEN_LAB_API_KEY = config("ELEVEN_LAB_API_KEY")

# Eleven lab
def text2speech(message):

    # Define data - body
    body = {
        "text": message,
        "voice_setting":{
            "stability": 0,
            "similarity_boost": 0,
        }
    }

    # Define voice - search https://api.elevenlabs.io/v1/voices
    voice_Rachel = "21m00Tcm4TlvDq8ikWAM"

    # Constructing Headers and Endpoint
    headers = {"xi-api-key": ELEVEN_LAB_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_Rachel}"

    # Send request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
        
    except Exception as e:
        print(e)
        return
    if response.status_code == 200:
            return response.content
    else:
            return