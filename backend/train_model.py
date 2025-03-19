import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample training data (replace with real dataset)
training_texts = ["I am happy today", "I feel so sad", "This is amazing", "I am angry", "I love this day"]
training_labels = ["happy", "sad", "happy", "angry", "happy"]  # Corresponding emotions

# Convert text to feature vectors
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(training_texts)

# Train model
model = MultinomialNB()
model.fit(X_train, training_labels)

# Save model and vectorizer
joblib.dump(model, "emotion_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model and vectorizer saved successfully!")
