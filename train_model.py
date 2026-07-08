"""
Train the Fake News Detection Model

This script trains a Passive Aggressive Classifier using TF-IDF vectorization
to classify news articles as fake or real.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import os
import sys

# Create model directory if it doesn't exist
os.makedirs('model', exist_ok=True)

def load_data():
    """
    Load fake and real news datasets
    Expected files: Fake.csv and True.csv in the model/database/model/model/dataset/ directory
    """
    print("🔄 Loading datasets...")
    
    fake_path = 'model/database/model/model/dataset/Fake.csv'
    true_path = 'model/database/model/model/dataset/True.csv'
    
    if not os.path.exists(fake_path) or not os.path.exists(true_path):
        print(f"❌ Dataset files not found!")
        print(f"   Expected: {fake_path}")
        print(f"   Expected: {true_path}")
        print("\n📝 To train the model, download the datasets:")
        print("   1. Get Fake.csv and True.csv from:")
        print("      https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
        print("   2. Place them in: model/database/model/model/dataset/")
        return None
    
    try:
        fake_df = pd.read_csv(fake_path)
        true_df = pd.read_csv(true_path)
        
        print(f"✅ Loaded {len(fake_df)} fake news articles")
        print(f"✅ Loaded {len(true_df)} real news articles")
        
        return fake_df, true_df
    except Exception as e:
        print(f"❌ Error loading datasets: {e}")
        return None

def prepare_data(fake_df, true_df):
    """
    Prepare and combine fake and real news data
    """
    print("\n🔄 Preparing data...")
    
    # Add labels: 0 = Fake, 1 = Real
    fake_df['label'] = 0
    true_df['label'] = 1
    
    # Combine datasets
    df = pd.concat([fake_df, true_df], ignore_index=True)
    
    # Keep only necessary columns and handle missing values
    df = df[['text', 'label']].dropna()
    
    # Shuffle and reset index
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"✅ Total articles: {len(df)}")
    print(f"✅ Fake news: {(df['label'] == 0).sum()}")
    print(f"✅ Real news: {(df['label'] == 1).sum()}")
    
    return df

def train_model(df):
    """
    Train the Passive Aggressive Classifier
    """
    print("\n🔄 Training model...")
    
    X = df['text']
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"✅ Training set: {len(X_train)} articles")
    print(f"✅ Test set: {len(X_test)} articles")
    
    # Vectorize text using TF-IDF
    print("\n🔄 Vectorizing text (TF-IDF)...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        min_df=5,
        max_df=0.7,
        stop_words='english',
        ngram_range=(1, 2)
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"✅ Features extracted: {X_train_vec.shape[1]}")
    
    # Train Passive Aggressive Classifier
    print("\n🔄 Training Passive Aggressive Classifier...")
    model = PassiveAggressiveClassifier(
        max_iter=50,
        random_state=42,
        tol=1e-3,
        early_stopping=True,
        validation_fraction=0.1
    )
    
    model.fit(X_train_vec, y_train)
    print("✅ Model trained successfully")
    
    # Evaluate model
    print("\n📊 Evaluating model...")
    y_pred = model.predict(X_test_vec)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"✅ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"✅ Precision: {precision:.4f}")
    print(f"✅ Recall: {recall:.4f}")
    print(f"✅ F1-Score: {f1:.4f}")
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n📈 Confusion Matrix:")
    print(f"   True Negatives: {cm[0][0]}")
    print(f"   False Positives: {cm[0][1]}")
    print(f"   False Negatives: {cm[1][0]}")
    print(f"   True Positives: {cm[1][1]}")
    
    return model, vectorizer

def save_model(model, vectorizer):
    """
    Save trained model and vectorizer
    """
    print("\n💾 Saving model and vectorizer...")
    
    try:
        joblib.dump(model, 'model/model.pkl')
        joblib.dump(vectorizer, 'model/vectorizer.pkl')
        print("✅ Model saved to: model/model.pkl")
        print("✅ Vectorizer saved to: model/vectorizer.pkl")
        return True
    except Exception as e:
        print(f"❌ Error saving model: {e}")
        return False

def main():
    """
    Main training pipeline
    """
    print("="*60)
    print("🚀 FAKE NEWS DETECTION MODEL TRAINING")
    print("="*60)
    
    # Load data
    result = load_data()
    if result is None:
        sys.exit(1)
    
    fake_df, true_df = result
    
    # Prepare data
    df = prepare_data(fake_df, true_df)
    
    # Train model
    model, vectorizer = train_model(df)
    
    # Save model
    if save_model(model, vectorizer):
        print("\n" + "="*60)
        print("✨ TRAINING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n🎯 Next steps:")
        print("   1. Run the Flask app: python app.py")
        print("   2. Visit http://localhost:5000")
        print("   3. Test the model with news articles")
        print("\n💡 To deploy with Docker:")
        print("   docker-compose up --build")
    else:
        print("\n❌ Training failed to save model")
        sys.exit(1)

if __name__ == "__main__":
    main()
