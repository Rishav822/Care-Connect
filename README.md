# 🩺 Care Connect AI

## 📌 Overview

**Care Connect** is an AI-powered conversational assistant designed to provide **basic health information and guidance for common symptoms** through a simple web-based chat interface.

The application combines **Natural Language Processing (NLP)** and a **neural-network-based intent classification model** to understand user messages and return an appropriate response.

> ⚠️ **Medical Disclaimer:** Care Connect is intended for basic health information and assistance only. It is **not a substitute for a qualified medical professional, diagnosis, or emergency medical care**. Users should consult a healthcare professional for medical advice.

---

## ✨ Key Features

- 🤖 **AI Conversational Assistant** for common health-related queries
- 🧠 **Intent Classification** using a neural network
- 🔤 **NLP Processing** with tokenization and lemmatization
- 📚 **Bag-of-Words** text vectorization
- 💬 **Interactive Web Chat Interface**
- ⚡ **Asynchronous communication** between frontend and backend
- 🛡️ **Confidence threshold & fallback responses**
- 📱 **Responsive UI** for desktop and mobile
- 🔒 **Input validation and security considerations**
- 🧩 **Modular three-tier architecture**
- 💾 **Model and vocabulary persistence** using HDF5/Pickle files

---

## 🏗️ System Architecture

Care Connect follows a **three-tier architecture**:

```text
┌─────────────────────────────────────────────┐
│              PRESENTATION LAYER             │
│         HTML • CSS • JavaScript             │
│              💬 Chat Interface              │
└──────────────────────┬──────────────────────┘
                       │ HTTP / JSON
                       ▼
┌─────────────────────────────────────────────┐
│               APPLICATION LAYER             │
│                   Flask                    │
│      NLP • Intent Classification • API      │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                  DATA LAYER                 │
│ TensorFlow/Keras Model • JSON • Pickle     │
│ chatbot_model.h5 • words.pkl • classes.pkl │
└─────────────────────────────────────────────┘
```

The frontend communicates with the Flask backend using HTTP POST requests and JSON data. The backend processes the message through the NLP pipeline, predicts the intent, and generates the corresponding response.

---

## 🧠 How It Works

```text
User Message
     │
     ▼
Text Tokenization
     │
     ▼
Lemmatization
     │
     ▼
Bag-of-Words Vector
     │
     ▼
Neural Network
     │
     ▼
Intent + Confidence Score
     │
     ├── Confidence > 0.25 ──► Matching Response
     │
     └── Confidence ≤ 0.25 ──► Fallback Response
```

### Processing Pipeline

1. The user enters a message in the chat interface.
2. JavaScript sends the message to the Flask `/get_response` endpoint.
3. NLTK tokenizes and lemmatizes the text.
4. The processed text is converted into a Bag-of-Words vector.
5. The trained neural network predicts the user's intent.
6. A confidence threshold of **0.25** is used to determine whether the prediction is reliable.
7. The corresponding response template is selected and returned to the user.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| 🌐 Flask | Web server and REST API |
| 🧠 TensorFlow / Keras | Neural network and model inference |
| 🔤 NLTK | NLP, tokenization and lemmatization |
| 🔢 NumPy | Numerical operations |
| 📦 Pickle | Vocabulary/class data persistence |
| 🧱 HTML5 | Web page structure |
| 🎨 CSS3 | User interface styling |
| ⚡ JavaScript | Chat interaction and API communication |
| 📄 JSON | Intent and response data |

---

## 📂 Project Structure

```text
Care-Connect/
│
├── app.py                  # Flask application server
├── train_model.py          # Model training script
│
├── index.html              # Main web interface
├── style.css               # UI styling
├── script.js               # Frontend interaction
│
├── intents.json            # Intent patterns and responses
├── chatbot_model.h5        # Trained TensorFlow/Keras model
├── words.pkl               # Processed vocabulary
├── classes.pkl             # Intent class names
│
└── README.md               # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd Care-Connect
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask tensorflow nltk numpy
```

### 4. Download NLTK resources

```bash
python -c "import nltk; nltk.download('punkt')"
python -c "import nltk; nltk.download('wordnet')"
```

---

## 🧪 Train the Model

If you want to retrain the chatbot using the intent dataset:

```bash
python train_model.py
```

The training process creates/updates:

```text
chatbot_model.h5
words.pkl
classes.pkl
```

The documented model uses:

- Dense layer: **128 neurons**, ReLU
- Dropout: **0.5**
- Dense layer: **64 neurons**, ReLU
- Dropout: **0.5**
- Output layer: Softmax
- Optimizer: SGD
- Learning rate: `0.01`
- Momentum: `0.9`
- Nesterov: enabled
- Epochs: `200`
- Batch size: `5`

---

## ▶️ Run the Application

Start the Flask development server:

```bash
python app.py
```

Then open the local address shown by Flask in your browser.

---

## 🔌 API

### `POST /get_response`

Processes a user message and returns the chatbot response.

**Request:**

```json
{
  "message": "What should I do if I have a headache?"
}
```

**Response:**

```json
{
  "response": "..."
}
```

The frontend uses JavaScript `fetch()` to asynchronously send the request and display the returned response in the chat interface.

---

## 🔐 Security & Privacy

The system design includes several security considerations:

- Input validation
- Maximum message-length enforcement
- Protection against injection-style attacks
- XSS prevention considerations
- Rate limiting for API endpoints
- Read-only model access during runtime
- Restricted training-data access
- HTTPS recommended for production deployment
- No personal health information is intended to be stored
- Session data is maintained in browser memory

For production deployment, additional security testing and hardening should be performed.

---

## 🚀 Production Deployment

The project documentation recommends a production setup using:

```text
Internet
   │
   ▼
Nginx / Reverse Proxy
   │
   ▼
Gunicorn / WSGI
   │
   ▼
Flask Application
   │
   ▼
ML Model + NLP Pipeline
```

Recommended production considerations include:

- Gunicorn WSGI server
- Nginx reverse proxy
- SSL/TLS certificate
- Environment variables
- Firewall configuration
- Rate limiting
- Security headers
- Regular dependency updates
- Server and model monitoring

---

## 🧪 Testing

The system design defines testing areas including:

- NLP pipeline testing
- Model prediction testing
- API endpoint testing
- Frontend interaction testing
- End-to-end workflow testing
- Cross-browser testing
- Mobile responsiveness testing
- Concurrent-load testing
- Error-handling scenarios

Target requirements documented for the project include **80% minimum code coverage**, with critical paths targeted for **100% coverage**.

---

## 📈 Performance Goals

The documented system targets:

| Metric | Target |
|---|---:|
| UI loading | `< 2 seconds` |
| Average chat processing | `< 1 second` |
| Model inference | `< 500 ms/request` |
| Concurrent users | `100+` |
| Target intent classification accuracy | `> 90%` |

These are **design/acceptance targets**, not a claim that every deployment currently achieves them.

---

## 🔮 Future Improvements

Possible improvements based on the system's scalability and maintenance plan include:

- ➕ Add more health-related intents and training patterns
- 🧠 Improve response quality and model performance
- 🔄 Scheduled model retraining
- 🧪 A/B testing for model improvements
- 📊 Better monitoring and analytics
- ⚡ Model caching and performance optimization
- 🌍 CDN integration for static assets
- 📈 Horizontal scaling with load balancing
- ♿ Further accessibility improvements
- 🔐 Stronger production security controls

---

## 📚 Documentation

The project includes a detailed **System Design Specification (SDS)** covering:

- System architecture
- Component relationships
- NLP processing
- Model training
- Data management
- Security model
- Hardware/software requirements
- Performance requirements
- Error handling
- Deployment
- Testing
- Maintenance

---

## 👨‍💻 Project

**Care Connect AI**  
An academic/educational project focused on applying **Artificial Intelligence, NLP, Machine Learning, and web technologies** to basic health-assistance conversations.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub!

<p align="center">
  <b>Care Connect AI — Connecting users with smarter health assistance 🤖🩺</b>
</p>
