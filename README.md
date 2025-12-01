

# **withyou — An Agentic Mental Health Companion**

*A multi-agent mental wellness system and future mobile app designed to track mood, journaling, habits, and emotional patterns — offering personalized, safe, and adaptive mental health support.*

---

## **🌱 Overview**

**withyou** is an agentic mental health companion built using concepts from the **Google 5-Day AI Agents Intensive**.
Its goal is to provide **safe, personalized, and continuous emotional support** using:

* Multi-agent orchestration
* Context-aware interventions
* Journaling + mood analysis
* Personalized recommendations
* Secure long-term memory
* Observability, evaluation, and safety mechanisms

The prototype in this repository represents the **backend intelligence** that will eventually power a **mobile app** capable of:

* Tracking mood and symptoms
* Recording journaling entries
* Recognizing emotional patterns
* Suggesting evidence-based interventions
* Helping users build healthy routines
* Escalating to human help when needed

---

## **✨ Key Features**

### **1. Multi-Agent System**

* **Safety Agent** (crisis detection)
* **Triage Agent** (interprets signals + routing)
* **Coach Agent** (grounding, CBT-inspired support)
* **Planner Agent** (habits + routine scheduling)
* **Clinician Bridge Agent** (professional summaries)

### **2. Tools (MCP-inspired)**

* `symptom_checker`
* `resource_lookup`
* `scheduler_tool`
* `journal_insights_tool` *(mocked)*
* `mood_trend_analyzer` *(mocked)*

### **3. Sessions & Memory**

* Short-term session state
* Long-term memory for user preferences & patterns
* Consent-based, encrypted storage

### **4. Observability**

* Logs
* Traces
* Metrics
* LLM-as-Judge evaluation pipeline

### **5. Mobile-App Ready Architecture**

* Designed for mood logs, journaling, activity monitoring
* Future-ready for notifications & habit-building workflows

---

## **🧠 System Architecture**

> *Note: Replace the image below with your actual architecture diagram when ready.*

```
+-----------------------------------------------------+
|                      withyou                        |
|              Agentic Backend Architecture           |
+-----------------------------------------------------+
|  Client Layer (App/Notebook UI)                     |
|      - Chat Interface                               |
|      - Mood Logs / Journaling                       |
+-----------------------------------------------------+
|  Orchestrator Layer                                 |
|      - Routing                                      |
|      - Context Engineering                          |
|      - Memory Retrieval                             |
|      - Observability                                |
+-----------------------------------------------------+
|  Multi-Agent System                                 |
|   - Safety Agent                                    |
|   - Triage Agent                                    |
|   - Coach Agent                                     |
|   - Planner Agent                                   |
|   - Clinician Bridge Agent                          |
+-----------------------------------------------------+
|                Tools (MCP-based)                    |
|   - Symptom Checker                                 |
|   - Scheduler                                       |
|   - Resource Lookup                                 |
|   - Journaling Analyzer (mock)                      |
|   - Mood Pattern Analyzer (mock)                    |
+-----------------------------------------------------+
|         Sessions + Long-Term Memory                 |
|         (Encrypted, Consent-based)                  |
+-----------------------------------------------------+
```

---

## **📦 Repository Structure**

```
withyou/
├── README.md
├── docs/
│   ├── architecture.png
│   ├── safety_flow.png
│   ├── mobile_app_future.png
│
├── notebooks/
│   ├── demo_notebook.ipynb
│   ├── evaluation_pipeline.ipynb
│
├── src/
│   ├── agents/
│   │   ├── safety_agent.py
│   │   ├── triage_agent.py
│   │   ├── coach_agent.py
│   │   ├── planner_agent.py
│   │   └── clinician_bridge_agent.py
│   ├── tools/
│   │   ├── symptom_checker.py
│   │   ├── scheduler_tool.py
│   │   ├── resource_lookup.py
│   │   └── mock_analysis_tools.py
│   ├── orchestrator/
│   │   └── orchestrator.py
│   ├── session_service.py
│   ├── memory_bank.py
│   └── observability/
│       ├── logger.py
│       └── metrics.py
│
└── tests/
    ├── test_triage.py
    ├── test_safety.py
    └── test_tools.py
```

---

## **🚀 Getting Started**

### **1. Clone the Repository**

```bash
git clone https://github.com/<your-username>/withyou.git
cd withyou
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Open the Demo Notebook**

Run it directly in:

* **Kaggle**, or
* **Jupyter Notebook**, or
* **Colab (no API keys needed)**

```bash
jupyter notebook notebooks/demo_notebook.ipynb
```

---

## **🧩 Agents Overview**

### **🛡️ Safety Agent**

* Runs first on every message
* Identifies crisis indicators (self-harm, extreme distress)
* Provides crisis resources
* Escalates to human reviewers
* Stops all other agents

---

### **📊 Triage Agent**

* Interprets conversation signals
* Reads mood trends from mobile app input (simulated)
* Evaluates journaling sentiment
* Decides which agent handles next steps

---

### **💬 Coach Agent**

Provides personalized, evidence-aligned support:

* CBT-style reframing
* Grounding exercises
* Emotional regulation strategies
* Mindfulness micro-guidance
* Tailors interventions based on memory

---

### **📅 Planner Agent**

Uses scheduling tools to help build consistent habits:

* Sleep hygiene routines
* Journaling streak encouragement
* Self-care activity planning
* Break reminders

---

### **📝 Clinician Bridge Agent**

When users opt in:

* Creates redacted summaries
* Prepares mood trend snapshots
* Helps share insights with mental health professionals

---

## **🔧 Tools Layer (MCP-inspired)**

| Tool Name                 | Description                    |
| ------------------------- | ------------------------------ |
| **symptom_checker**       | Grades severity based on input |
| **scheduler_tool**        | Creates reminders & routines   |
| **resource_lookup**       | Fetches vetted help resources  |
| **journal_insights_tool** | Analyzes journaling (mock)     |
| **mood_trend_analyzer**   | Detects mood shifts (mock)     |

These tools can easily be replaced with real APIs in the future mobile app.

---

## **🧠 Memory & Sessions**

### **Sessions**

Maintain short-term conversation context.

### **Memory Bank**

Stores long-term:

* user preferences
* coping strategies
* emotional triggers
* journaling patterns
* mood patterns

All data is:

* encrypted
* consent-based
* user-controllable (view/edit/delete)

---

## **📊 Observability & Evaluation**

* **Logs** track each agent’s behavior
* **Traces** reveal how tasks flow through agents
* **Metrics** measure safety, latency, completion rates
* **LLM-as-Judge** evaluates quality & helpfulness

The included `evaluation_pipeline.ipynb` notebook automates this process.

---

## **🧪 Running Tests**

```bash
pytest tests/
```

Tests include:

* crisis detection
* tool output validation
* triage logic correctness

---

## **🔐 Safety, Ethics & Scope**

**withyou is NOT a medical device and does NOT diagnose conditions.**
It is a supportive wellness tool only.

### Safety Measures:

* crisis detection with escalation
* human-in-the-loop workflows
* explicit user consent for memory
* secure data handling
* non-diagnostic guidance only

### Ethical Principles:

* user autonomy
* transparency
* privacy by design
* avoid overconfidence or medical claims

---

## **📱 Future Work (Mobile App)**

Planned for future versions:

* Flutter / React Native mobile app
* Mood tracking dashboard
* Emotional insights visualization
* Habit analytics
* Push notifications
* Local on-device encryption
* On-device inference for sensitive tasks

---

## **🛠️ Technologies Used**

* Python
* ADK patterns
* MCP-style tools
* LLM-based reasoning
* Memory Bank
* Context Engineering
* Observability (logs/traces/metrics)
* Kaggle Notebooks

---

## **📄 License**

MIT License (or your preferred license)

---

## **🤝 Acknowledgements**

This project was inspired and built during the **Google + Kaggle 5-Day AI Agents Intensive Course**.

