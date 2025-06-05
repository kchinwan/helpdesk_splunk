import json
import os

def save_chat(chat_id, chat_data, folder="saved_chats"):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, f"{chat_id}.json"), "w") as f:
        json.dump(chat_data, f, indent=2)

def load_chat(chat_id, folder="saved_chats"):
    path = os.path.join(folder, f"{chat_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None