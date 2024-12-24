# import streamlit as st
# import requests
# import os
# from PIL import Image
# from io import BytesIO
# import base64

# # Dynamic backend URL
# BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000/track_symptoms/")

# # Streamlit UI
# st.title("Patient Progress Tracker")

# # Upload files
# st.subheader("Upload Therapy Session Files")
# uploaded_files = st.file_uploader("Upload multiple files (JSON or TXT)", accept_multiple_files=True, type=["json", "txt"])

# if uploaded_files:
#     if st.button("Analyze Progress"):
#         # Send files to the backend
#         files = [("files", (file.name, file, file.type)) for file in uploaded_files]
#         response = requests.post(BACKEND_URL, files=files)

#         if response.status_code == 200:
#             data = response.json()

#             # Render diagnosis
#             st.subheader("Patient Current Diagnosis")
#             st.text(data.get("diagnosis", "No diagnosis available"))

#             # Render progress score
#             st.subheader("Cumulative Progress Score")
#             st.metric("Progress Score", data.get("progress_score", "N/A"))
            
#             # Render plot image
#             st.subheader("Symptoms Tracked Over time")
#             image_base64 = data.get("symptoms_plot_image", "")
#             if image_base64:
#                 image = Image.open(BytesIO(base64.b64decode(image_base64)))
#                 st.image(image, caption="Symptom Progress Over Sessions")
            
#             st.subheader("Other Themes Tracked Over time")
#             image_base64 = data.get("theme_plot_image", "")
#             if image_base64:
#                 image = Image.open(BytesIO(base64.b64decode(image_base64)))
#                 st.image(image, caption="Symptom Progress Over Sessions")

#             # Render summary
#             st.subheader("Symptoms Progress Summary")
#             st.text(data.get("summary", "No summary available"))
            
#             # Render recommendation
#             st.subheader("Recommendations")
#             st.text(data.get("recommendation", "No recommendation available"))

#         else:
#             st.error("Failed to process files. Please try again.")



import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO
import base64

# Dynamic backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000/track_symptoms/")

# Inject custom CSS to reduce margins and increase container width
st.markdown(
    """
    <style>
        .main {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            max-width: 1600px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit UI
st.title("Patient Progress Tracker")

# Upload files
st.subheader("Upload Therapy Session Files")
uploaded_files = st.file_uploader("Upload multiple files (JSON or TXT)", accept_multiple_files=True, type=["json", "txt"])

if uploaded_files:
    if st.button("Analyze Progress"):
        # Send files to the backend
        files = [("files", (file.name, file, file.type)) for file in uploaded_files]
        response = requests.post(BACKEND_URL, files=files)

        if response.status_code == 200:
            data = response.json()

            # Divide the page into two sections
            left_col, right_col = st.columns([3, 2])  # Left is wider for text

            # Right section: Images first
            with right_col:
                st.subheader("Symptoms Tracked Over Time")
                image_base64 = data.get("symptoms_plot_image", "")
                if image_base64:
                    image = Image.open(BytesIO(base64.b64decode(image_base64)))
                    st.image(image, caption="Symptom Progress Over Sessions", use_container_width=True)

                st.subheader("Other Themes Tracked Over Time")
                image_base64 = data.get("theme_plot_image", "")
                if image_base64:
                    image = Image.open(BytesIO(base64.b64decode(image_base64)))
                    st.image(image, caption="Progress Over Sessions (other metrics)", use_container_width=True)

            # Left section: Text-based information
            with left_col:
                # Render diagnosis
                st.subheader("Patient Current Diagnosis")
                st.text(data.get("diagnosis", "No diagnosis available"))

                # Render progress score
                st.subheader("Cumulative Progress Score")
                st.metric("Progress Score", data.get("progress_score", "N/A"))

                # Render summary
                st.subheader("Symptoms Progress Summary")
                st.text(data.get("summary", "No summary available"))

                # Render recommendation
                st.subheader("Recommendations")
                st.text(data.get("recommendation", "No recommendation available"))

        else:
            st.error("Failed to process files. Please try again.")
