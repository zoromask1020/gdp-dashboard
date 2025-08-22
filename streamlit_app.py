import streamlit as st
import requests
from datetime import datetime

# Your n8n webhook URL (Test URL)
N8N_WEBHOOK_URL = "https://343ed076b52d.ngrok-free.app/webhook/cleaning"

# Get chat_id and service from query params
chat_id = st.query_params.get("chatid", [""])[0]
service_choice = st.query_params.get("service", [""])[0]

# Mapping param -> dropdown index
service_map = {
    "": 0,
    "house": 1,
    "car": 2,
    "office": 3
}

st.title("Service Request Form")

with st.form(key='service_form'):
    name = st.text_input("Name", "")
    email = st.text_input("Email", "")
    phone = st.text_input("Phone", "")
    rate = st.selectbox("Rate", ["", "1000-2000", "2000-3000", "3000-4000"])
    
    servicedesign = st.selectbox(
        "Services", 
        ["", "House Cleaning", "Car Cleaning", "Office Cleaning"],
        index=service_map.get(service_choice, 0)
    )
    
    condition = st.text_input("Condition", "") 
    address = st.text_input("Address", "")
    preferred_date = st.date_input("Preferred Cleaning Date")
    preferred_time = st.time_input("Preferred Cleaning Time")
    
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if not (name and email and phone and rate and servicedesign):
        st.error("Please fill all the fields!")
    else:
        current_time = preferred_time.strftime("%H:%M:%S")
        current_date = preferred_date.strftime("%Y-%m-%d")
        
        text_message = (
            f"*New Service Request Added!*\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Rate: {rate}\n"
            f"Services: {servicedesign}\n"
            f"Condition: {condition}\n"
            f"Address: {address}\n"
            f"Preferred Time: {current_time}\n"
            f"Preferred Date: {current_date}\n"
            f"✅ We’ll contact you shortly."
        )
        
        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "rate": rate,
            "service_design": servicedesign,
            "condition": condition,
            "address": address,
            "time": current_time,
            "date": current_date,
            "chat_id": chat_id,
            "text": text_message
        }
        
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload)
            if response.status_code == 200:
                st.success("Form submitted successfully! You can close the tab.")
            else:
                st.error(f"Failed to send to n8n. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")
