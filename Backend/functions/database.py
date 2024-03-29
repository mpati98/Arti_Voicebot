import json
import random


#Get recent message
def get_recent_messages():

    #Define the filename and learn instruction
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content": "You are interviewing the user for a jos as retail assistant. Ask short questions that are relevant to the junior position. Your name is Arti. The user called Shaun. Keep your answers to under 30 words."
    } 

    # Initialize messages
    messages = []

    #Add a random element
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + " Your reponse will include some dry humor."
    else:
        learn_instruction["content"] = learn_instruction["content"] + " Your reponse will include rather challenging question."

    # Append instruction to message
    messages.append(learn_instruction)

    #Get last message:
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)
            # Add last 5 messages
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
    except Exception as e:
        print(e)

    return messages

# Stored message
def store_messages(request_message, response_message):
    #Define the filename and learn instruction
    file_name = "stored_data.json"

    # Get recent messages
    messages = get_recent_messages()[1:]

    # Add messages to data
    user_message = {"role": "user", "content": request_message}
    assitant_message = {"role": "user", "content": response_message}
    messages.append(user_message)
    messages.append(assitant_message)

    # Save the updated file
    with open(file_name, 'w') as f:
        json.dump(messages, f)

# Reset messages
def reset_message():
    # Overwrite current file with nothing
    open("stored_data.json", "w") 