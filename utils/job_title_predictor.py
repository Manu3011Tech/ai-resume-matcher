import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# 🔧 Train the job title prediction model
def train_job_title_model(dataset_path="ai_resume_matcher/resume_dataset.csv", save_path="model/job_title_model.pkl"):
    df = pd.read_csv(dataset_path)

    if 'Resume' not in df.columns or 'Category' not in df.columns:
        raise ValueError("CSV must contain 'Resume' and 'Category' columns")

    X = df['Resume']
    y = df['Category']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=3000)),
        ('clf', LogisticRegression(max_iter=1000))
    ])

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print("✅ Model Trained with Accuracy:", round(acc * 100, 2), "%")
    print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(model, save_path)

    return model, round(acc * 100, 2)

# 🔮 Predict job title from resume
def predict_job_title(resume_text, model_path="model/job_title_model.pkl"):
    if not os.path.exists(model_path):
        return "⚠️ Model not found. Please train the model first."

    model = joblib.load(model_path)
    prediction = model.predict([resume_text])[0]
    return prediction
# 🧪 Test code
if __name__ == "__main__":
    train_job_title_model()


import joblib
model = joblib.load("model/job_title_model.pkl")
print(model)

     
     
     

