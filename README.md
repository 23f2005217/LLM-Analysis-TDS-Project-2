---
title: LLM Analysis Quiz Solver
sdk: docker
app_port: 7860
---

# LLM Analysis - Autonomous Quiz Solver Agent

An intelligent, autonomous agent built with LangGraph and LangChain that solves data-related quizzes involving web scraping, data processing, analysis, and visualization tasks.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/saivijayragav/LLM-Analysis-TDS-Project-2.git
cd LLM-Analysis-TDS-Project-2
```

### 2. Environment Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Open `.env` and fill in your details.

### 3. Get API Keys

You will need the following API keys:

- **IITM Token**: Get it from [https://aipipe.org/login](https://aipipe.org/login)
- **Gemini API Key**: Get it from [https://aistudio.google.com/](https://aistudio.google.com/)
- **Vertex API Key**: Get it from [https://console.cloud.google.com/vertex-ai/studio/settings/api-keys](https://console.cloud.google.com/vertex-ai/studio/settings/api-keys)

Update your `.env` file with these keys:

```env
IITM_API_KEY=your_token_here
GEMINI_API_KEY=your_gemini_key_here
VERTEX_API_KEY=your_vertex_key_here
EMAIL=your_email
SECRET=your_secret
```

### 4. Install Dependencies

Using `uv` (Recommended):

```bash
# Install uv if needed
pip install uv

# Sync dependencies
uv sync
uv run playwright install chromium
```

Using `pip`:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -e .
playwright install chromium
```

## Usage

Start the server:

```bash
uv run main.py
```

The server will start at `http://0.0.0.0:7860`.

### Test the Endpoint

You can test the agent with a curl command:

```bash
curl -X POST http://localhost:7860/solve \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your_email",
    "secret": "your_secret",
    "url": "https://tds-llm-analysis.s-anand.net/demo"
  }'
```