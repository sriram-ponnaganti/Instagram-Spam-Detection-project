# 🛡️ AI-Powered Instagram Spam Detection

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange?style=for-the-badge&logo=scikit-learn)
![NLP](https://img.shields.io/badge/NLP-Text%20Classification-purple?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=for-the-badge&logo=pandas)
![NumPy](https://img.shields.io/badge/Library-NumPy-013243?style=for-the-badge&logo=numpy)

An AI-powered **Instagram spam comment detection system** built with Python and Streamlit. The application uses **Natural Language Processing (NLP)** and Machine Learning to analyze comments and classify them as **SPAM** or **NOT SPAM**, while providing a confidence score for the prediction.

---
<p align="center">
  <img src="stock1.png" alt="SpamGuard AI" width="800">
</p>

<p align="center">
  <img src="stock2.png" alt="SpamGuard AI" width="800">
</p>

<p align="center">
  <img src="stock3.png" alt="SpamGuard AI" width="800">
</p>

## ✨ Features

- 🤖 **AI Spam Detection** — Classifies comments as spam or legitimate.
- 🧠 **NLP-Based Classification** — Converts text into machine-learning features using TF-IDF.
- 📊 **Confidence Score** — Displays the model's prediction confidence.
- ⚡ **Real-Time Prediction** — Analyze comments instantly through the Streamlit dashboard.
- 🎨 **Interactive Dashboard** — Modern, responsive interface designed for an engaging user experience.
- 🔐 **Security-Focused Design** — Built around the concept of social-media comment security.
- 📈 **Prediction Visualization** — Presents classification results and confidence information clearly.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **Streamlit** | Interactive web application |
| **Scikit-learn** | Machine Learning and text classification |
| **TF-IDF** | Text feature extraction |
| **Logistic Regression** | Spam classification |
| **Pandas** | Dataset handling |
| **NumPy** | Numerical operations |

---

## 🧠 How It Works

The application follows an NLP-based classification pipeline:

```text
Instagram Comment
       ↓
Text Preprocessing
       ↓
TF-IDF Vectorization
       ↓
Logistic Regression Model
       ↓
Spam / Not Spam Prediction
       ↓
Confidence Score
```

### Prediction Process

1. The user enters an Instagram comment.
2. The comment is processed and converted into numerical features using **TF-IDF**.
3. The trained **Logistic Regression** model analyzes the generated features.
4. The model predicts whether the comment is **SPAM** or **NOT SPAM**.
5. The application displays the prediction and confidence score.

---

## 🔍 Example

### Input

```text
Congratulations! You won a free prize. Click here to claim now!
```

### Output

```text
Prediction: SPAM
Confidence: High
```

The trained model analyzes the text and determines the most likely classification based on learned patterns from the training data.

---

## 📊 Machine Learning Model

The project uses the following approach:

### TF-IDF Vectorization

**TF-IDF (Term Frequency-Inverse Document Frequency)** converts text comments into numerical feature vectors that can be processed by a machine-learning model.

### Logistic Regression

A **Logistic Regression** classifier is used to determine whether a comment belongs to the spam or non-spam category.

### Probability Prediction

The model also generates class probabilities, which are used to present the prediction confidence in the application.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.9 or later
- Git
- A terminal or command prompt

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/instagram-spam-detection.git
cd instagram-spam-detection
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 📂 Project Structure

```text
instagram-spam-detection/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── spam_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── data/
│   └── raw/
│       └── Youtube01-Psy.csv
│
└── screenshots/
    ├── spam1.png
    ├── spam2.png
    └── spam3.png
```

> **Note:** The screenshot files are optional and can be added later to showcase the application interface.

---

## 📸 Screenshots

Screenshots of the application dashboard and prediction results will be added here.

<!-- Add your screenshots later:

<p align="center">
  <img src="screenshots/spam1.png" alt="Instagram Spam Detection Dashboard" width="850">
</p>

<p align="center">
  <img src="screenshots/spam2.png" alt="Spam Detection Analysis" width="850">
</p>

<p align="center">
  <img src="screenshots/spam3.png" alt="Spam Prediction Result" width="850">
</p>

-->

---

## 🌐 Live Demo

🚀 **Try the deployed application:**

```text
https://YOUR-APP-NAME.streamlit.app/
```

> Replace the URL above with your actual Streamlit deployment URL.

---

## 🎯 Use Cases

This project can be used as a foundation for:

- Detecting promotional spam comments
- Identifying suspicious social-media messages
- Automating basic comment moderation
- Demonstrating NLP text classification
- Learning practical Machine Learning deployment with Streamlit

---

## 🔮 Future Improvements

- Add support for multiple social-media platforms.
- Improve text preprocessing and feature engineering.
- Experiment with advanced NLP models.
- Add bulk comment analysis.
- Add downloadable prediction reports.
- Add model performance metrics and analytics.
- Improve multilingual spam detection.

---

## 👨‍💻 Author

**Sriram Ponnaganti**

B.Tech — Computer Science Engineering (AI/ML)

---

## ⭐ Support

If you found this project useful, consider giving the repository a **star ⭐** on GitHub.
