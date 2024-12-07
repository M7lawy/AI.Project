import os
from gtts import gTTS
from deep_translator import GoogleTranslator
import streamlit as st

# Ensure the 'static' directory exists
if not os.path.exists('static'):
    os.makedirs('static')

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Text-to-Speech & Translation App",
    page_icon="🎙️",
    layout="centered",
)

# App title
st.title("🎙️ Text-to-Speech & Translation App")
st.markdown("Convert your text to speech or translate and convert it into audio!")

# Sidebar for user options
option = st.sidebar.radio(
    "Choose an option:",
    ["Text-to-Speech Only", "Translate and Text-to-Speech"]
)

# Upload a text file
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
if uploaded_file:
    # Read uploaded file content
    text = uploaded_file.read().decode("utf-8")
    st.success("File uploaded successfully!")
else:
    # If no file is uploaded, use the text box
    text = st.text_area("Enter the text:")

# Language options
if option == "Text-to-Speech Only":
    speech_language = st.selectbox(
        "Select the speech language:",
        [("English", "en"), ("Spanish", "es"), ("German", "de"), ("Arabic", "ar")],
        format_func=lambda lang: lang[0]
    )
elif option == "Translate and Text-to-Speech":
    translate_language = st.selectbox(
        "Select the translation language:",
        [("English", "en"), ("Spanish", "es"), ("German", "de"), ("Arabic", "ar")],
        format_func=lambda lang: lang[0]
    )

# Button to process the input
if st.button("Process"):
    if not text.strip():
        st.warning("Please enter or upload some text.")
    else:
        audio_filename = "static/output.mp3"

        if option == "Text-to-Speech Only":
            # Text-to-Speech only
            tts = gTTS(text=text, lang=speech_language[1])
            tts.save(audio_filename)
            st.success("Text-to-Speech conversion successful!")
        elif option == "Translate and Text-to-Speech":
            # Translate and Text-to-Speech
            translated_text = GoogleTranslator(source='auto', target=translate_language[1]).translate(text)
            tts = gTTS(text=translated_text, lang=translate_language[1])
            tts.save(audio_filename)
            st.success("Translation and Text-to-Speech conversion successful!")
            st.text_area("Translated Text:", value=translated_text, height=100)

            # Copy translated text button
            st.download_button(
                label="Copy Translated Text",
                data=translated_text,
                file_name="translated_text.txt",
                mime="text/plain"
            )

        # Corrected audio player for mobile compatibility
        st.audio(audio_filename, format="audio/mp3")

# Footer
st.markdown(
    """
    <div style="text-align: center; font-size: small;">
        Project by Engineering Students, Tanta University, AI Department.  
        Team Members: Mohamed Elmhlawy, Ahmed Talaat, Omar Yasser, Kareem Saadallah, Zeyad ElSheikh.
    </div>
    """,
    unsafe_allow_html=True,
)
