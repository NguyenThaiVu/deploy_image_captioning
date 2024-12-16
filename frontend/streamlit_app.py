import streamlit as st
import requests
from PIL import Image
import time

# Flask server URL
BACKEND_URL = "http://127.0.0.1:5000"
# BACKEND_URL = "https://backend.redfield-15d23ff1.canadaeast.azurecontainerapps.io:443"

st.title("Image Captioning")

st.sidebar.title("Connection Tools")
# Initialize session state for connection and device test results
if "connection_status" not in st.session_state:
    st.session_state["connection_status"] = None
if "device_status" not in st.session_state:
    st.session_state["device_status"] = None

# Connection Test
if st.sidebar.button("Check Back-End Connection"):
    try:
        response = requests.get(BACKEND_URL)  
        if response.status_code == 200:
            st.session_state["connection_status"] = "success"
        else:
            st.session_state["connection_status"] = f"error: {response.status_code}"
    except Exception as e:
        st.session_state["connection_status"] = f"error: {str(e)}"

# Display connection status in the sidebar
if st.session_state["connection_status"]:
    if st.session_state["connection_status"] == "success":
        st.sidebar.success("Connection to back-end is successful!")
    elif "error" in st.session_state["connection_status"]:
        st.sidebar.error(f"Back-end {st.session_state['connection_status']}")

# Device Test
if st.sidebar.button("Check Device"):
    try:
        response = requests.get(f"{BACKEND_URL}/device")  
        if response.status_code == 200:
            device = response.json().get("device", "Unknown")
            st.session_state["device_status"] = f"Device: {device}"
        else:
            error_message = response.json().get("error", "Unknown error")
            st.session_state["device_status"] = f"error: {error_message}"
    except Exception as e:
        st.session_state["device_status"] = f"error: {str(e)}"

# Display device status in the sidebar
if st.session_state["device_status"]:
    if "Device" in st.session_state["device_status"]:
        st.sidebar.success(st.session_state["device_status"])
    elif "error" in st.session_state["device_status"]:
        st.sidebar.error(st.session_state["device_status"])



uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", width=500)

    # Generate Caption Button
    if st.button("Generate Caption"):
        # Send the image to the Flask back-end
        st.write("Generating caption...")
        try:
            start_time = time.time()  
            response = requests.post(
                f"{BACKEND_URL}/caption",
                files={"image": uploaded_image.getvalue()}
            )
            end_time = time.time()
            response_time = end_time - start_time

            if response.status_code == 200:
                caption = response.json().get("caption", "No caption generated")
                st.success(f"Generated Caption: {caption}")
                st.success(f"Response Time: {response_time:.3f} seconds")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")

        except Exception as e:
            st.error(f"Error: {e}")
