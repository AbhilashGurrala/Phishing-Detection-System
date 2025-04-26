import streamlit as st
from detect_single_email import detect_single_email

st.title("Phishing Email Detection System")

st.write("Enter the email details below to check if it is a phishing attempt:")

# Input fields
sender = st.text_input("Sender Email")
receiver = st.text_input("Receiver Email")
subject = st.text_input("Email Subject")
body = st.text_area("Email Body", height=200)

# When button is clicked
if st.button("Check for Phishing"):
    if sender and receiver and subject and body:
        result, confidence = detect_single_email(sender, receiver, subject, body)
        st.subheader("Result")
        st.write(f"**Prediction:** {result}")
        st.write(f"**Confidence Score:** {confidence}%")
    else:
        st.warning("Please fill in all the fields before submitting.")