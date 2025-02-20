import firebase_admin
from firebase_admin import credentials, firestore, auth  # <-- Add auth import
import streamlit as st

# Ensure the Firebase config is a proper dictionary
firebase_config = dict(st.secrets["firebase"])  

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
        # Check if user already exists in Firebase Authentication
        try:
            user = auth.get_user_by_email(email)
            # If the user exists, delete them
            auth.delete_user(user.uid)
        except auth.UserNotFoundError:
            pass  # If user does not exist, continue

        # Create new user in Firebase Authentication
        user = auth.create_user(email=email, password=password)
        
        return user.uid  # Return the new user ID
    except Exception as e:
        return str(e)

# Login Function
def login_user(email, password):
    users_ref = db.collection("users").where("email", "==", email).stream()
    for user in users_ref:
        return user.id
    return None

# Store User Data
def save_user(uid, email, name, phone, experience, position, location, tech_stack):
    user_data = {"email": email, "name": name, "phone": phone, "experience": experience, "position": position, "location": location, "tech_stack": tech_stack}
    db.collection("users").document(uid).set(user_data)

# Retrieve User Data
def get_user_data(uid):
    return db.collection("users").document(uid).get().to_dict()

# Delete User Data Function
def delete_user_data(uid):
    try:
        # Delete user's chat history
        chats_ref = db.collection("users").document(uid).collection("chats").stream()
        for chat in chats_ref:
            chat.reference.delete()

        # Delete user document from Firestore
        db.collection("users").document(uid).delete()

        # Delete user from Firebase Authentication
        auth.delete_user(uid)

        return True
    except Exception as e:
        return str(e)


