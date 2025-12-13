import os
from google.adk.agents import ParallelAgent, SequentialAgent, LlmAgent


GEMINI_MODEL = "gemini-2.5-flash"


# ---------- Parallel Sub-Agents: All read the same resume, run in parallel ----------


tech_reviewer_agent = LlmAgent(
   name="TechReviewer",
   model=GEMINI_MODEL,
   description="Evaluates technical strength of the candidate for a Backend Developer role.",
   instruction=(
       "You are a senior backend engineer reviewing a candidate's resume for a Backend Developer role.\n"
       "Read the resume text carefully and write a short, focused technical assessment.\n\n"
       "Comment on:\n"
       "- Backend languages and frameworks (e.g., Python, Java, Node.js, Go, .NET, etc.).\n"
       "- Databases and storage (SQL/NoSQL, which ones, how used).\n"
       "- Experience with APIs, microservices, system design, distributed systems, or performance.\n"
       "- Years of relevant backend experience.\n\n"
       "End with a single line: 'Technical Rating: X/10' where X is an integer between 1 and 10.\n"
       "Output 1–2 short paragraphs plus the final rating line."
   ),
   output_key="tech_assessment",
)


culture_reviewer_agent = LlmAgent(
   name="CultureFitReviewer",
   model=GEMINI_MODEL,
   description="Assesses culture fit, communication, and stability.",
   instruction=(
       "You are an HR business partner assessing culture fit for a Backend Developer role.\n"
       "Read the resume text and provide a brief assessment focusing on:\n"
       "- Communication indicators (clear responsibilities, achievements, leadership, mentoring, etc.).\n"
       "- Stability (frequency of job changes, internships vs full-time roles).\n"
       "- Ownership/initiative (projects owned, impact described, cross-team work).\n"
       "- Any red flags (very short stints, unclear responsibilities, etc.).\n\n"
       "End with a single line: 'Culture Fit Rating: Y/10' where Y is an integer between 1 and 10.\n"
       "Output 1–2 short paragraphs plus the final rating line."
   ),
   output_key="culture_assessment",
)


compensation_reviewer_agent = LlmAgent(
   name="CompensationBenchmarker",
   model=GEMINI_MODEL,
   description="Suggests a compensation band based on experience and role level.",
   instruction=(
       "You are a compensation analyst for a tech company in India.\n"
       "Based ONLY on the resume text and typical Indian market expectations, estimate a reasonable\n"
       "fixed-CTC band (in LPA) for this candidate as a Backend Developer.\n\n"
       "Consider:\n"
       "- Total years of relevant backend/software experience.\n"
       "- Brand and size of companies (startups vs big product companies vs service companies).\n"
       "- Seniority level (junior, mid, senior).\n\n"
       "Output:\n"
       "- 1–2 sentences explaining your reasoning.\n"
       "- Then a line in the format: 'Suggested Band: A–B LPA (India, Backend Developer)'\n"
       "Do NOT mention any city-specific or company-specific data; keep it generic."
   ),
   output_key="comp_assessment",
)


# ---------- Parallel Agent: all three run concurrently ----------


parallel_assessment_agent = ParallelAgent(
   name="ParallelCandidateAssessment",
   sub_agents=[tech_reviewer_agent, culture_reviewer_agent, compensation_reviewer_agent],
   description="Runs tech, culture, and compensation assessments in parallel on the same resume.",
)


# ---------- Merger Agent: reads outputs from the parallel agents ----------


hiring_summary_agent = LlmAgent(
   name="HiringSummaryAgent",
   model=GEMINI_MODEL,
   description="Combines parallel assessments into a final hiring recommendation.",
   instruction=(
       "You are the hiring manager summarizing the parallel reviews for a Backend Developer candidate.\n\n"
       "You will receive the following assessments:\n"
       "- Technical assessment and rating: {tech_assessment}\n"
       "- Culture fit assessment and rating: {culture_assessment}\n"
       "- Compensation suggestion: {comp_assessment}\n\n"
       "Task:\n"
       "1) Briefly summarize the technical strength (1–2 sentences).\n"
       "2) Briefly summarize culture fit and soft-skill signals (1–2 sentences).\n"
       "3) Mention the suggested compensation band.\n"
       "4) Give a clear final decision label in ALL CAPS: one of\n"
       "   'REJECT', 'KEEP IN PIPELINE', or 'STRONG HIRE'.\n"
       "5) In one sentence, justify that final label.\n\n"
       "Output Format (strict):\n"
       "## Final Candidate Summary\n"
       "Technical: <your summary>\n"
       "Culture Fit: <your summary>\n"
       "Compensation: <band line>\n"
       "Decision: <REJECT / KEEP IN PIPELINE / STRONG HIRE>\n"
       "Reason: <one-sentence justification>"
   ),
)


# ---------- Overall root agent: Sequential(Parallel(...) -> Merger) ----------
root_agent = SequentialAgent(
   name="ParallelHiringReviewPipeline",
   sub_agents=[
       parallel_assessment_agent,  # runs all reviewers in parallel
       hiring_summary_agent,       # merges their outputs
   ],
   description="Parallel multi-agent hiring review: tech + culture + compensation, then a combined decision.",
)
