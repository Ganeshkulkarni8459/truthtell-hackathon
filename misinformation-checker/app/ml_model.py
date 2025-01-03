import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load data
true_data = pd.read_csv('./Data/True.csv')
false_data = pd.read_csv('./Data/Fake.csv')
true_data['label'] = 1
false_data['label'] = 0

data = pd.concat([true_data, false_data], ignore_index=True)
data['text'] = data['text'].str.lower()

X = data['text']
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)

model = MultinomialNB()
model.fit(X_train_vectorized, y_train)

def get_misinformation_score(text):
    text_vectorized = vectorizer.transform([text])
    prediction_prob = model.predict_proba(text_vectorized)[0]
    misinformation_score = round(prediction_prob[0] * 100, 2)
    is_misinformation = prediction_prob[0] > 0.5
    return misinformation_score, "Misinformation" if is_misinformation else "True Information"
