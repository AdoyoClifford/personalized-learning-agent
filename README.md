<div align="center">

# 🎓 Personalized Learning Agent

**An AI agent that creates adaptive, personalized learning paths for students**

[![Python](https://img.shields.io/badge/Python-100%25-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![AI Agent](https://img.shields.io/badge/AI%20Agent-LLM%20Powered-FF6F00?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

</div>

---

## 📖 About

The Personalized Learning Agent is an AI-powered system that creates **customized learning paths** tailored to each student's goals, skill level, and learning preferences. Built with Python, it leverages LLMs to generate adaptive content, assess understanding, and recommend optimal next steps in a student's learning journey.

## ✨ Features

- 🎯 **Adaptive Learning Paths** — Generates custom curricula based on student goals and current knowledge
- 📊 **Skill Assessment** — Evaluates student proficiency to determine starting points
- 📝 **Content Generation** — Creates exercises, explanations, and quizzes using LLMs
- 🔄 **Dynamic Adjustment** — Adapts the learning path based on student progress and performance
- 💡 **Smart Recommendations** — Suggests resources and topics based on learning patterns
- 🧠 **Context-Aware** — Maintains conversation history for personalized interactions

## 🏗️ How It Works

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│   Student    │────▶│  Learning Agent  │────▶│ Personalized │
│   Input      │     │                  │     │ Learning     │
│  (goals,     │     │  ┌────────────┐  │     │ Path         │
│   skill      │     │  │ Assessment │  │     │              │
│   level)     │     │  ├────────────┤  │     │ • Modules    │
│              │     │  │ Curriculum │  │     │ • Exercises  │
│              │     │  │ Generator  │  │     │ • Quizzes    │
│              │     │  ├────────────┤  │     │ • Resources  │
│              │     │  │ Progress   │  │     │              │
│              │     │  │ Tracker    │  │     │              │
│              │     │  └────────────┘  │     │              │
└──────────────┘     └──────────────────┘     └──────────────┘
```

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| **Language** | Python |
| **AI/LLM** | Large Language Models |
| **Architecture** | AI Agent Pattern |
| **Focus** | Education Technology |

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- An LLM API key (OpenAI / Google AI)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AdoyoClifford/personalized-learning-agent.git
   cd personalized-learning-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the agent**
   ```bash
   python -m learning_assistant_agent
   ```

## 📁 Project Structure

```
personalized-learning-agent/
├── learning_assistant_agent/
│   ├── __init__.py        # Agent initialization
│   ├── agent.py           # Core agent logic
│   ├── assessment.py      # Skill assessment module
│   ├── curriculum.py      # Curriculum generation
│   └── utils/             # Utility functions
├── .env.example
├── requirements.txt
└── README.md
```

## 🎯 Use Cases

- **Self-learners** wanting a structured path for new skills
- **Educators** looking to create personalized material for students
- **EdTech platforms** needing adaptive learning capabilities
- **Bootcamps** wanting to assess and customize student paths

## 🗺️ Roadmap

- [ ] Add support for multiple subjects and domains
- [ ] Implement spaced repetition for review scheduling
- [ ] Build a web interface for interactive learning
- [ ] Add progress analytics and visualizations
- [ ] Support multi-language content generation

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

