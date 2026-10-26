# AI PDF Summarizer & Question Answering System

An AI-powered Django web application that extracts information from PDF documents, generates summaries, and answers questions using a Large Language Model (LLM).

## Features

- **PDF Upload and Processing:** Upload and process PDF documents.
- **Text Extraction:** Extract text from PDFs using pdfplumber.
- **Document Statistics:** Analyze document content.
- **Keyword Extraction:** Identify important keywords using YAKE.
- **Multiple Summary Modes:** Generate short, medium, and detailed summaries.
- **AI Question Answering:** Ask questions about document content.
- **Local LLM Integration:** Use Ollama with the Phi-3 model.
- **Section Retrieval:** Retrieve relevant document sections using TF-IDF.
- **Source Verification:** Review relevant document sections to verify answers.
- **Question and Answer History:** Review previous questions and answers.
- **PDF Report Download:** Export summaries as downloadable PDF reports.
- **Local AI Processing:** Run supported inference locally through Ollama.

## Technology Stack

- Python
- Django
- pdfplumber
- YAKE
- Scikit-learn
- Ollama and Phi-3
- ReportLab
- Requests
- python-dotenv

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SunilMalladad89/ai-pdf-summarizer.git
cd ai-pdf-summarizer
```

### 2. Create a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and configure the environment variables required by the application, including `DJANGO_SECRET_KEY`.

Add `GEMINI_API_KEY` only if your application uses Gemini API functionality.

Never commit your `.env` file or publish secret keys.

### 5. Install Ollama and download Phi-3

Install Ollama from https://ollama.com/

```powershell
ollama pull phi3
```

Ensure Ollama is running before using the local model.

### 6. Run database migrations

```bash
python manage.py migrate
```

### 7. Start the application

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## How It Works

1. Upload a PDF document.
2. Extract and analyze its text.
3. Extract keywords and document statistics.
4. Generate a summary using the selected summary mode.
5. Ask questions about the document.
6. Retrieve relevant sections using TF-IDF.
7. Generate answers using the configured language model.
8. Review source sections and download the summary report.

## Project Objective

This project demonstrates practical Python development, PDF processing, natural language processing, information retrieval, and local LLM integration.

## Future Improvements

- Add automated tests.
- Improve document retrieval.
- Strengthen answer verification and source references.
- Add application screenshots and a demo video.
- Document deployment and production security.

## License

No license has been specified yet. Add an appropriate license if you intend to distribute the project.