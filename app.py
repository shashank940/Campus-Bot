import streamlit as st
import html
from chatbot import get_answer

st.set_page_config(
    page_title="CampusBot",
    page_icon="🎓",
    layout="centered"
)

# Custom styling
st.markdown("""
<style>
#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 130px;
}

/* Hide default avatars */
[data-testid="stChatMessageAvatar"] {
    display: none !important;
}

/* Hide default chat message backgrounds */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* Chat rows */
.chat-row {
    display: flex;
    width: 100%;
    margin: 14px 0;
}

.chat-row.user {
    justify-content: flex-end;
}

.chat-row.bot {
    justify-content: flex-start;
}

/* Message bubbles */
.chat-bubble {
    max-width: 78%;
    padding: 12px 17px;
    border-radius: 20px;
    font-size: 16px;
    line-height: 1.5;
    overflow-wrap: anywhere;
}

.user .chat-bubble {
    background: #2563eb;
    color: white;
    border-bottom-right-radius: 5px;
}

.bot .chat-bubble {
    background: #303846;
    color: white;
    border-bottom-left-radius: 5px;
}
div[data-testid="stButton"] button {
    border-radius: 20px;
    background: #303846;
    color: white;
}

/* Mobile layout */
@media (max-width: 600px) {
    .block-container {
        padding-left: 15px;
        padding-right: 15px;
        padding-bottom: 130px;
    }

    .chat-bubble {
        max-width: 99%;
        font-size: 16px;
    }

    div[data-testid="stButton"] {
        right: 12px;
        bottom: 85px;
    }
}
</style>
""", unsafe_allow_html=True)
# Heading
st.title("🎓 Welcome to CampusBot")
st.subheader("Your Virtual Campus Assistant!")
st.write("Ask me anything about your college!")

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:

    role = message["role"]
    content = html.escape(message["content"])

    if role == "user":
        st.markdown(
            f'<div class="chat-row user">'
            f'<div class="chat-bubble">{content}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-row bot">'
            f'<div class="chat-bubble">{content}</div>'
            f'</div>',
            unsafe_allow_html=True
        )



# input
question = st.chat_input(
    "Ask me anything about your campus life!"
)

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    answer = get_answer(question)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()
