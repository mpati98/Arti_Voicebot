# uvicorn main:app
# uvicorn main:app --reload

# Main Import
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

# Custom function imports
from functions.database import store_messages, reset_message
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import text2speech



app = FastAPI()


# CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000"
]

# CORS - Middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def check_health():
    return {"message": "Healthy"}

@app.get("/reset")
async def reset_conversation():
    reset_message()
    return {"message": "Conversation was reset"}


@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    # #Get saved audio
    # audio_input = open("test_sound.mp3", "rb")

    # Save audio file from Frontent
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    #Decode audio
    message_decoded = convert_audio_to_text(audio_input)

    # Guard: Ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")
    
    # Get GPT response
    chat_response = get_chat_response(message_decoded)

    # Guard: Ensure message response
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chat response")
    
    # Store messages
    store_messages(message_decoded, chat_response)

    # Convert chat response to voice
    audio_output = text2speech(chat_response)

    # Guard: Ensure message response
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get Eleven Labs audio response")
    
    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="application/octet-stream")