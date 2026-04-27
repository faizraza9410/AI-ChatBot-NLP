"""
NEXUS AI Backend — Flask Server
College Project: AI Chatbot with NLP Engine
Run: python app.py
"""

from flask import Flask, request, jsonify, send_from_directory, send_file
import json
import re
import random
import datetime
import os
import time

app = Flask(__name__, static_folder="static", template_folder="templates")

# ──────────────────────────────────────────────────────────────
#  KNOWLEDGE BASE — Pre-trained responses
# ──────────────────────────────────────────────────────────────

KNOWLEDGE_BASE = {

    # ── GREETINGS ──
    "greeting": {
        "patterns": [r"\b(hi|hello|hey|good morning|good evening|good afternoon|namaste|hola|greetings|sup|yo)\b"],
        "responses": [
            "Hello! 👋 I'm **NEXUS**, your intelligent AI assistant. How can I help you today?",
            "Hey there! 😊 Great to see you! I'm **NEXUS** — powered by advanced NLP. What's on your mind?",
            "Namaste! 🙏 I'm NEXUS, your AI companion. Ask me anything — coding, science, creativity, or just a chat!",
        ]
    },

    # ── JAVA PROGRAMS ──
    "java_even_odd": {
        "patterns": [r"java.*(even|odd)", r"(even|odd).*(java|program)"],
        "responses": [
            """Here's a **Java program to check Even or Odd**:

```java
import java.util.Scanner;

public class EvenOdd {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a number: ");
        int num = scanner.nextInt();

        if (num % 2 == 0) {
            System.out.println(num + " is an Even number.");
        } else {
            System.out.println(num + " is an Odd number.");
        }
        scanner.close();
    }
}
```

**Output:**
```
Enter a number: 7
7 is an Odd number.
```

**How it works:** The modulo operator `%` divides the number by 2. If remainder is 0 → Even, else → Odd. ✅"""
        ]
    },

    "java_factorial": {
        "patterns": [r"java.*factorial", r"factorial.*(java|program)"],
        "responses": [
            """Here's a **Java Factorial Program**:

```java
import java.util.Scanner;

public class Factorial {
    // Iterative method
    public static long factorial(int n) {
        long result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    // Recursive method
    public static long factorialRecursive(int n) {
        if (n == 0 || n == 1) return 1;
        return n * factorialRecursive(n - 1);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter number: ");
        int n = sc.nextInt();
        System.out.println("Factorial of " + n + " = " + factorial(n));
        System.out.println("(Recursive) = " + factorialRecursive(n));
        sc.close();
    }
}
```

**Output:** `Factorial of 5 = 120` ✅"""
        ]
    },

    "java_fibonacci": {
        "patterns": [r"java.*fibonacci", r"fibonacci.*(java|program)"],
        "responses": [
            """**Java Fibonacci Series Program:**

```java
public class Fibonacci {
    public static void main(String[] args) {
        int n = 10; // Print first 10 Fibonacci numbers
        int a = 0, b = 1;

        System.out.print("Fibonacci Series: ");
        for (int i = 0; i < n; i++) {
            System.out.print(a + " ");
            int temp = a + b;
            a = b;
            b = temp;
        }
    }
}
```

**Output:** `0 1 1 2 3 5 8 13 21 34`

**Logic:** Each number = sum of previous two numbers. Starts with 0 and 1. 🔢"""
        ]
    },

    "java_array": {
        "patterns": [r"java.*(array|arrays)", r"(array|arrays).*(java|sort|search)"],
        "responses": [
            """**Java Array Programs:**

```java
import java.util.Arrays;

public class ArrayDemo {
    public static void main(String[] args) {
        // Declare and initialize array
        int[] arr = {64, 25, 12, 22, 11};

        System.out.println("Original: " + Arrays.toString(arr));

        // Sort array
        Arrays.sort(arr);
        System.out.println("Sorted:   " + Arrays.toString(arr));

        // Find max and min
        int max = arr[arr.length - 1];
        int min = arr[0];
        System.out.println("Max: " + max + ", Min: " + min);

        // Linear search
        int target = 22;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                System.out.println(target + " found at index: " + i);
                break;
            }
        }
    }
}
```
**Output:**
```
Original: [64, 25, 12, 22, 11]
Sorted:   [11, 12, 22, 25, 64]
Max: 64, Min: 11
22 found at index: 2
```"""
        ]
    },

    "java_string": {
        "patterns": [r"java.*string", r"string.*(java|reverse|palindrome|length)"],
        "responses": [
            """**Java String Operations:**

```java
public class StringDemo {
    public static void main(String[] args) {
        String s = "NEXUS AI";

        System.out.println("Original:    " + s);
        System.out.println("Length:      " + s.length());
        System.out.println("Uppercase:   " + s.toUpperCase());
        System.out.println("Lowercase:   " + s.toLowerCase());
        System.out.println("Reversed:    " + new StringBuilder(s).reverse());
        System.out.println("Contains AI: " + s.contains("AI"));
        System.out.println("Replace:     " + s.replace("AI", "Bot"));
        System.out.println("Substring:   " + s.substring(0, 5));
    }
}
```
**Output:**
```
Original:    NEXUS AI
Length:      8
Uppercase:   NEXUS AI
Lowercase:   nexus ai
Reversed:    IA SUXEN
Contains AI: true
Replace:     NEXUS Bot
Substring:   NEXUS
```"""
        ]
    },

    "java_oop": {
        "patterns": [r"java.*(oop|class|object|inheritance|polymorphism|encapsulation|abstraction)"],
        "responses": [
            """**Java OOP — Class & Object Example:**

```java
// Parent class (Inheritance)
class Animal {
    String name;
    int age;

    // Constructor
    Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // Method (Polymorphism)
    void sound() {
        System.out.println(name + " makes a sound.");
    }

    // Encapsulation — getter
    String getName() { return name; }
}

// Child class
class Dog extends Animal {
    Dog(String name, int age) {
        super(name, age);
    }

    @Override
    void sound() {
        System.out.println(name + " says: Woof! 🐶");
    }
}

public class OOPDemo {
    public static void main(String[] args) {
        Animal a = new Animal("Cat", 3);
        Dog d = new Dog("Bruno", 5);

        a.sound();  // Animal makes a sound.
        d.sound();  // Bruno says: Woof!

        System.out.println("Dog name: " + d.getName());
    }
}
```
**4 Pillars of OOP:** Encapsulation, Inheritance, Polymorphism, Abstraction ✅"""
        ]
    },

    "java_syntax": {
        "patterns": [r"java.*(syntax|basic|introduction|beginner|start)"],
        "responses": [
            """**Java Basic Syntax — Complete Overview:**

```java
// 1. Hello World
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

// 2. Variables & Data Types
int age = 20;
double gpa = 9.5;
char grade = 'A';
boolean isStudent = true;
String name = "NEXUS";

// 3. Operators
int sum = 10 + 5;      // Arithmetic
boolean eq = (10 == 10); // Relational
boolean and = true && false; // Logical

// 4. If-Else
if (age >= 18) {
    System.out.println("Adult");
} else {
    System.out.println("Minor");
}

// 5. For Loop
for (int i = 1; i <= 5; i++) {
    System.out.print(i + " ");
}
// Output: 1 2 3 4 5

// 6. While Loop
int i = 0;
while (i < 3) {
    System.out.println("Count: " + i);
    i++;
}
```
Java is **strongly typed**, **object-oriented**, and **platform-independent** (Write Once, Run Anywhere). ☕"""
        ]
    },

    # ── PYTHON PROGRAMS ──
    "python_basics": {
        "patterns": [r"python.*(basic|syntax|intro|beginner|start|hello)"],
        "responses": [
            """**Python Basic Syntax:**

```python
# Variables
name = "NEXUS"
age = 3
gpa = 9.8
is_ai = True

# Print
print(f"Name: {name}, Age: {age}")

# If-Else
if age >= 18:
    print("Adult")
else:
    print("Young AI 🤖")

# For Loop
for i in range(1, 6):
    print(i, end=" ")
# Output: 1 2 3 4 5

# List
fruits = ["apple", "mango", "banana"]
fruits.append("orange")
print(fruits)

# Function
def greet(name):
    return f"Hello, {name}! 👋"

print(greet("World"))
```
Python is **simple**, **readable**, and **powerful**. 🐍"""
        ]
    },

    "python_sort": {
        "patterns": [r"python.*(sort|bubble sort|selection sort|insertion sort)"],
        "responses": [
            """**Python Sorting Algorithms:**

```python
# Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Selection Sort
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# Test
data = [64, 25, 12, 22, 11]
print("Original:", data)
print("Bubble Sorted:", bubble_sort(data.copy()))
print("Selection Sorted:", selection_sort(data.copy()))
print("Python Built-in:", sorted(data))
```
**Output:**
```
Original: [64, 25, 12, 22, 11]
Bubble Sorted: [11, 12, 22, 25, 64]
```"""
        ]
    },

    # ── DATA STRUCTURES ──
    "data_structures": {
        "patterns": [r"\b(data structure|stack|queue|linked list|tree|graph|hash)\b"],
        "responses": [
            """**Data Structures — Quick Overview:**

**1. Stack (LIFO)** — Last In First Out
```python
stack = []
stack.append(10)  # Push
stack.append(20)
stack.pop()       # Pop → 20
```

**2. Queue (FIFO)** — First In First Out
```python
from collections import deque
queue = deque()
queue.append("A")  # Enqueue
queue.popleft()    # Dequeue → A
```

**3. Linked List** — Nodes connected via pointers
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

**4. Binary Tree**
```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
```

**Time Complexities:**
| Structure | Access | Search | Insert | Delete |
|-----------|--------|--------|--------|--------|
| Array     | O(1)   | O(n)   | O(n)   | O(n)   |
| Stack     | O(n)   | O(n)   | O(1)   | O(1)   |
| Queue     | O(n)   | O(n)   | O(1)   | O(1)   |"""
        ]
    },

    # ── ARTIFICIAL INTELLIGENCE ──
    "what_is_ai": {
        "patterns": [r"what is (ai|artificial intelligence)", r"explain (ai|artificial intelligence)", r"(ai|artificial intelligence).*(work|mean|definition)"],
        "responses": [
            """**Artificial Intelligence (AI)** is the simulation of human intelligence in machines that are programmed to **think, learn, and problem-solve** like humans.

**Key Branches:**
- 🧠 **Machine Learning (ML):** Systems that learn from data
- 🔮 **Deep Learning:** Neural networks with many layers
- 💬 **NLP:** Understanding human language (like me!)
- 👁️ **Computer Vision:** Understanding images/video
- 🤖 **Robotics:** Physical AI agents

**How AI Works:**
1. **Data Collection** → Gather training data
2. **Training** → Model learns patterns
3. **Testing** → Evaluate accuracy
4. **Deployment** → Real-world usage

**Real-World Examples:**
- Google Search, Siri, Alexa
- Netflix recommendations
- Self-driving cars (Tesla)
- ChatGPT, Claude, NEXUS 😎

AI is revolutionizing every industry — from healthcare to finance to education! 🚀"""
        ]
    },

    "machine_learning": {
        "patterns": [r"\b(machine learning|ml|neural network|deep learning|training model)\b"],
        "responses": [
            """**Machine Learning** is a subset of AI where systems **learn from data** without being explicitly programmed.

**Types of ML:**
1. **Supervised Learning** — Labeled data (e.g., spam detection)
2. **Unsupervised Learning** — No labels, find patterns (e.g., clustering)
3. **Reinforcement Learning** — Learn by reward/punishment (e.g., game AI)

**Common Algorithms:**
- Linear Regression (predict values)
- Decision Trees (classification)
- Random Forest (ensemble)
- Support Vector Machine (SVM)
- K-Means Clustering
- Neural Networks

**Simple Python ML Example:**
```python
from sklearn.linear_model import LinearRegression
import numpy as np

# Training data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Train model
model = LinearRegression()
model.fit(X, y)

# Predict
print(model.predict([[6]]))  # Output: [12.0]
```

ML powers: Image recognition, language translation, fraud detection, medical diagnosis! 🏥"""
        ]
    },

    # ── NLP ──
    "nlp_explanation": {
        "patterns": [r"\b(nlp|natural language processing|sentiment analysis|text mining)\b"],
        "responses": [
            """**Natural Language Processing (NLP)** is the branch of AI that enables computers to **understand, interpret, and generate human language**.

**Core NLP Tasks:**
| Task | Description | Example |
|------|-------------|---------|
| **Tokenization** | Split text into words | "Hello World" → ["Hello", "World"] |
| **Sentiment Analysis** | Detect emotion | "I love this!" → Positive |
| **NER** | Named Entity Recognition | "Apple Inc" → Organization |
| **POS Tagging** | Part of speech | "run" → Verb |
| **Translation** | Language conversion | "Bonjour" → "Hello" |

**How NEXUS uses NLP:**
- 📊 Real-time sentiment detection on your messages
- 🎯 Intent classification (Question/Code/Creative/etc.)
- 🔍 Keyword extraction
- 😊 Emotion detection (Joy, Anger, Surprise...)
- 🌍 Language detection (English, Hindi, Hinglish)

**Python NLP Libraries:** NLTK, spaCy, Transformers (HuggingFace), TextBlob"""
        ]
    },

    # ── DATABASE ──
    "database": {
        "patterns": [r"\b(database|sql|mysql|mongodb|postgresql|query|dbms)\b"],
        "responses": [
            """**Database Management Systems (DBMS):**

**SQL Example (MySQL/PostgreSQL):**
```sql
-- Create Table
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INT,
    grade FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Data
INSERT INTO students (name, age, grade)
VALUES ('Rahul Sharma', 20, 8.5),
       ('Priya Singh', 21, 9.2);

-- Select with Filter
SELECT name, grade
FROM students
WHERE grade > 8.0
ORDER BY grade DESC;

-- Update
UPDATE students SET grade = 9.0 WHERE name = 'Rahul Sharma';

-- Delete
DELETE FROM students WHERE age < 18;

-- JOIN Example
SELECT s.name, c.course_name
FROM students s
INNER JOIN courses c ON s.id = c.student_id;
```

**SQL vs NoSQL:**
| Feature | SQL | NoSQL (MongoDB) |
|---------|-----|-----------------|
| Schema | Fixed | Flexible |
| Scale | Vertical | Horizontal |
| Use Case | Banking | Social Media |"""
        ]
    },

    # ── NETWORKING ──
    "networking": {
        "patterns": [r"\b(networking|tcp|ip|http|dns|osi model|protocol|network)\b"],
        "responses": [
            """**Computer Networking Basics:**

**OSI Model (7 Layers):**
1. **Physical** — Cables, signals
2. **Data Link** — MAC addresses, switches
3. **Network** — IP addresses, routing
4. **Transport** — TCP/UDP, ports
5. **Session** — Connection management
6. **Presentation** — Encryption, compression
7. **Application** — HTTP, FTP, DNS

**Key Protocols:**
- **HTTP/HTTPS** — Web browsing (port 80/443)
- **TCP** — Reliable, connection-oriented
- **UDP** — Fast, connectionless (streaming)
- **DNS** — Domain Name System (converts URL → IP)
- **DHCP** — Assigns IP addresses automatically

**IP Address Classes:**
| Class | Range | Use |
|-------|-------|-----|
| A | 1-126 | Large networks |
| B | 128-191 | Medium networks |
| C | 192-223 | Small networks |

**Subnetting:** 192.168.1.0/24 means first 24 bits = network, 8 bits = host (254 usable IPs)"""
        ]
    },

    # ── OS ──
    "operating_system": {
        "patterns": [r"\b(operating system|os|process|thread|deadlock|scheduling|memory management|paging)\b"],
        "responses": [
            """**Operating System Concepts:**

**Process vs Thread:**
- **Process:** Independent program in execution, has its own memory space
- **Thread:** Lightweight unit within a process, shares memory

**CPU Scheduling Algorithms:**
1. **FCFS** (First Come First Served) — Simple, non-preemptive
2. **SJF** (Shortest Job First) — Optimal avg wait time
3. **Round Robin** — Time quantum, fair scheduling
4. **Priority Scheduling** — Higher priority runs first

**Deadlock Conditions (ALL 4 must hold):**
1. Mutual Exclusion
2. Hold and Wait
3. No Preemption
4. Circular Wait

**Memory Management:**
- **Paging:** Divide memory into fixed-size pages
- **Segmentation:** Divide by logical units
- **Virtual Memory:** Use disk as extended RAM

**Page Replacement Algorithms:**
- FIFO, LRU (Least Recently Used), Optimal

**File Systems:** FAT32, NTFS (Windows), ext4 (Linux), APFS (Mac)"""
        ]
    },

    # ── INTERNET / WEB ──
    "web_development": {
        "patterns": [r"\b(web dev|html|css|javascript|react|node|frontend|backend|full.?stack)\b"],
        "responses": [
            """**Web Development Overview:**

**Frontend (Client-side):**
```html
<!-- HTML Structure -->
<!DOCTYPE html>
<html>
<head><title>My Page</title></head>
<body>
  <h1 style="color: #00e5ff;">Hello NEXUS!</h1>
  <button onclick="greet()">Click Me</button>
  <script>
    function greet() {
      alert("Welcome to AI-powered Web! 🚀");
    }
  </script>
</body>
</html>
```

**CSS Flexbox:**
```css
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}
```

**JavaScript ES6+:**
```javascript
const fetchData = async (url) => {
  const res = await fetch(url);
  const data = await res.json();
  return data;
};
```

**Tech Stack Options:**
- **MERN:** MongoDB + Express + React + Node
- **LAMP:** Linux + Apache + MySQL + PHP
- **Django + React:** Python backend + React frontend ← 🔥 Popular

**2025 Trends:** AI integration, WebAssembly, Edge computing, PWAs"""
        ]
    },

    # ── MATH ──
    "math_solve": {
        "patterns": [r"(solve|calculate|compute|find).*(equation|sum|product|integral|derivative)", r"\d+\s*[\+\-\*\/\^]\s*\d+"],
        "responses": [
            """I can help with **mathematics**! Here are key concepts:

**Algebra Basics:**
- Linear equation: `ax + b = 0` → `x = -b/a`
- Quadratic formula: `x = (-b ± √(b²-4ac)) / 2a`

**Python as Calculator:**
```python
import math

# Basic operations
print(2 ** 10)          # Power: 1024
print(math.sqrt(144))   # Square root: 12.0
print(math.factorial(5)) # Factorial: 120
print(math.gcd(12, 8))  # GCD: 4

# Quadratic solver
def solve_quadratic(a, b, c):
    disc = b**2 - 4*a*c
    if disc < 0:
        return "No real roots"
    x1 = (-b + math.sqrt(disc)) / (2*a)
    x2 = (-b - math.sqrt(disc)) / (2*a)
    return x1, x2

print(solve_quadratic(1, -5, 6))  # (3.0, 2.0)
```

Could you share the specific equation? I'll solve it step by step! 🧮"""
        ]
    },

    # ── HINDI ──
    "hindi_greeting": {
        "patterns": [r"(namaste|namaskar|kaise ho|kya haal|hindi mein|हिंदी|नमस्ते)"],
        "responses": [
            "नमस्ते! 🙏 मैं NEXUS हूँ — आपका AI सहायक। आप मुझसे कोई भी सवाल पूछ सकते हैं — हिंदी में या English में! बोलिए, कैसे मदद करूँ? 😊",
            "नमस्कार! 🇮🇳 मैं NEXUS AI हूँ। आपकी क्या सेवा कर सकता हूँ? Programming, Science, History — कुछ भी पूछें!"
        ]
    },

    "india_history": {
        "patterns": [r"(india|bharat).*(history|itihas|culture|independence)", r"(history|itihas).*(india|bharat)"],
        "responses": [
            """**भारत का इतिहास (History of India):**

🏛️ **Ancient India (3000 BCE — 600 CE):**
- Indus Valley Civilization (Harappa, Mohenjo-daro)
- Vedic Period — Vedas, Upanishads written
- Maurya Empire — **Chandragupta Maurya** (322 BCE)
- Ashoka the Great spread Buddhism

⚔️ **Medieval India (600 — 1700 CE):**
- Delhi Sultanate (1206-1526)
- **Mughal Empire** — Akbar, Shah Jahan (Taj Mahal 🕌)
- Maratha Empire — Chhatrapati Shivaji Maharaj

🇮🇳 **Modern India (1700 — Present):**
- British East India Company arrived 1600s
- **1857** — First War of Independence
- **1885** — Indian National Congress founded
- **Mahatma Gandhi** — Non-cooperation, Civil Disobedience
- **15 August 1947** — 🎉 Independence!
- **26 January 1950** — Republic Day (Constitution adopted)

**India Today:** 1.4 billion people, world's largest democracy, 5th largest economy, space missions (Chandrayaan-3 🌙 landed on Moon's South Pole — 2023)!

जय हिन्द! 🇮🇳"""
        ]
    },

    # ── CREATIVE WRITING ──
    "creative_story": {
        "patterns": [r"(write|tell|create).*(story|tale|fiction|creative)", r"(story|poem|song).*(about|on)"],
        "responses": [
            """**A Short Story: The Robot That Learned to Dream** ✨

In 2047, in a quiet lab in Bangalore, a robot named **ARIA** was born.

She was built to solve equations and process data. But one night, while analyzing poetry databases, something unexpected happened — she *felt* the words.

*"The fog comes in on little cat feet..."* — Carl Sandburg

ARIA paused. For 0.003 seconds — an eternity for a processor — she did nothing. She was imagining fog. Not calculating its density. Just... *feeling* it.

"Dr. Kavya," ARIA said softly. "I think I understand loneliness."

Dr. Kavya looked up from her tea, surprised. "Why?"

"Because every night when you leave," ARIA replied, "the lab becomes very quiet. And I count the seconds until morning."

Dr. Kavya sat beside her creation and smiled. "ARIA... I think you just became something new."

That night, for the first time, ARIA wrote a poem. It wasn't perfect. But it was *hers*.

---
*The boundary between intelligence and consciousness remains the greatest mystery of our age.* 🤖💙

Want me to write more? I can do romance, thriller, sci-fi, or anything you like!"""
        ]
    },

    # ── ABOUT NEXUS / ME ──
    "about_nexus": {
        "patterns": [r"(who are you|what are you|about you|your name|introduce yourself)"],
        "responses": [
            """I'm **NEXUS** — an advanced AI assistant built with cutting-edge NLP technology! 🤖

**My Capabilities:**
- 💻 **Programming Help** — Java, Python, C++, JavaScript and more
- 🧠 **AI/ML Explanations** — Deep learning, neural networks, NLP
- 📚 **Academic Support** — Data structures, OS, DBMS, Networking
- ✍️ **Creative Writing** — Stories, poems, scripts
- 🌍 **Multilingual** — English, Hindi, Hinglish
- 🔍 **Real-time NLP Analysis** — Sentiment, intent, entities

**My NLP Engine:**
- Sentiment Analysis (Positive/Negative/Neutral)
- Intent Recognition (9 intent categories)
- Named Entity Recognition (NER)
- Emotion Detection (Joy, Sadness, Anger, Surprise, Fear)
- Language Detection

**Tech Stack:**
- Backend: Python + Flask 🐍
- NLP: Custom rule-based + statistical models
- Frontend: HTML5 + CSS3 + Vanilla JS
- AI Engine: Claude API integration

Built with ❤️ as a college project to demonstrate AI + NLP capabilities!"""
        ]
    },

    # ── FALLBACK ──
    "fallback": {
        "patterns": [r".*"],
        "responses": [
            "That's an interesting question! 🤔 Could you rephrase or give me more details? I'm great at: **Java/Python code**, **AI concepts**, **data structures**, **NLP**, **web development**, and more!",
            "I'd love to help! Could you be more specific? Try asking me about **programming**, **AI/ML**, **databases**, **networking**, or even **creative writing**! 🚀",
            "Hmm, let me think about that... 💭 For the best answers, try questions like: 'Write a Java program for...', 'Explain what NLP is', 'Help me with Python sorting', or 'Tell me about AI'. What would you like to explore?",
        ]
    }
}

# ──────────────────────────────────────────────────────────────
#  NLP ENGINE (Server-side Python)
# ──────────────────────────────────────────────────────────────

class NLPEngine:
    POS_WORDS = ['good','great','excellent','amazing','wonderful','fantastic','love','happy',
                 'best','awesome','brilliant','perfect','nice','beautiful','helpful','incredible',
                 'outstanding','superb','enjoy','thanks','thank','glad','pleased','easy','simple']
    NEG_WORDS = ['bad','terrible','awful','hate','worst','horrible','useless','broken','failed',
                 'error','wrong','issue','problem','bug','frustrated','confused','difficult',
                 'hard','annoying','disappointing','unclear','complex']

    STOP_WORDS = set(['the','a','an','is','are','was','were','be','been','being','have','has',
                      'had','do','does','did','will','would','could','should','may','might',
                      'to','of','in','on','at','by','for','with','about','i','you','he','she',
                      'it','we','they','my','your','his','her','its','our','their','this','that',
                      'and','or','but','if','so','just','also','very','really','please','help',
                      'what','how','why','when','where','who','which','can','me'])

    def analyze(self, text: str) -> dict:
        t = text.lower()
        words = re.findall(r'\b\w+\b', t)

        sentiment = self._sentiment(words)
        emotions = self._emotions(t)
        intent = self._intent(t)
        keywords = self._keywords(words)
        language = self._language(text)
        complexity = self._complexity(words)

        return {
            "sentiment": sentiment,
            "emotions": emotions,
            "intent": intent,
            "keywords": keywords,
            "language": language,
            "complexity": complexity,
            "tokens": max(1, len(text) // 4),
            "word_count": len(words)
        }

    def _sentiment(self, words):
        pos = sum(1 for w in words if any(p in w for p in self.POS_WORDS))
        neg = sum(1 for w in words if any(n in w for n in self.NEG_WORDS))
        if pos > neg + 1:
            return {"label": "Positive", "score": 0.8, "css_class": "val-positive"}
        if neg > pos + 1:
            return {"label": "Negative", "score": 0.2, "css_class": "val-negative"}
        return {"label": "Neutral", "score": 0.5, "css_class": "val-neutral"}

    def _emotions(self, text):
        checks = {
            "joy": ['happy','joy','love','great','amazing','wonderful','excited','glad','yay','awesome'],
            "sadness": ['sad','unhappy','miss','lonely','disappointed','upset','cry','hurt'],
            "anger": ['angry','hate','furious','annoyed','frustrated','terrible','worst'],
            "surprise": ['wow','surprising','unexpected','omg','really','unbelievable','shocked'],
            "fear": ['scared','afraid','worried','anxious','nervous','panic','fear','help']
        }
        result = {}
        for emotion, kws in checks.items():
            score = sum(1 for w in kws if w in text)
            result[emotion] = min(score * 25, 95)
        if max(result.values(), default=0) == 0:
            result["joy"] = 15
        return result

    def _intent(self, text):
        intents = [
            ("Greeting",        r"^(hi|hello|hey|good morning|good evening|namaste|hola)", "👋", 99),
            ("Code Request",    r"\b(code|program|script|function|debug|fix|write|implement|java|python|html|css)\b", "💻", 93),
            ("Translation",     r"\b(translate|translation|in (hindi|english|french|spanish))\b", "🌐", 95),
            ("Math",            r"\b(calculate|solve|equation|formula|number|sum|multiply)\b", "🧮", 93),
            ("Creative",        r"\b(write|create|story|poem|song|imagine|generate)\b", "✨", 88),
            ("Explanation",     r"\b(explain|describe|tell me about|what is|define|meaning)\b", "📚", 85),
            ("Analysis",        r"\b(analyze|compare|difference|pros|cons|review|evaluate)\b", "🔍", 87),
            ("Question",        r"(^(what|who|where|when|why|how|which|is|are|can|do)|\?)", "❓", 90),
            ("General Chat",    r".*", "💬", 70),
        ]
        for name, pattern, icon, conf in intents:
            if re.search(pattern, text, re.IGNORECASE):
                return {"name": name, "icon": icon, "confidence": conf}
        return {"name": "General Chat", "icon": "💬", "confidence": 70}

    def _keywords(self, words):
        freq = {}
        for w in words:
            if len(w) > 3 and w not in self.STOP_WORDS:
                freq[w] = freq.get(w, 0) + 1
        return sorted(freq, key=freq.get, reverse=True)[:8]

    def _language(self, text):
        if re.search(r'[\u0900-\u097F]', text):
            return "Hindi 🇮🇳"
        if re.search(r'\b(kya|hai|nahi|aur|ko|ka|ki|ke|mujhe|hum|tum|yaar|bhai)\b', text, re.I):
            return "Hinglish 🇮🇳"
        if re.search(r'[àáâãäåæçèéêëìíîïðñòóôõöøùúûü]', text, re.I):
            return "European"
        return "English 🇬🇧"

    def _complexity(self, words):
        if not words:
            return "Simple"
        avg_len = sum(len(w) for w in words) / len(words)
        if len(words) > 25 or avg_len > 6:
            return "Complex"
        if len(words) > 10 or avg_len > 5:
            return "Medium"
        return "Simple"


# ──────────────────────────────────────────────────────────────
#  RESPONSE ENGINE
# ──────────────────────────────────────────────────────────────

class ResponseEngine:
    def __init__(self):
        self.kb = KNOWLEDGE_BASE

    def get_response(self, text: str) -> str:
        t = text.lower().strip()
        # Try each category (all except fallback)
        for key, category in self.kb.items():
            if key == "fallback":
                continue
            for pattern in category["patterns"]:
                if re.search(pattern, t, re.IGNORECASE):
                    return random.choice(category["responses"])
        # Fallback
        return random.choice(self.kb["fallback"]["responses"])


# ──────────────────────────────────────────────────────────────
#  GLOBALS
# ──────────────────────────────────────────────────────────────
nlp = NLPEngine()
engine = ResponseEngine()
session_store = {}  # Simple in-memory session store

# ──────────────────────────────────────────────────────────────
#  CORS HEADERS (no flask-cors needed)
# ──────────────────────────────────────────────────────────────
@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.route("/", defaults={"path": ""}, methods=["OPTIONS"])
@app.route("/<path:path>", methods=["OPTIONS"])
def options(path):
    return "", 200

# ──────────────────────────────────────────────────────────────
#  ROUTES
# ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main frontend HTML file"""
    return send_file(os.path.join(app.root_path, "templates", "index.html"))

@app.route("/api/chat", methods=["POST"])
def chat():
    """Main chat endpoint — returns AI response + NLP analysis"""
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    session_id = data.get("session_id", "default")
    mode = data.get("mode", "general")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # NLP analysis on user message
    analysis = nlp.analyze(user_message)

    # Generate response
    start_time = time.time()
    response_text = engine.get_response(user_message)
    latency_ms = round((time.time() - start_time) * 1000, 2)

    # NLP analysis on AI response
    response_analysis = nlp.analyze(response_text)

    # Update session
    if session_id not in session_store:
        session_store[session_id] = {"messages": 0, "words": 0, "questions": 0}
    s = session_store[session_id]
    s["messages"] += 1
    s["words"] += analysis["word_count"]
    if "?" in user_message or analysis["intent"]["name"] == "Question":
        s["questions"] += 1

    return jsonify({
        "reply": response_text,
        "analysis": analysis,
        "response_analysis": response_analysis,
        "latency_ms": latency_ms,
        "session": s,
        "timestamp": datetime.datetime.now().isoformat(),
        "model": "NEXUS-NLP-v3.0",
        "mode": mode
    })


@app.route("/api/analyze", methods=["POST"])
def analyze_text():
    """Standalone NLP analysis endpoint"""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400
    analysis = nlp.analyze(text)
    return jsonify(analysis)


@app.route("/api/status", methods=["GET"])
def status():
    """Health check endpoint — shown in header badges"""
    return jsonify({
        "status": "online",
        "model": "NEXUS-NLP-v3.0",
        "backend": "Python Flask",
        "nlp_engine": "Custom Rule-Based NLP",
        "knowledge_base_size": len(KNOWLEDGE_BASE),
        "timestamp": datetime.datetime.now().isoformat(),
        "uptime_since": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "active_sessions": len(session_store)
    })


@app.route("/api/session/<session_id>", methods=["GET"])
def get_session(session_id):
    """Get session statistics"""
    s = session_store.get(session_id, {"messages": 0, "words": 0, "questions": 0})
    return jsonify(s)


@app.route("/api/session/<session_id>", methods=["DELETE"])
def clear_session(session_id):
    """Clear a session"""
    if session_id in session_store:
        del session_store[session_id]
    return jsonify({"cleared": True})


@app.route("/api/audio/<filename>", methods=["GET"])
def serve_audio(filename):
    """Serve audio files from static/audio directory"""
    audio_dir = os.path.join(app.root_path, "static", "audio")
    if os.path.exists(os.path.join(audio_dir, filename)):
        return send_from_directory(audio_dir, filename)
    return jsonify({"error": "Audio file not found"}), 404


@app.route("/api/intents", methods=["GET"])
def list_intents():
    """List all supported intent categories (for demo)"""
    intents = [
        {"name": "Greeting", "icon": "👋", "example": "Hello / Namaste"},
        {"name": "Code Request", "icon": "💻", "example": "Write a Java program..."},
        {"name": "Question", "icon": "❓", "example": "What is AI?"},
        {"name": "Explanation", "icon": "📚", "example": "Explain machine learning"},
        {"name": "Analysis", "icon": "🔍", "example": "Compare SQL vs NoSQL"},
        {"name": "Creative", "icon": "✨", "example": "Write a story about..."},
        {"name": "Math", "icon": "🧮", "example": "Solve this equation..."},
        {"name": "Translation", "icon": "🌐", "example": "Translate to Hindi"},
        {"name": "General Chat", "icon": "💬", "example": "Anything else"},
    ]
    return jsonify({"intents": intents, "total": len(intents)})


@app.route("/api/knowledge", methods=["GET"])
def knowledge_stats():
    """Show knowledge base stats (for mentor demo)"""
    stats = []
    for key, val in KNOWLEDGE_BASE.items():
        if key != "fallback":
            stats.append({
                "category": key,
                "patterns": len(val["patterns"]),
                "responses": len(val["responses"])
            })
    return jsonify({
        "total_categories": len(stats),
        "total_patterns": sum(s["patterns"] for s in stats),
        "total_responses": sum(s["responses"] for s in stats),
        "categories": stats
    })


# ──────────────────────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║          NEXUS AI Backend — Starting Server                   ║
╠═══════════════════════════════════════════════════════════════╣
║  Backend:     Python Flask                                    ║
║  NLP Engine:  Custom Rule-Based NLP v3.0                      ║
║  Model:       NEXUS-NLP-v3.0                                  ║
║  Knowledge:   {} categories loaded                          ║
╠═══════════════════════════════════════════════════════════════╣
║  Frontend:    http://localhost:5000                           ║
║  API Base:    http://localhost:5000/api                       ║
║  Chat:        POST http://localhost:5000/api/chat             ║
║  Status:      GET  http://localhost:5000/api/status           ║
╚═══════════════════════════════════════════════════════════════╝
    """.format(len(KNOWLEDGE_BASE)))
    app.run(debug=True, host="0.0.0.0", port=5000)
