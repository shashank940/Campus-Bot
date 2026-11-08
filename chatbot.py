import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

FAQ_FILE = "faqs.json"


def load_faqs():
    if not os.path.exists(FAQ_FILE):
        return []

    with open(FAQ_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_answer(question):
    faqs = load_faqs()

    if not faqs:
        return "No college information is available yet."

    training_questions = []
    training_answers = []

    for faq in faqs:

        # Supports both old and new JSON formats
        examples = faq.get("questions", [])

        if not examples and faq.get("question"):
            examples = [faq["question"]]

        for example in examples:
            if example.strip():
                training_questions.append(example)
                training_answers.append(faq["answer"])

    if not training_questions:
        return "No FAQ questions are available."

    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))

        question_vectors = vectorizer.fit_transform(training_questions)

        user_vector = vectorizer.transform([question])

        similarities = cosine_similarity(
            user_vector,
            question_vectors
        )

        best_match = similarities.argmax()
        confidence = similarities[0][best_match]

        if confidence < 0.25:
            return "Sorry, I couldn't find an answer. Please contact the college office."

        return training_answers[best_match]

    except ValueError:
        return "Please add valid questions to the FAQ database."
