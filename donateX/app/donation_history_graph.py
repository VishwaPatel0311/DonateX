import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# Set up the API URL
API_URL = "http://localhost:14011/donate/summary/plot"

# Streamlit UI
st.title("📊 Donation Summary Dashboard")

# Input for JWT token
token = st.text_input("Enter your Bearer Token (JWT):", type="password")
# Add Streamlit widgets to input date range
start_date = st.date_input("Start Date", value="2025-04-01")
end_date = st.date_input("End Date", value="2025-04-30")


# Button to fetch the graph
if st.button("Get Donation Summary Plot"):
    if not token:
        st.warning("Please enter a valid token.")
    else:
        try:
            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = requests.get(
                API_URL,
                params={"start_date": start_date, "end_date": end_date},
                headers=headers
            )
            print("response", response)
            # print("response.json()", response.json())
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption="Donation Summary Plot", use_column_width=True)
            else:
                print(f"Request failed: {response.status_code} - {response.text}")
                st.error(f"Request failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
            st.error(f"An error occurred: {e}")