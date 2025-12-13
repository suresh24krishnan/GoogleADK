
# MultiAgent Sequential Pipeline (Google ADK)

This project demonstrates a clean, production‑ready **Sequential Workflow Agent** built using the Google AI Developer Kit (ADK).  
It evaluates a candidate’s resume through a three‑stage pipeline:

1. ✅ **ResumeValidator** — Checks if the resume meets minimum backend developer requirements  
2. ✅ **SkillEvaluator** — Scores the candidate (1–10) if valid  
3. ✅ **HRSummary** — Produces a professional HR‑style summary  

The entire workflow is orchestrated by a **SequentialAgent**, making this a simple but powerful example of multi‑agent architecture.

---

## 🚀 Features

### ✅ Resume Validation  
Ensures the candidate meets baseline requirements:
- Education or equivalent experience  
- At least 1 year of software development  
- Backend language + database + Git  
- Backend‑relevant work experience  

### ✅ Skill Scoring  
If valid, the candidate is scored **1–10** based on:
- Backend depth  
- Tech stack  
- Experience level  
- Mention of APIs, services, cloud, distributed systems  

### ✅ HR Summary  
Generates a concise, professional summary including:
- Fit for backend role  
- Strengths  
- Gaps  
- Recommendation (Reject / Keep in pipeline / Strong hire)

---

## 📁 Project Structure

```
MultiAgent_Sequential_Pipeline/
│
├── app.py            # Main ADK workflow agent
├── README.md
├── requirements.txt
└── .gitignore
```

Everything is intentionally kept in a **single file** for simplicity and clarity.

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

### 3. Set your Google API key

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
multiagent_sequential_pipeline >
```

Paste your resume text directly into the prompt and press **Enter**.

ADK will automatically:

1. Validate the resume  
2. Score the candidate  
3. Generate the HR summary  
4. Return the final output  

---

## 🧠 Example Input

Paste something like:

```
John Doe
Backend Developer

Education:
B.S. in Computer Science

Experience:
Software Engineer (2 years)
- Built REST APIs in Python
- Worked with PostgreSQL
- Implemented microservices

Skills:
Python, FastAPI, Docker, Git, PostgreSQL, AWS
```

---

## ✅ Example Output (Simplified)

```
The candidate is a strong fit for a backend developer role...
Skill Score: 8
Recommendation: Keep in pipeline
```

---

## 📌 Notes

- This project uses **SequentialAgent**, one of ADK’s workflow agent types  
- All sub‑agents are **LlmAgent** instances  
- The pipeline is fully extensible (add JD parser, recruiter agent, final decision agent, etc.)

---

## 📄 License

This project is for educational and experimental use.
```
