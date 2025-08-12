import streamlit as st
import requests
from datetime import datetime

# Your n8n webhook URL (Test URL)
N8N_WEBHOOK_URL = "https://202e1bfb0d1d.ngrok-free.app/webhook-test/cleaning"

# Get chat_id from query params
chat_id = st.query_params.get("chatid", [""])

st.title("Service Request Form")

with st.form(key='service_form'):
    name = st.text_input("Name", "")
    email = st.text_input("Email", "")
    phone = st.text_input("Phone", "")
    rate = st.selectbox("Rate", ["", "1000-2000", "2000-3000", "3000-4000"])
    servicedesign = st.selectbox("Services", ["", "House Cleaning", "Car Cleaning", "Office Cleaning"])
    condition = st.text_input("Condition", "") 
    
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if not (name and email and phone and rate and servicedesign):
        st.error("Please fill all the fields!")
    else:
        # Auto-generate current date and time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%Y-%m-%d")

        # Build Telegram confirmation message
        text_message = (
            f"*New Service Request Received!*\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Rate: {rate}\n"
            f"Services: {servicedesign}\n"
            f"Condition: {condition}\n"
            f"Time: {current_time}\n"
            f"Date: {current_date}\n"
            f"✅ We’ll contact you shortly."
        )

        # Data to send to n8n (and then to MySQL)
        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "rate": rate,
            "service_design": servicedesign,
            "condition": condition,
            "time": current_time,
            "date": current_date,
            "chat_id": chat_id,
            "text": text_message
        }

        try:
            # Send to n8n webhook
            response = requests.post(N8N_WEBHOOK_URL, json=payload)

            if response.status_code == 200:
                st.success("Form submitted successfully! You can close the tab.")
            else:
                st.error(f"Failed to send to n8n. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")
