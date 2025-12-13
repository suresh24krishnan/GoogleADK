import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

# Initialize client
client = genai.Client()

st.set_page_config(page_title="Educosys Multimodal AI App", layout="centered")

st.title("🎨 MediaMaker Multimodal AI App")
st.write("Generate images, captions, and YouTube summaries using multimodal Gemini models.")

# ---------------------------------------------------------
# SECTION 1: IMAGE GENERATION
# ---------------------------------------------------------
st.header("🖼️ Image Generator")

user_prompt = st.text_input("Describe the image you want me to generate:")

if st.button("Generate Image"):
    if not user_prompt:
        st.warning("Please enter a prompt!")
    else:
        try:
            with st.spinner("Generating image..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["Text", "Image"]
                    )
                )

            st.subheader("Generated Output")

            for part in response.candidates[0].content.parts:
                if part.text:
                    st.write(part.text)
                elif part.inline_data:
                    image = Image.open(BytesIO(part.inline_data.data))
                    st.image(image, caption="Generated Image")

        except Exception as e:
            st.error(f"Error generating image: {e}")

# ---------------------------------------------------------
# SECTION 2: IMAGE CAPTIONING
# ---------------------------------------------------------
st.header("📝 Image Caption Generator")

uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image")

    if st.button("Generate Caption"):
        try:
            with st.spinner("Generating caption..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=["What is this image?", image]
                )
            st.subheader("Generated Caption")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error generating caption: {e}")

# ---------------------------------------------------------
# SECTION 3: YOUTUBE VIDEO SUMMARIZER
# ---------------------------------------------------------
st.header("🎬 YouTube Video Summarizer")

youtube_url = st.text_input("Enter a YouTube video URL:")

if st.button("Summarize Video"):
    if not youtube_url:
        st.warning("Please enter a YouTube URL!")
    else:
        try:
            with st.spinner("Summarizing video..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=types.Content(
                        parts=[
                            types.Part(text="Summarize this video:"),
                            types.Part(
                                file_data=types.FileData(file_uri=youtube_url)
                            )
                        ]
                    )
                )
            st.subheader("Video Summary")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error generating summary: {e}")
