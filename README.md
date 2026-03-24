<p align="center">
<em> <strong>CareerCatalyst - AI-Powered Professional Development Ecosystem</strong> </em>
</p>

---

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Personal Project](https://img.shields.io/badge/Personal%20Project-orange.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Table of Contents
- [Overview](#-overview)
- [Core Values Proposition](#-core-values-proposition)
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Detailed Setup Guide](#-detailed-setup-guide)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Sample Documents](#-sample-documents--disclaimer)
- [Contributing](#-contributing)
- [License & Acknowledgments](#-license--acknowledgments)
- [Contact](#-contact)

## Overview

***CareerCatalyst*** is an intelligent ecosystem of interconnected AI agents designed to support young professionals in a company from day one through their career journey. The system leverages a network of specialized agents that collaborate to provide personalized onboarding guidance, adaptive learning, and continuous career coach support.

Born from a training for talent leaders, ***CareerCatalyst*** demonstrates how multiple AI agents can work together to create a comprehensive professional development experience, all running locally with open-source technologies.

## Core Values Proposition

- **Accelerated Onboarding**: Reduce time-to-productivity from months to weeks
- **Personalized Learning**: AI-driven skill development based on role requirements and career goals
- **Continuous Mentorship**: 24/7 availability of guidance and feedback
- **Career Intelligence**: Data-driven insights for career progression

## Design Architecture

The architecture maintains the core multi-agent system while providing multiple access points for different user preferences and use cases. All design and implementation are based on open-source LLM and tools in Python.
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE LAYER                               │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐   │
│  │       TELEGRAM BOT INTERFACE    │  │      WEB CHAT INTERFACE         │   │
│  │  ┌─────────────────────────┐    │  │  ┌─────────────────────────┐    │   │
│  │  │   Telegram Bot Server   │    │  │  │    Streamlit Web App    │    │   │
│  │  └─────────────────────────┘    │  │  └─────────────────────────┘    │   │
│  └─────────────────────────────────┘  └─────────────────────────────────┘   │ 
│                                  │                         │                │
│                          HTTPS API Calls           HTTP Requests            │
└──────────────────────────────────┼─────────────────────────┼────────────────┘
                                   ├─────────────────────────┤
┌──────────────────────────────────▼─────────────────────────▼──────────────┐
│                    UNIFIED API GATEWAY / ORCHESTRATION                    │
│            • Handles both Telegram webhooks and HTTP requests             │
│            • Normalizes input from different interfaces                   │
└──────────────────────────────────────┼────────────────────────────────────┘
                                       │ Normalized Request
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                          AI AGENT ORCHESTRATION LAYER                       │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │                       Concierge Agent                             │      │
│  │  (LangChain RouterChain)                                          │      │
│  │  • Routes queries to appropriate specialist agent                 │      │
│  │  • Uses LLM-based routing decision making                         │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│          ┌───────────────────────────┼───────────────────────────┐          │
│          │                           │                           │          │
│  ┌───────▼───────┐         ┌─────────▼─────────┐       ┌─────────▼─────────┐│
│  │ Onboarding    │         │ Learning Agent    │       │ Career Agent      ││
│  │ Agent         │         │                   │       │                   ││
│  │ • Company Q&A │         │ • Learning recs   │       │ • Career guidance ││
│  │ • Policies    │         │ • Skills          │       │ • Goal setting    ││
│  │ • Procedures  │         │ • Course advices  │       │ • Performance     ││
│  └───────┬───────┘         └───────────────────┘       └───────────────────┘│
└──────────┼───────────────────────────────────────────────────────┼──────────┘
           │ Query with context                                    │ Direct LLM call
┌──────────▼───────────────────────────────────────────────────────▼──────────┐
│                          CORE AI INFRASTRUCTURE                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    Local LLM (Ollama)                               │    │
│  │  • Model: llama3/mistral/deepseek-r1                                │    │
│  │  • Provides intelligence for all agents                             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                      │
│                          ┌───────────▼───────────┐                          │
│                          │   Embeddings Engine   │                          │
│                          │  (OllamaEmbeddings)   │                          │
│                          │ • Text to vector      │                          │
│                          └───────────┬───────────┘                          │
│                          ┌───────────▼───────────┐                          │
│                          │   Vector Database     │                          │
│                          │     (Chroma DB)       │                          │
│                          └───────────┬───────────┘                          │
└──────────────────────────────────────┼──────────────────────────────────────┘
                                       │ Query/Store vectors
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                         DOCUMENT PROCESSOR                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │               Multi-format Document Processor                       │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │    │
│  │  │   PDF       │  │   DOCX      │  │   Excel,CSV │  │   PPT       │ │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────┼──────────────────────────────────────┘
                                       │ Processed documents
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                         COMPANY DATA REPOSITORY                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                   ./company_data/                                   │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │    │
│  │  │   PDF       │  │   DOCX      │  │   XLSX/CSV  │  │   PPT       │ │    │
│  │  │ Documents   │  │ Documents   │  │ Documents   │  │ Documents   │ │    │
│  │  │ • Policies  │  │ • Guides    │  │ • Data      │  │ • Decks     │ │    │
│  │  │ • Manuals   │  │ • Reports   │  │ • Sheets    │  │ • Slides    │ │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```
## Features

### Multi-Agent System
- **Concierge Agent**: Intelligently routes queries to specialized agents
- **Onboarding Agent**: RAG-enabled assistant for company-specific questions
- **Learning Agent**: Personalized learning recommendations
- **Career Coach Agent**: Long-term career development guidance

### User Interfaces
- **Web Interface**: Streamlit-based chat application with profile management
- **Telegram Bot**: Conversational interface accessible via Telegram
- **API Gateway**: RESTful API for custom integrations

### Document Processing
- Multi-format support (PDF, DOCX, Excel, CSV, PPT, TXT, MD)
- Automatic text extraction and chunking
- Vector storage for semantic search

### Privacy & Security
- 100% local processing with Ollama
- No data sent to external APIs
- Company data stays within your infrastructure

## Prerequisites

- **Python 3.9+** with required packages
- **Ollama** running locally on port 11434
- **Git** (for cloning the repository)
- **Telegram Bot Token** from BotFather (optional, for Telegram interface)

## Quick Start


### Clone the repository
```shell
git clone https://github.com/yourusername/CareerCatalyst.git
cd CareerCatalyst
```
### Create virtual environment (recommended)
```shell
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### Install dependencies
```shell
pip install -r requirements.txt
```
### Set up company documents
```shell
mkdir -p company_data
```
### Copy your company documents into `company_data/`

### Initialize the knowledge base
```shell
python rag_setup.py
```

## Detailed Setup Guide

### Step 1: Start Ollama in Terminal #1
```shell
ollama serve
```
In another terminal, pull the required model:
```shell
ollama pull llama3
```
or
```shell 
ollama pull mistral 
```
or
```shell
ollama pull deepseek-r1
```

### Step 2: Prepare Company Documents
Place your company documents in the `./company_data/` directory:
```
company_data/
├── employee_handbook.pdf
├── onboarding_guide.docx
├── training_catalog.xlsx
├── career_paths.pptx
├── policies_and_procedures.pdf
└── ...
```
### Step 3: Initialize RAG System
```shell
python rag_setup.py
```
This will:
   - Process all documents in ./company_data/
   - Create embeddings using Ollama
   - Store vectors in Chroma DB (./chroma_db_company/)

### Step 4: Start the Services in Terminal #2,#3 and #4
#### Terminal  #2 - API Gateway:
```shell
python -m uvicorn api_gateway:app --reload --port 8000
```
#### Terminal #3 - Web Interface:
```shell
streamlit run web_app.py
```
#### Terminal #4 - Telegram Bot (Optional):
First, configure your bot token in telegram_app.py
```shell
python telegram_app.py
```

## Usage Guide

### Web Interface
- Open http://localhost:8501 in your browser
- Set up your profile in the sidebar (role and interests)
- Start chatting with CareerCatalyst
- Use quick action buttons for common topics

### Telegram Bot
- Find your bot on Telegram (using the username you set with BotFather)
- Send `/start` to begin
- Follow the prompts to set up your profile
- Ask questions directly or use commands:
  - `/onboarding` - Ask about company policies
  - `/learning` - Get learning recommendations
  - `/career` - Career guidance
  - `/help` - Show help

### API Gateway
#### Health check
```shell
curl http://localhost:8000/health
```
#### Chat endpoint
```shell
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What training programs are available?",
    "user_id": "user123",
    "role": "Software Engineer",
    "interests": "machine learning, cloud computing"
  }'
```  
## Project Structure
```
CareerCatalyst/
├── agents.py                 # Multi-agent system implementation
├── api_gateway.py            # FastAPI gateway
├── document_processor.py     # Multi-format document processor
├── rag_setup.py              # RAG system initialization
├── web_app.py                # Streamlit web interface
├── telegram_app.py           # Telegram bot implementation
├── check_requirements.py     # Dependency verification script
├── requirements.txt          # Python dependencies
├── company_data/             # Your company documents (create this)
├── chroma_db_company/        # Vector database (auto-generated)
├── README.md                 # This file
├── LICENSE                   # MIT License
├── NOTICE.md                 # Third-party notices
├── CONTRIBUTING.md           # Contribution guidelines
└── ACKNOWLEDGMENTS.md        # Project acknowledgments
```
## Configuration

### Changing the LLM Model
In agents.py, modify the model parameter:
```python
self.llm = Ollama(base_url="http://localhost:11434", model="mistral")  # or deepseek-r1
```
### Adjusting Retrieval Settings
In agents.py, modify the retriever configuration:
```python
self.retriever = self.vector_db.as_retriever(
    search_kwargs={"k": 10}  # Number of documents to retrieve
)
```

### Telegram Bot Token
In telegram_bot.py, replace the token:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_FROM_BOTFATHER"
```


## Sample Documents & Disclaimer

The `company_data/` directory contains sample/fictional documents for demonstration purposes:

Sample Documents Included
- `Corporate flexible work policy.md` - Sample flexible work policy
- `Corporate work sites.docx` - Work site definitions
- `Corporate-Code-of-Conduct.pdf` - Code of conduct template
- `Employee_Onboarding_Resources.pdf` - Onboarding resources
- `Employee_Benefits_Handbook.pdf` - Benefits information
- `Employee_Learning_Resources.pdf` - Learning resources
- `How to deliver a good presentation.pptx` - Presentation template
- `hr_policy.txt` - HR policy sample
- `it_setup.pdf` - IT setup instructions
- `Location Employee Number.xlsx` - Employee data sample
- `Career Guide.txt` - Career guide sample


## Contributing
I welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License & Acknowledgments
### License
Copyright © 2025-present `C.J Mei`. 
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

### Third-Party Dependencies
*CareerCatalyst* stands on the shoulders of giants. I acknowledge and thank all open-source projects that make this possible:

| Project | License | Purpose |
|---------|---------|---------|
| LangChain | 	MIT | 	AI agent orchestration |
| Streamlit | 	Apache 2.0 | 	Web interface |
| FastAPI | 	MIT | 	API gateway |
| Ollama | 	MIT | 	Local LLM inference |
| Chroma DB | 	Apache 2.0 | 	Vector storage |
| python-telegram-bot | 	LGPLv3 | 	Telegram integration |
| PyPDF2 | 	BSD | 	PDF processing |
| pandas | 	BSD | 	Data processing |

For a complete list, see [NOTICE.md](NOTICE.md).

## Project Origin
*CareerCatalyst* was initially developed as a personal hands-on project with the vision to democratize career development support using cutting-edge AI technology.

## Contact
- Project Maintainer: *`C.J Mei`* - chaojunmei8@163.com
- GitHub Issues: https://github.com/meiGitLab/CareerCatalyst/issues
- Project Board: https://github.com/meiGitLab/CareerCatalyst/projects

## Star History
If you find this project useful, please consider giving it a star on GitHub!