import streamlit as st
import requests
from PIL import Image

# Flask server URL
BACKEND_URL = "http://127.0.0.1:5000"

st.title("Image Captioning with Streamlit and Flask")

# Connection Test
if st.button("Check Back-End Connection"):
    try:
        response = requests.get(BACKEND_URL)  
        if response.status_code == 200:
            st.success("Connection to back-end is successful!")
        else:
            st.error(f"Back-end responded with status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error connecting to back-end: {e}")


uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Generate Caption Button
    if st.button("Generate Caption"):
        # Send the image to the Flask back-end
        st.write("Generating caption...")
        try:
            response = requests.post(
                f"{BACKEND_URL}/caption",
                files={"image": uploaded_image.getvalue()}
            )

            if response.status_code == 200:
                caption = response.json().get("caption", "No caption generated")
                st.success(f"Generated Caption: {caption}")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")

        except Exception as e:
            st.error(f"Error: {e}")
