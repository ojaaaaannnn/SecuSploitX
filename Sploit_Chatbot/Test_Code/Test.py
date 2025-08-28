import re
import time
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TestChatBot:
    def __init__(self):
        self.model = joblib.load("model.pkl")
        self.data = pd.read_csv("Questions.csv")
        self.vectorizer = TfidfVectorizer()
        self.vectorizer.fit(self.data["question"].values)

    def Test_Model(self):
        print("Sploit ChatBot Loading ...")
        print("Type 'exit' to Quit.")
        try:
            while True:
                user_input = input("Enter Question Here: ").lower()
                if user_input == "exit":
                    print("Exiting ...")
                    break

                resub = re.sub(r"[^\w\s]","",user_input)

                Predicted = self.model.predict([resub])[0]

                user_vec = self.vectorizer.transform([user_input])
                questions_vec = self.vectorizer.transform(self.data["question"].values)
                similarities = cosine_similarity(user_vec, questions_vec).flatten()
                max_sim_idx = similarities.argmax()
                max_sim_score = similarities[max_sim_idx]

                if max_sim_score >= 0.7:
                    answer = self.data["answer"].iloc[max_sim_idx]
                    print("Answer (from similar question):", answer)
                else:
                    print("Answer (predicted by model):", Predicted)

                time.sleep(1)

        except Exception as e:
            print(f"Failed to Generate Answer : {e}")

if __name__ == "__main__":
    C = TestChatBot()
    C.Test_Model()