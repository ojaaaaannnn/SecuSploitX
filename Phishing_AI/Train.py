import time
from datetime import datetime
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

started_time = datetime.now()
print("Started Training Time :", started_time)


class Train:
    def model(self):
        df = pd.read_csv(
            "phishing_dataset.csv",
            usecols=[0, 1],
            names=["category", "text"],
            header=0,
            quotechar='"',
            on_bad_lines="skip"
        )

        df.to_csv("phishing_dataset_clean.csv", index=False, quoting=1)

        print(f"[INFO] Loaded dataset with {len(df)} rows")

        Pipe_line = Pipeline([
            ('vectorizer', TfidfVectorizer()),
            ('classifier', GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=3,
                subsample=0.8,
                random_state=42
            ))
        ])

        x = df["text"]
        y = df["category"]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=42
        )

        Pipe_line.fit(x_train, y_train)

        y_pred = Pipe_line.predict(x_test)
        print("Accuracy Score :", accuracy_score(y_test, y_pred))
        print("Classification Report :\n", classification_report(y_test, y_pred))

        confusion = confusion_matrix(y_test, y_pred, labels=Pipe_line.classes_)
        plt.figure(figsize=(12, 10))
        sns.heatmap(confusion,
                    annot=True,
                    fmt='d',
                    xticklabels=Pipe_line.classes_,
                    yticklabels=Pipe_line.classes_,
                    cmap="Blues")
        plt.xlabel("Predicted")
        plt.ylabel("True")
        plt.title("Confusion Matrix")
        plt.savefig("Confusion_matrix.png")
        plt.close()

        try:
            joblib.dump(Pipe_line, "model.pkl")
            print("Model saved successfully!")
        except Exception as e:
            print(f"Failed to Save Model : {e}")


if __name__ == "__main__":
    C = Train()
    C.model()

ended_time = datetime.now()
print("Ended Training Time :", ended_time)
