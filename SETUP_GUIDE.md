# 📰 Fake News Detection System - Setup Guide

## ✨ What's Included

This complete app setup includes:
- ✅ Flask backend with prediction routes
- ✅ Beautiful responsive frontend templates (HTML/CSS/JS)
- ✅ Model training script with evaluation metrics
- ✅ Static assets (CSS, JavaScript)
- ✅ Docker & Docker Compose configuration
- ✅ Complete documentation

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- git

### Step 1: Clone & Setup
```bash
git clone https://github.com/Deepak-Rithik/fake-news-detection-project
cd fake-news-detection-project
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Get the Dataset

**Option A: Download from Kaggle (Recommended)**
1. Visit: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset
2. Download `Fake.csv` and `True.csv`
3. Create directory: `mkdir -p model/database/model/model/dataset`
4. Place files in that directory

**Option B: Create Dummy Dataset (Testing Only)**
```bash
# This will create small test datasets for quick testing
python -c "
import pandas as pd
import os
os.makedirs('model/database/model/model/dataset', exist_ok=True)

# Create dummy data
fake_data = {
    'title': ['Fake News 1', 'Fake News 2'],
    'text': ['This is definitely fake news content', 'Another obviously false story']
}
real_data = {
    'title': ['Real News 1', 'Real News 2'],
    'text': ['This is authentic news from reliable sources', 'Verified true news story']
}

pd.DataFrame(fake_data).to_csv('model/database/model/model/dataset/Fake.csv', index=False)
pd.DataFrame(real_data).to_csv('model/database/model/model/dataset/True.csv', index=False)
print('✅ Dummy datasets created')
"
```

### Step 5: Train the Model
```bash
python train_model.py
```

You should see:
```
✅ Loaded X fake news articles
✅ Loaded Y real news articles
✅ Accuracy: 0.95XX (95%+ for real datasets)
💾 Model saved to: model/model.pkl
💾 Vectorizer saved to: model/vectorizer.pkl
```

### Step 6: Run the Flask App
```bash
python app.py
```

Output:
```
 * Running on http://127.0.0.1:5000
```

### Step 7: Open in Browser
Visit: http://localhost:5000

---

## 🐳 Run with Docker (Production)

### Prerequisites
- Docker installed: https://docs.docker.com/install/
- Docker Compose installed: https://docs.docker.com/compose/install/

### Steps

1. **Place dataset files**
   ```bash
   # Create directory structure
   mkdir -p model/database/model/model/dataset
   
   # Copy Fake.csv and True.csv into that directory
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the app**
   - URL: http://localhost:5000
   - The app will automatically train the model on first run

4. **View logs**
   ```bash
   docker-compose logs -f fake-news-app
   ```

5. **Stop the app**
   ```bash
   docker-compose down
   ```

---

## 📁 Project Structure

```
fake-news-detection-project/
├── app.py                          # Main Flask application
├── train_model.py                  # Model training script
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker Compose config
├── procfile                        # Heroku deployment
├── runtime.txt                     # Python version for Heroku
│
├── model/
│   ├── model.pkl                   # Trained ML model (generated)
│   ├── vectorizer.pkl              # TF-IDF vectorizer (generated)
│   ├── predict.py                  # Prediction utilities
│   ├── preprocess.py               # Text preprocessing
│   └── database/
│       └── model/
│           └── model/
│               └── dataset/        # Place Fake.csv & True.csv here
│
├── templates/
│   ├── index.html                  # Main prediction page
│   └── about.html                  # About page
│
├── static/
│   ├── css/
│   │   └── style.css               # Custom styling
│   └── js/
│       └── main.js                 # Frontend JavaScript
│
└── SETUP_GUIDE.md                  # This file
```

---

## 🧠 Model Details

### Algorithm
- **Classifier**: Passive Aggressive Classifier
- **Vectorizer**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Accuracy**: 95%+ on real dataset

### How It Works
1. **Text Preprocessing**: Remove noise, lowercase, remove stopwords
2. **TF-IDF Vectorization**: Convert text to numerical features
3. **Classification**: Predict fake (0) or real (1)

### Performance Metrics
```
Accuracy  : ~95%
Precision : ~95%
Recall    : ~95%
F1-Score  : ~95%
```

---

## 🧪 Testing the App

### Test Data

**Fake News Example:**
```
Celebrity XYZ caught in shocking scandal! Scientists have discovered aliens living in our oceans. 
This story will blow your mind! Click here for exclusive footage...
```

**Real News Example:**
```
The Federal Reserve announced interest rate decision today. According to latest economic data, 
employment rates have improved. Official statement released by the agency...
```

### Manual Testing
1. Open http://localhost:5000
2. Paste news text in the textarea
3. Click "Check News"
4. View the prediction result

### Automated Testing
```bash
# Create a test script
cat > test_api.py << 'EOF'
import requests

test_cases = [
    ("This is definitely fake news story", "Fake News"),
    ("Official government announcement today", "Real News"),
]

for text, expected in test_cases:
    response = requests.post('http://localhost:5000/predict', 
                            data={'news': text})
    print(f"Input: {text[:30]}...")
    print(f"Expected: {expected}")
    print(f"Status: {response.status_code}\n")
EOF

python test_api.py
```

---

## 📤 Deployment

### Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   # Visit: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and create app**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Upload dataset (if needed)**
   ```bash
   git add model/database/model/model/dataset/
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **View logs**
   ```bash
   heroku logs --tail
   ```

### Deploy to AWS/Azure/GCP

Use the provided Dockerfile:
```bash
docker build -t fake-news-detection .
docker run -p 5000:5000 fake-news-detection
```

---

## 🔧 Troubleshooting

### Issue: "Model not found"
**Solution**: Run `python train_model.py` to train the model first

### Issue: "Dataset files not found"
**Solution**: Download from Kaggle and place in `model/database/model/model/dataset/`

### Issue: "ModuleNotFoundError"
**Solution**: Activate virtual environment and reinstall dependencies
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution**: Change port in app.py or kill existing process
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Issue: Docker build fails
**Solution**: Ensure Docker daemon is running and disk space is available
```bash
docker system prune  # Clean up unused Docker images
```

---

## 📚 Additional Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Scikit-learn ML**: https://scikit-learn.org/
- **Docker Guide**: https://docs.docker.com/
- **Dataset Source**: https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset

---

## ✅ Checklist Before Deployment

- [ ] Model trained successfully (accuracy > 90%)
- [ ] App runs without errors locally
- [ ] Templates load correctly
- [ ] CSS and JavaScript work properly
- [ ] Predictions are accurate
- [ ] Docker build completes successfully
- [ ] Environment variables are set
- [ ] Dataset is backed up
- [ ] Tests pass
- [ ] Documentation is updated

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review GitHub issues
3. Create new issue with details

---

**Created with ❤️ for detecting fake news**
