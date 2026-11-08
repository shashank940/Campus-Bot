import streamlit as st
from chatbot import get_answer

# Page configuration
st.set_page_config(
    page_title="CampusBot",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
<style>

/* Page background */
.stApp {
    background-color: #f0f4f8;
}

/* All headings */
h1, h2, h3 {
    color: #123456 !important;
}

/* Normal text */
.stApp p,
.stApp label,
.stMarkdown {
    color: #263445 !important;
}

/* Input field */
.stTextInput input {
    background-color: #ffffff !important;
    color: #123456 !important;
    border: 2px solid #123456 !important;
}

/* All buttons */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #123456 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}

/* Button text */
.stButton > button p,
.stFormSubmitButton > button p {
    color: #ffffff !important;
}

/* Button hover */
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #245b89 !important;
    color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)
# Main heading
st.title("🎓 Welcome to CampusBot")
st.subheader("Your Virtual Campus Assistant! 🤖")
st.write("Ask me anything about your college!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# Function to process questions
def process_question(question):

    if question.strip():
        st.session_state["messages"].append({
            "role": "user",
            "content": question
        })

        answer = get_answer(question)

        st.session_state["messages"].append({
            "role": "assistant",
            "content": answer
        })




# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Quick questions
st.write("### Quick Questions")

col1, col2 = st.columns(2)

with col1:
    if st.button("Available Courses"):
        process_question("Which courses are available?")
        st.rerun()

with col2:
    if st.button("Admission Details"):
        process_question("How can I get admission?")
        st.rerun()


# Normal chat input
with st.form("chat_form", clear_on_submit=True):
    question = st.text_input(
        "Ask me anything about your campus life!"
    )

    submit = st.form_submit_button("Send")

    if submit and question.strip():
        process_question(question)
        st.rerun()
# Clear Chat button at bottom-right
col1, col2 = st.columns([5, 1])

with col2:
    if st.button("🗑️ Clear Chat"):
        st.session_state["messages"] = []
        st.rerun()
