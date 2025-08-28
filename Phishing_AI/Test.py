import re
import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
import joblib

class TestChatBot:
    def __init__(self):
        self.model = joblib.load("model.pkl")

        self.data = pd.read_csv("phishing_dataset_clean.csv")

        self.vectorizer = TfidfVectorizer()
        self.vectorizer.fit(self.data["text"].values)

        self.categories = self.data["category"].unique().tolist()

    def generate_email(self, user_input):
        try:
            resub = re.sub(r"[^\w\s]", "", user_input.lower())
            closest_category, score = process.extractOne(resub, self.categories)
            Predicted = closest_category

            subset = self.data[self.data["category"] == Predicted]
            if subset.empty:
                return "⚠ No matching samples found in dataset!"

            input_vector = self.vectorizer.transform([resub])
            subset_vectors = self.vectorizer.transform(subset["text"].values)
            similarities = cosine_similarity(input_vector, subset_vectors).flatten()
            top_indices = similarities.argsort()[-3:][::-1]
            email_text = subset.iloc[random.choice(top_indices)]["text"]
            return email_text

        except Exception as e:
            return f"❌ Error generating email: {str(e)}"

    def predict_category(self, user_input):
        try:
            resub = re.sub(r"[^\w\s]", "", user_input.lower())
            closest_category, score = process.extractOne(resub, self.categories)
            return closest_category
        except Exception as e:
            return f"❌ Error predicting category: {str(e)}"
