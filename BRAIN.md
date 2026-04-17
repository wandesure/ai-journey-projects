# BRAIN.md — Wande's AI Skills Journey
*Ground truth for this project. Read this first every session.*

---

## WHO I AM
- **Name:** Wande Oluwatomi
- **Location:** Calgary, Alberta, Canada
- **Current role:** Senior Security Consultant at TELUS
- **Credentials:** CISSP | CCSP | CGRC | PMP
- **Goal:** Transition from pure security consulting to AI-powered security + compliance tools — freelance, employment, and product income streams

---

## THE JOURNEY
- **Programme:** Structured 40-week AI Skills Journey (started Week 1, Week 8 complete, starting Week 9)
- **Starting point:** Zero prior programming experience
- **Learning style:** Socratic method — concepts before code, explain every line before typing, no rabbit holes
- **Sessions:** Saturday/Sunday 2-3 hours, weekdays 1.5-2 hours
- **Tutor:** Claude (claude.ai) — Socratic approach, tough love, no fluff

---

## CURRENT STATUS — Week 8 COMPLETE, Week 9 READY
- **Phase:** Deployment + Claude Code + MCP (complete) — moving to Authentication + Monetisation
- **Live product:** AI Document Intelligence Hub (3 tabs)
- **Live URL:** https://ai-journey-projects-4njztxymtqnlphnqshqsnc.streamlit.app
- **GitHub:** github.com/wandesure/ai-journey-projects (public, 37+ commits)

---

## WHAT HAS BEEN BUILT (in order)
### Phase 1-2: Foundations (Weeks 1-2)
- Claude 101 certification
- Introduction to AI (Elements of AI) certification
- Prompt Engineering mastery

### Phase 3: Python + Claude API (Weeks 3-4)
- `my_first_ai.py` — First Claude API call
- `study_assistant.py` — AI study tool with system prompts
- `ai_job_helper.py` — Work assistant with conversation loop
- `chatbot.py` — Multi-turn chatbot with conversation memory
- `file_reader.py` — File processing with encoding support
- `summariser.py` — Document Q&A with follow-up capability

### Phase 3 continued: AI Agents + Tool Use (Week 5)
- `calculator_agent.py` — Single tool agent
- `multi_tool_agent.py` — Three tool agent with router function
- `compliance_checker.py` — AI security compliance analyser (NIST, ISO 27001, CIS, SOC 2) with follow-up Q&A — polished and employer ready
- `search_agent.py` — Real-time web search agent
- `super_agent.py` — Four tool super agent

### Phase 4: RAG + LangChain (Week 6)
- `simple_rag.py` — Keyword RAG with basic chunking
- `doc_intelligence.py` — Semantic RAG with ChromaDB + SentenceTransformers + PDF support + multi-document + 5 industry modes
- `doc_intelligence_lc.py` — LangChain RAG pipeline refactor

### Phase 5: Deployment (Week 7)
- `app.py` — Streamlit web app with Document Q&A + Compliance Checker tabs
- Deployed live on Streamlit Cloud
- Professional branding — "Built by Wande Oluwatomi | AI Developer | Security & Compliance Specialist"

### Phase 6: Claude Code + MCP + UI Polish (Week 8 — COMPLETE)
- Claude Code installed (v2.1.107) and actively used
- CLAUDE.md created via /init
- Document Summariser tab added via Claude Code (one sentence instruction)
- Professional CSS theme applied via Claude Code
- MCP connected — Google Drive accessible from Claude
- App now has THREE tabs — Document Q&A, Compliance Checker, Document Summariser
- LinkedIn post published showcasing live app

---

## TECH STACK
- **OS:** Windows laptop
- **Python:** 3.14 — always use `py` command (never `python` or `python3`)
- **Package install:** `py -m pip install`
- **Editor:** VS Code with Claude Code extension
- **API:** Anthropic Claude API (claude-opus-4-6)
- **Key libraries:** anthropic, streamlit, langchain, chromadb, sentence-transformers, pypdf, python-dotenv
- **Version control:** Git + GitHub
- **Deployment:** Streamlit Cloud (free tier)
- **API key:** stored in .env file (never on GitHub)
- **Claude Code:** installed, used via VS Code terminal and standalone terminal

---

## KEY FILES
- `app.py` — main Streamlit web app (THREE tabs: Document Q&A, Compliance Checker, Document Summariser)
- `compliance_checker.py` — standalone CLI compliance checker
- `doc_intelligence.py` — standalone RAG document assistant
- `doc_intelligence_lc.py` — LangChain version of RAG assistant
- `.streamlit/config.toml` — Streamlit theme (blue #2E75B6 professional theme)
- `CLAUDE.md` — Claude Code project briefing
- `requirements.txt` — deployment dependencies
- `runtime.txt` — forces Python 3.11 on Streamlit Cloud
- `sample_policy.txt` — test security policy document
- `hr_policy.txt` — test HR policy document

---

## PERSONAL CONTEXT
- Works full time at TELUS — sessions fit around job
- Office receiving Anthropic training (introductory level — Wande is ahead)
- French speaker — occasionally says "Merci"
- Motto: "No rest for the weary"
- Personality: ahead of schedule, sharp eye for bugs, asks sharp questions
- Imposter syndrome present but being overcome through building real things
- Goal is NOT to become a pure developer — goal is AI-powered security consultant + product builder + freelancer

---

## LEARNING STYLE — CRITICAL
- **Socratic method** — ask questions, don't dump code
- **Concept before code** — always explain what we're building before typing
- **Explain every line** before it's typed
- **No rabbit holes** — stick to the plan
- **Test locally first** — always test before pushing to GitHub
- **New approach (Week 8+):** Less code transcription, more real problem solving, shorter sessions, Claude Code for heavy lifting

---

## PERSONALITY NOTES FOR TUTOR
- Calls Claude "buddy"
- Signs off with "Merci" sometimes
- Pushes back when Claude gives up too easily (see: Streamlit deployment battle)
- Holds Claude accountable for mistakes ("you told me to comment it out!")
- Responds well to encouragement but dislikes empty praise
- Best motivated by seeing real things work in the browser

---

## IMMEDIATE NEXT STEPS (Week 9)
- Authentication for Streamlit app
- User sessions
- Pricing strategy exploration
- First client outreach preparation

---

## WEEK 8 ACHIEVEMENTS
- Claude Code mastered for rapid development
- MCP integration with Google Drive
- Professional CSS theme applied
- Document Summariser tab shipped
- LinkedIn visibility (post published)
- Three-tab production app live

---

## REFERENCE DOCUMENTS IN PROJECT
- `Claude_API_CheatSheet_v2.docx` — living reference guide (Anthropic keywords, Python errors, agent pattern)
- `Git_GitHub_CheatSheet.docx` — Git commands reference
- `journey_log.txt` — weekly milestone tracker
- Weekly plan documents (Week5, Week6, Week7, Week8)

---

*Last updated: Week 8 complete, ready for Week 9 — 17 April 2026*
*To update: add new milestones, update current status, note any decisions made*
