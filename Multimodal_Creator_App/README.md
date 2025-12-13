
# MediaMaker Multimodal AI App

MediaMaker is a Streamlit-based multimodal application that brings together three powerful AI capabilities in one simple interface:

- **Image Generation**  
- **Image Captioning**  
- **YouTube Video Summarization**

Powered by Google’s Gemini multimodal models, this app allows users to create images, understand images, and summarize video content—all from a clean, intuitive UI.

---

## 🚀 Features

### 🎨 Image Generation
Enter a text prompt and generate an AI-created image using Gemini’s multimodal generation capabilities.

### 📝 Image Captioning
Upload any image (PNG/JPG/JPEG) and let the model describe it in natural language.

### 🎬 YouTube Video Summarization
Paste a YouTube URL and receive a concise summary of the video’s content.

---

## 🧠 Tech Stack

- **Python 3.10+**
- **Streamlit** for the UI
- **Google Gemini API (`google.genai`)** for multimodal AI
- **Pillow (PIL)** for image handling
- **dotenv** for environment variable management

---

## 📁 Project Structure

```
MediaMaker_Multimodal_App/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not committed)
└── README.md              # Project documentation
```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd MediaMaker_Multimodal_App
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
env\Scripts\activate      # Windows
source env/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key

Create a `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## 🖥️ Usage

Once the app launches:

1. **Image Generator**  
   - Enter a prompt  
   - Click **Generate Image**

2. **Image Caption Generator**  
   - Upload an image  
   - Click **Generate Caption**

3. **YouTube Video Summarizer**  
   - Paste a YouTube URL  
   - Click **Summarize Video**

---

## ⚠️ Quota & Rate Limits

Some Gemini models—especially experimental or image-generation models—may require paid quota.  
If you encounter a `429 RESOURCE_EXHAUSTED` error, switch to a free-tier model or check your usage at:

- https://ai.dev/usage  
- https://ai.google.dev/gemini-api/docs/rate-limits

---

## ✅ Future Enhancements

- Audio transcription  
- PDF summarization  
- Multi-page Streamlit navigation  
- Integration with ADK MCP tools  
- Local file summarization  
- Drag-and-drop image editing

---

## 📄 License

This project is for educational and experimental use.

```

