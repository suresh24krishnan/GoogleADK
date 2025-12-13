
# **ADK RAG Wiki Assistant (Embedding‑Based RAG with Google ADK + OpenAI)**

A lightweight, fast, and fully self‑contained **Retrieval‑Augmented Generation (RAG)** agent built using **Google ADK**, **OpenAI embeddings**, and **in‑memory vector search**.  
This project demonstrates how to build a clean, production‑ready RAG pipeline without external vector databases like Chroma or FAISS — perfect for learning, prototyping, and extending into more advanced multi‑document systems.

---

## ✅ **Features**

- **Google ADK Agent** with tool‑calling  
- **Embedding‑based RAG** using OpenAI’s `text-embedding-3-small`  
- **In‑memory vector store** (no Chroma, no FAISS, no DB required)  
- **Automatic chunking** of Wikipedia content  
- **Cosine similarity retrieval**  
- **Context‑grounded answers** using Gemini (`gemini-2.5-flash`)  
- **Caching layer** to avoid repeated embedding calls  
- **Clean, modular architecture** for easy extension  

---

## ✅ **Project Structure**

```
ADK_RAG_Wiki_Assistant/
│
├── adk_rag_wiki_assistant_agent/
│   ├── agent.py               # Main ADK agent with embeddings + RAG
│   ├── __init__.py            # Auto-loads root_agent for ADK
│   └── .env (ignored)         # API keys (not committed)
│
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── .gitignore                 # Ensures env + secrets are excluded
```

---

## ✅ **How It Works**

### **1. Fetch Wikipedia Content**
The agent retrieves the **Artificial Intelligence** Wikipedia page using a browser‑like User‑Agent to avoid 403 blocks.

### **2. Chunking**
The page is split into ~800‑character chunks, respecting paragraph boundaries.

### **3. Embedding**
All chunks are embedded using:

```
text-embedding-3-small
```

Embeddings are cached in memory for the lifetime of the ADK process.

### **4. Query Embedding + Similarity Search**
Each user query is embedded and compared to all chunk vectors using cosine similarity.

### **5. Top‑K Retrieval**
The top 3 most relevant chunks are returned as context.

### **6. Gemini Generates the Final Answer**
The ADK agent:

- **must call** the `retrieve_ai_context` tool first  
- receives the retrieved context  
- produces a grounded, accurate answer  

---

## ✅ **Setup Instructions**

### **1. Clone the repo**

```bash
git clone https://github.com/suresh24krishnan/GoogleADK.git
cd GoogleADK/ADK_RAG_Wiki_Assistant
```

### **2. Create a virtual environment**

```bash
python -m venv env
source env/bin/activate   # macOS/Linux
env\Scripts\activate      # Windows
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

### **4. Add your API keys**

Create `.env` inside:

```
ADK_RAG_Wiki_Assistant/adk_rag_wiki_assistant_agent/
```

Add:

```
GOOGLE_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
```

### **5. Run the agent**

From the project root:

```bash
adk run
```

You’ll see:

```
Running agent wiki_rag_embedding_agent...
```

---

## ✅ **Example Queries**

Try these inside the ADK console:

- *What is artificial intelligence*  
- *Explain the history of AI*  
- *What is the difference between strong AI and weak AI*  
- *What are the applications of AI in real life*  
- *What is the Turing test and why is it important*  

Each query triggers:

✅ embedding search  
✅ context retrieval  
✅ grounded answer generation  

---

## ✅ **Why No ChromaDB or FAISS?**

This project intentionally avoids external vector databases to keep things:

- simple  
- portable  
- dependency‑free  
- Windows‑friendly  
- easy to extend  

The in‑memory vector store is fast and perfect for single‑document RAG.

If you want to scale to:

- multiple documents  
- persistent storage  
- millions of vectors  

you can easily swap in FAISS, LanceDB, or a cloud vector DB.

---

## ✅ **Future Enhancements**

Here are natural next steps:

- Add multiple Wikipedia pages (ML, Deep Learning, Robotics, AGI…)  
- Add PDF ingestion  
- Add persistent FAISS index  
- Add a Streamlit UI  
- Add section‑aware retrieval  
- Add source citations in the final answer  

---

## ✅ **Author**

**Suresh Krishnan**  
Enterprise/Solution/Product Architect  
AI/ML, multi‑agent systems, reproducible workflows, emotionally attuned UX  

---
