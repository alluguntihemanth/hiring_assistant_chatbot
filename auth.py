import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

# Ensure the Firebase config is a proper dictionary
firebase_config = json.loads(st.secrets["firebase"])  # Convert from AttrDict to dict

# Validate that 'type' is 'service_account'
if "type" not in firebase_config or firebase_config["type"] != "service_account":
    raise ValueError("Invalid Firebase credentials: Missing or incorrect 'type' field.")

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()


# Signup Function
def signup_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except Exception as e:
        return str(e)

# Login Function
def login_user(email, password):
    users_ref = db.collection("users").where("email", "==", email).stream()
    for user in users_ref:
        return user.id
    return None

# Store User Data
def save_user(uid, email, name, tech_stack):
    user_data = {"email": email, "name": name, "tech_stack": tech_stack}
    db.collection("users").document(uid).set(user_data)

# Retrieve User Data
def get_user_data(uid):
    return db.collection("users").document(uid).get().to_dict()

# Delete User Data Function
def delete_user_data(uid):
    try:
        # Delete user's chat history
        chats_ref = db.collection("users").document(uid).collection("chats")
        for chat in chats_ref.stream():
            chat.reference.delete()

        # Delete user document
        db.collection("users").document(uid).delete()

        # Delete user from Firebase Authentication
        auth.delete_user(uid)

        return True
    except Exception as e:
        return str(e)
