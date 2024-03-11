from dotenv import load_dotenv
load_dotenv()#loading all environment variables
import streamlit as st 
import os
from PIL import Image
import google.generativeai as genai
from google.generativeai.types import IncompleteIterationError
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model=genai.GenerativeModel("gemini-pro")
def get_gemini_chat_response(question):
    response = model.start_chat(history=[])  # Start a new chat session
    response = response.send_message(question, stream=True)
    return response
#vision pro model
model_new=genai.GenerativeModel("gemini-pro-vision")
def get_gemini_vision_response(image,question):
    response=model_new.generate_content([question,image])
    try:
        response.resolve()  # Ensure response completion before accessing attributes
    except IncompleteIterationError:
        pass 
    return response.parts[0].text

st.set_page_config(page_title="Question Answer Chatbot",page_icon=":gemini:",layout="wide")
st.write("<h1 style='color: orange;'>Gemini Chatbot</h1>", unsafe_allow_html=True)
st.write("<h6 style='color: orange;'>: LLM Application which answers any query</h6>",unsafe_allow_html=True)
# st.header("Gemini LLM Appliaction")

if 'chat_history'not in st.session_state:
    st.session_state['chat_history']=[]

input=st.text_input("YOU: ",key="input")

uploaded_file = st.file_uploader("📷", type=["jpg", "jpeg", "png"],key="image_upload")


submit=st.button("Ask the question","")
st.markdown("<i class='fas fa-paper-plane'></i>", unsafe_allow_html=True)

concat_text=""
if submit and input:
    # chat_response=get_gemini_chat_response(input)

    st.session_state['chat_history'].append(("You",input))
    if uploaded_file is not None:
        # Process uploaded image
        image = Image.open(uploaded_file)
        # Get response from vision model
        vision_response = get_gemini_vision_response(image,input)
        st.write(vision_response)
        st.image(image, caption="Uploaded Image",width=250)
        st.session_state['chat_history'].append(("Bot (Vision)", vision_response))
    else:
        chat_response=get_gemini_chat_response(input)
        for chunk in chat_response:
            concat_text+=chunk.text
        st.write(concat_text)
        st.session_state['chat_history'].append(("Bot",concat_text))

st.write("<h4><u style='color: orange;'>Chat History:</h4>",unsafe_allow_html=True)
for role,text in st.session_state['chat_history']:
    st.write(f"<b style='color: orange;'>{role}:</b> {text}",unsafe_allow_html=True)