import streamlit as st
import requests
st.write("Query params:", st.query_params)

chat_id = st.query_params.get('chatid', [''])[0]

st.write("Chat ID from query:", chat_id)
CHAT_ID = chat_id


# Your Telegram bot token and chat ID
BOT_TOKEN = '8421113239:AAEI_RdMhkJCznGfLxj931EJ04t9UeFl1PU'
# CHAT_ID = 8341153272  # or get dynamically from user input if you want



def send_telegram_message(text):
    url = f"https://api.telegram.org/bot8421113239:AAEI_RdMhkJCznGfLxj931EJ04t9UeFl1PU/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    return response.ok

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
        message = (
            f"*New Service Request:*\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Rate: {rate}\n"
            f"Service Design: {servicedesign}"
        )
        success = send_telegram_message(message)
        if success:
            st.success("Form submitted and message sent to Telegram!")
        else:
            st.error(f"Failed to send message to Telegram. Please try again.old: {chat_id},{CHAT_ID},{message}")
