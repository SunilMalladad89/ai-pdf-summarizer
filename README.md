# AI PDF Summarizer & Question Answering System



An AI-powered web application built with Django that extracts information from PDF documents, generates summaries, and answers questions using a locally running Large Language Model (LLM).



## Features



- ðŸ“„ **PDF Upload & Processing** â€” Upload and process PDF documents.

- ðŸ“ **Text Extraction** â€” Extract text from PDFs using `pdfplumber`.

- ðŸ“Š **Document Statistics** â€” Analyze document content.

- ðŸ”‘ **Keyword Extraction** â€” Identify important keywords using YAKE.

- ðŸ“š **Multiple Summary Modes** â€” Generate short, medium, and detailed summaries.

- ðŸ¤– **AI Question Answering** â€” Ask questions about document content.

- ðŸ§  **Local LLM Integration** â€” Integrate Ollama with the Phi-3 model.

- ðŸ” **Section Retrieval** â€” Retrieve relevant document sections using TF-IDF.

- ðŸ“– **Source Section Verification** â€” Review relevant source sections to verify answers.

- ðŸ•’ **Q&A History** â€” Keep track of previous questions and answers.

- ðŸ“¥ **PDF Report Download** â€” Export summaries as downloadable PDF reports.

- âš¡ **Local AI Processing** â€” Run supported AI inference locally without sending document content to a cloud LLM, when using the local Ollama path.



## ðŸ› ï¸ Technology Stack



| Technology | Purpose |

|---|---|

| Python | Core programming language |

| Django | Web application framework |

| pdfplumber | PDF text extraction |

| YAKE | Keyword extraction |

| Scikit-learn | TF-IDF-based retrieval |

| Ollama | Local LLM runtime |

| Phi-3 | Language model |

| ReportLab | PDF report generation |

| Requests | HTTP requests |

| python-dotenv | Environment variable management |



## âš™ï¸ Installation and Setup



### Prerequisites



- Python

- pip

- Ollama

- The Phi-3 model downloaded through Ollama



### 1. Clone the repository



```bash

git clone https://github.com/SunilMalladad89/ai-pdf-summarizer.git

cd ai-pdf-summarizer

```



### 2. Create and activate a virtual environment



Windows PowerShell:



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



### 3. Install dependencies



```powershell

pip install -r requirements.txt

```



### 4. Configure environment variables



Create a `.env` file in the project root.



Add the environment variables required by the application:



```text

DJANGO\_SECRET\_KEY=your\_generated\_django\_secret\_key

GEMINI\_API\_KEY=your\_gemini\_api\_key

```



Generate a new Django secret key for your own environment. Add a Gemini API key only if your configured application features require it.



**Never commit `.env` or publish real API keys or secret keys.**



### 5. Install and prepare Ollama



Install Ollama from:



https://ollama.com/



Download the Phi-3 model:



```powershell

ollama pull phi3

```



Ensure Ollama is running before using local-model features.



### 6. Run database migrations



```powershell

python manage.py migrate

```



### 7. Start the Django development server



```powershell

python manage.py runserver

```



Open the application in your browser:



http://127.0.0.1:8000/



## ðŸ”„ How It Works



1\. Upload a PDF document.

2\. Extract and analyze its text.

3\. Extract important keywords and document statistics.

4\. Generate a summary in the selected format.

5\. Ask questions about the document.

6\. Retrieve relevant sections using TF-IDF.

7\. Generate answers using the configured language model.

8\. Review source sections and download a summary report.



## ðŸŽ¯ Project Objective



This project demonstrates the practical application of Python web development, PDF processing, natural language processing, information retrieval, and local LLM integration.



## ðŸ”® Potential Improvements



- Add automated tests for core application features.

- Improve retrieval with embedding-based semantic search.

- Strengthen answer grounding and source citations.

- Add screenshots and a demonstration video.

- Improve error handling for scanned PDFs and large documents.

- Document deployment and production security configuration.



## ðŸ“Œ Future Contributions



Contributions and suggestions for improving the project are welcome.



## ðŸ“„ License



No license has been specified yet. Add a license if you intend to define how others may use, modify, and distribute the project.


