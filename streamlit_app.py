import streamlit as st
import requests

# Get chat_id from query params
chat_id = st.query_params.get('chatid', [''])[0]  # fixed to take first value
CHAT_ID = chat_id

# Your Telegram bot token
BOT_TOKEN = '8421113239:AAEI_RdMhkJCznGfLxj931EJ04t9UeFl1PU'

# Your n8n webhook URL (must be POST-enabled)
WEBHOOK_URL = "https://202e1bfb0d1d.ngrok-free.app/webhook/cleaning"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot8421113239:AAEI_RdMhkJCznGfLxj931EJ04t9UeFl1PU/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    return response.ok

def send_to_webhook(data):
    try:
        r = requests.post(WEBHOOK_URL, json=data)
        return r.status_code == 200
    except Exception as e:
        return False

st.title("Service Request Form")

with st.form(key='service_form'):
    name = st.text_input("Name", "")
    email = st.text_input("Email", "")
    phone = st.text_input("Phone", "")
    rate = st.text_input("Rate", "")
    servicedesign = st.selectbox("Service Design", ["", "Basic", "Premium", "Custom"])
    
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if not (name and email and phone and rate and servicedesign):
        st.error("Please fill all the fields!")
    else:
        # Data to send
        data = {
            "chat_id": chat_id,
            "name": name,
            "email": email,
            "phone": phone,
            "rate": rate,
            "service_design": servicedesign
        }
        
        # Send message to Telegram
        message = (
            f"*New Service Request:*\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Rate: {rate}\n"
            f"Service Design: {servicedesign}"
        )
        telegram_ok = send_telegram_message(message)
        
        # Send data to n8n webhook (for MySQL insert or other processing)
        webhook_ok = send_to_webhook(data)
        
        # Show results
        if telegram_ok and webhook_ok:
            st.success("Form submitted, message sent to Telegram, and data sent to webhook!")
        elif telegram_ok and not webhook_ok:
            st.warning("Message sent to Telegram, but failed to send data to webhook.")
        elif not telegram_ok and webhook_ok:
            st.warning("Data sent to webhook, but failed to send message to Telegram.")
        else:
            st.error("Failed to send both Telegram message and webhook data.")
