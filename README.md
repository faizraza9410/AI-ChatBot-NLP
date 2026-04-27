# 🤖 NEXUS AI — College Project Backend

## Project Overview
**Chatbot AI** is an intelligent chatbot with a custom NLP engine built using Python Flask.

**Tech Stack:**
- **Backend:** Python 3 + Flask (REST API)
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript  
- **NLP Engine:** Custom Rule-Based NLP (no external ML libraries needed)
- **Knowledge Base:** Pre-trained responses for 20+ categories

---

## ✅ Requirements
- Python 3.8 or higher
- Flask (usually pre-installed, or: `pip install flask`)
- A modern web browser (Chrome, Firefox, Edge)

---

## 🚀 How to Run

### Windows:
```
Double-click START.bat
```
OR open terminal in this folder:
```cmd
python app.py
```

### Mac / Linux:
```bash
chmod +x start.sh
./start.sh
```
OR:
```bash
python3 app.py
```

### Then open your browser at:
```
http://localhost:5000
```

---

## 📁 Project Structure
```
nexus_backend/
├── app.py              ← Main Flask backend (NLP + API)
├── START.bat           ← Windows startup script
├── start.sh            ← Mac/Linux startup script
├── README.md           ← This file
├── templates/
│   └── index.html      ← Frontend UI
└── static/
    └── audio/
        └── genie_a.mp3 ← Place your audio file here
```

---

## 🔌 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Open the chatbot UI |
| POST | `/api/chat` | Send a message, get AI reply + NLP analysis |
| POST | `/api/analyze` | Analyze text only (no reply) |
| GET | `/api/status` | Backend health check |
| GET | `/api/intents` | List all 9 intent categories |
| GET | `/api/knowledge` | Knowledge base statistics |
| GET | `/api/audio/<file>` | Serve audio files |

### Example API Call:
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Write a Java program for even or odd"}'
```

---

## 🧠 NLP Features
1. **Sentiment Analysis** — Positive / Neutral / Negative
2. **Intent Recognition** — 9 categories (Greeting, Code, Question, Creative, Math, etc.)
3. **Emotion Detection** — Joy, Sadness, Anger, Surprise, Fear
4. **Keyword Extraction** — Top keywords from user input
5. **Language Detection** — English, Hindi, Hinglish
6. **Text Complexity** — Simple / Medium / Complex
7. **Token Count** — Approximate token estimation

---

## 📚 Knowledge Base Topics
- Java programs (even/odd, factorial, fibonacci, arrays, strings, OOP)
- Python programs (sorting, basics)
- Artificial Intelligence & Machine Learning
- Natural Language Processing (NLP)
- Data Structures (Stack, Queue, Tree, etc.)
- Database / SQL
- Networking & OSI Model
- Operating Systems
- Web Development
- Mathematics
- Hindi & Indian languages
- Creative writing & stories

---

## 🎤 Audio
Place your `genie_a.mp3` file in:
```
static/audio/genie_a.mp3
```
The 🔊 button in the chat will play it.

---

## 👨‍💻 For the Demo
1. Run `python app.py`
2. Open `http://localhost:5000`
3. Try: "Write a Java program for even or odd"
4. Try: "What is artificial intelligence?"
5. Try: "Explain NLP"
6. Watch the real-time NLP analysis panels update!

---

*Built as a college project to demonstrate AI + NLP integration.*
