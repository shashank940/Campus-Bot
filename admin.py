import streamlit as st
import json
import os

st.set_page_config(
    page_title="CampusBot Admin",
    page_icon="🎓"
)

st.title("🎓 CampusBot Admin Dashboard")

FILE = "faqs.json"

# Load FAQs
def load_faqs():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Save FAQs
def save_faqs(data):
    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Add FAQ
st.subheader("Add New FAQ")

with st.form("faq_form"):

    questions = st.text_area(
        "Enter example questions (one per line)",
        placeholder="Which courses are available?\nWhat courses does the college offer?"
    )

    answer = st.text_area("Enter answer")

    submit = st.form_submit_button("Add FAQ")

    if submit:

        question_list = [
            q.strip()
            for q in questions.split("\n")
            if q.strip()
        ]

        if question_list and answer.strip():

            faqs = load_faqs()

            faqs.append({
                "questions": question_list,
                "answer": answer.strip()
            })

            save_faqs(faqs)

            st.success("FAQ added successfully!")

        else:
            st.warning("Please enter questions and an answer.")

# Display existing FAQs
st.subheader("Existing FAQs")

faqs = load_faqs()

if faqs:

    for index, faq in enumerate(faqs, start=1):

        with st.expander(f"FAQ {index}"):

            examples = faq.get(
                "questions",
                [faq.get("question", "")]
            )

            st.write("**Example Questions:**")

            for q in examples:
                st.write("- " + q)

            st.write("**Answer:**")
            st.write(faq["answer"])

else:
    st.info("No FAQs available.")