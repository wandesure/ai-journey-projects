# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A collection of AI-powered Python projects built as part of a structured AI Skills learning journey. Projects range from basic Claude API calls to production RAG systems and deployed web applications.

**Live Demo**: https://ai-journey-projects-4njztxymtqnlphnqshqsnc.streamlit.app

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI scripts
python <script_name>.py

# Run the Streamlit web app
streamlit run app.py
```

## Environment Setup

All scripts require `ANTHROPIC_API_KEY` in a `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
```

The web app (`app.py`) also supports Streamlit secrets for cloud deployment.

## Architecture

### Project Tiers

**Tier 1 - Basic API Usage**
- `my_first_ai.py`, `study_assistant.py`, `ai_job_helper.py` - Single Claude API calls with system prompts
- `chatbot.py` - Multi-turn conversation with history management (20-message sliding window)
- `file_reader.py`, `summariser.py` - File processing with Claude

**Tier 2 - AI Agents with Tools**
- `calculator_agent.py` - Single tool (calculator using `eval`)
- `multi_tool_agent.py` - Multiple tools with router function
- `search_agent.py` - Web search via DuckDuckGo API
- `super_agent.py` - Combined agent with calculate, word count, web search, and compliance tools

Tool pattern used throughout:
```python
tools = [{"name": "...", "description": "...", "input_schema": {...}}]
# Check response.stop_reason == "tool_use" to detect tool calls
# Extract tool_block from response.content where b.type == "tool_use"
```

**Tier 3 - RAG Systems**
- `simple_rag.py` - Basic RAG with keyword search
- `doc_intelligence.py` - ChromaDB + SentenceTransformers (`all-MiniLM-L6-v2`) for semantic search
- `doc_intelligence_lc.py` - LangChain-based RAG pipeline with `ChatAnthropic`, `Chroma`, `RecursiveCharacterTextSplitter`

Both RAG systems support 5 industry modes (Telecom, Legal, Healthcare, HR, Finance) with specialized system prompts.

**Tier 4 - Web Application**
- `app.py` - Streamlit app with two tabs: Document Q&A and Compliance Checker
- Analyzes policies against NIST SP 800-53, ISO 27001, CIS Controls v8, SOC 2

### Key Dependencies

- `anthropic` - Claude API client (model: `claude-opus-4-6`)
- `streamlit` - Web UI framework
- `chromadb` - Vector database for RAG
- `sentence-transformers` - Embeddings (`all-MiniLM-L6-v2`)
- `langchain*` - LangChain ecosystem for RAG pipeline
- `pypdf` - PDF text extraction
- `python-dotenv` - Environment variable management
