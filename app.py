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

/* Remove person and robot avatars */
[data-testid="stChatMessageAvatar"] {
    display: none !important;
}

/* Common chat bubble styling */
[data-testid="stChatMessage"] {
    padding: 12px 18px;
    border-radius: 18px;
    margin: 12px 0;
    max-width: 80%;
    width: fit-content;
}

/* User messages - right side */
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background-color: #d9fdd3;
    margin-left: auto;
    margin-right: 0;
    color: #111111;
}

/* Bot messages - left side */
[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background-color: #eeeeee;
    margin-right: auto;
    margin-left: 0;
    color: #111111;
}

/* Message text */
[data-testid="stChatMessage"] p {
    color: #111111 !important;
    font-size: 16px;
}

/* Remove unnecessary message borders */
[data-testid="stChatMessage"] {
    border: none !important;
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
    with st.chat_message(message["role"],
                         avatar=None
    ):
        st.markdown(message["content"])
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
