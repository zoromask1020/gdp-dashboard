import streamlit as st
import requests

# Your n8n webhook URL (Test URL)
N8N_WEBHOOK_URL = "https://202e1bfb0d1d.ngrok-free.app/webhook-test/cleaning"

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
        # Data to send to n8n
        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "rate": rate,
            "service_design": servicedesign
        }

        try:
            # Send to n8n webhook
            response = requests.post(N8N_WEBHOOK_URL, json=payload)

            if response.status_code == 200:
                st.success("Form submitted to n8n successfully!")
            else:
                st.error(f"Failed to send to n8n. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")
