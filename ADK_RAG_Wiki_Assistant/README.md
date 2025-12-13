
# Parallel Multi‑Agent Hiring Review Pipeline (Google ADK)

This project demonstrates a powerful **ParallelAgent + SequentialAgent** workflow using the Google AI Developer Kit (ADK).  
It evaluates a candidate’s resume through **three independent reviewers running in parallel**, followed by a final hiring summary agent that merges their outputs.

This architecture mirrors real‑world hiring panels where multiple reviewers independently assess a candidate before a hiring manager makes the final call.

---

## 🚀 Features

### ✅ Parallel Technical, Culture, and Compensation Review  
Three LlmAgents run **simultaneously** on the same resume:

1. **TechReviewer**  
   - Evaluates backend skills, APIs, microservices, databases, system design  
   - Produces a technical rating (1–10)

2. **CultureFitReviewer**  
   - Assesses communication, stability, ownership, leadership signals  
   - Produces a culture‑fit rating (1–10)

3. **CompensationBenchmarker**  
   - Suggests a compensation band (LPA, India)  
   - Based on experience, seniority, and typical market expectations

### ✅ Final Hiring Summary  
A fourth agent, **HiringSummaryAgent**, merges all three assessments and produces:

- Technical summary  
- Culture fit summary  
- Compensation band  
- Final decision label:  
  - `REJECT`  
  - `KEEP IN PIPELINE`  
  - `STRONG HIRE`  
- One‑sentence justification  

---

## 🧠 Architecture Overview

```
                ┌──────────────────────┐
                │   Tech Reviewer      │
                └──────────────────────┘
                         ▲
                         │
                         │
┌──────────────┐   ┌──────────────────────┐   ┌────────────────────────┐
│   Resume      │ → │ Culture Fit Reviewer │ → │ Compensation Reviewer  │
└──────────────┘   └──────────────────────┘   └────────────────────────┘
                         │
                         ▼
                ┌────────────────────────────┐
                │   Hiring Summary Agent     │
                └────────────────────────────┘
```

The three reviewers run **in parallel**, and their outputs are merged by the summary agent.

---

## 📁 Project Structure

```
ParallelAgent_HiringPipeline/
│
├── app.py            # Main ADK workflow agent
├── README.md
├── requirements.txt
└── .gitignore
```

Everything is intentionally kept in a **single file** for simplicity.

---

## 🔧 Installation

### 1. Create and activate a virtual environment

```bash
python -m venv env
env\Scripts\activate      # Windows
source env/bin/activate   # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Google API key

Create a `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## ▶️ Running the Agent

This is an **ADK workflow agent**, so you run it using the ADK CLI — *not* with `python app.py`.

From the project folder:

```bash
adk run
```

You will see:

```
ParallelHiringReviewPipeline >
```

Paste your resume text directly into the prompt and press **Enter**.

ADK will automatically:

- Run all three reviewers in parallel  
- Merge their outputs  
- Produce a final structured hiring summary  

---

## 🧪 Example Input

```
Jane Doe
Backend Developer

Experience:
Software Engineer at Flipkart (3 years)
- Built microservices in Java and Spring Boot
- Designed REST APIs
- Worked with MySQL and Redis
- Mentored junior developers

Skills:
Java, Spring Boot, MySQL, Redis, Docker, Kubernetes, Git
```

---

## ✅ Example Output (Simplified)

```
## Final Candidate Summary
Technical: Strong backend experience with Java, Spring Boot, and microservices...
Culture Fit: Stable career progression, clear responsibilities...
Compensation: Suggested Band: 18–24 LPA (India, Backend Developer)
Decision: KEEP IN PIPELINE
Reason: Strong technical profile with solid culture fit.
```

---

## 📌 Notes

- This project demonstrates **ParallelAgent** orchestration in ADK  
- All sub‑agents are **LlmAgent** instances  
- The pipeline is fully extensible (add JD parser, recruiter agent, final decision agent, etc.)  
- Ideal for demonstrating multi‑agent reasoning patterns  

---

## 📄 License

This project is for educational and experimental use.
```
