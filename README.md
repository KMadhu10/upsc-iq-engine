# 🎓 UPSC-IQ Exam Intelligence Hub

An enterprise-grade, context-grounded AI self-training simulator and adaptive quiz generation engine designed for the UPSC Civil Services Examination. This system leverages a zero-temperature Retrieval-Augmented Generation (RAG) framework connected directly to a serverless, globally distributed relational cluster to deliver 100% accurate, hallucination-free study roadmaps and dynamic testing modules.

---

## 🏗️ System Architecture & Data Flow

```text
  [STUDENT WORKSPACE FRONTEND] 🖥️ (Streamlit UI Enclave with Navy-Blue Grid Custom CSS)
               │
               ▼
  [CONTROL PARAMETERS BOARD]  ⚙️ (Syllabus Topic Selectbox + Dynamic Question Count Slider)
               │
               ▼
  [ORCHESTRATION LAYER]       🔌 (SQLAlchemy Core Engine Connection Pool Handler)
               │
               ▼
  [CLOUD DATA ASSET VAULT]    🗄️ (Neon Serverless PostgreSQL Database Infrastructure)
               │                  └─► Fetch 100% Accurate Context (ILIKE Keyword Queries)
               ▼
  [INFERENCE LOGIC MATRIX]    🧠 (LangChain Prompt Pipeline Layer + Groq Cloud API Engine)
               │                  └─► Process Zero-Temperature Deterministic Code Execution
               ▼
  [INTERACTIVE RADIO CANVASES] 📊 (State-Tracked Quiz Console w/ Session State Token Storage)
```

---

## 🛠️ Technical Capabilities & Structural Implementations

*   **Syllabus-Grounded Retrieval (Anti-Hallucination):** Bypasses standard LLM factual drift by querying serverless PostgreSQL instances first. The system wraps legal text blocks, case judgments, and summaries into tight context boundary windows before invoking inference models.
*   **Dynamic Multi-Question JSON Matrix Parsing:** Orchestrates a prompt framework that forces the cloud API to yield structured, executable JSON arrays containing precise multiple-choice tokens, correct matching fields, and verbose diagnostic explanations.
*   **Stateful UI Progression Tracking:** Leverages local session state pointers (`st.session_state`) to maintain active state memory tracking user options, score tallies, and horizontal progression streams across a 3-to-10 question array loop.
*   **High-Yield Automated Ingestion Daemon:** Features a robust Python-driven bulk uploader (`uploader.py`) that handles line-by-line parsing of structured local notebook sheets to stream batch entries to relational tables instantly via database transactions.

---

## 🗄️ Relational Database Schema Design

The core knowledge base is anchored inside a highly optimized PostgreSQL relational schema optimized for semantic search keyword operations:

```sql
CREATE TABLE upsc_knowledge (
    module_id SERIAL PRIMARY KEY,
    subject_tag VARCHAR(100) NOT NULL,
    topic_title VARCHAR(150) NOT NULL,
    official_syllabus_context TEXT NOT NULL,
    landmark_case_law TEXT,
    high_yield_summary TEXT NOT NULL
);
```

---

## 🚀 Execution & Setup Deployment Walkthrough

### 1. Local Workspace Initialization
```bash
# Clone and enter the repository folder root
cd Downloads/upsc-iq-engine

# Initialize and toggle the virtual environment box
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate

# Install the dependencies matrix
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a secure `.env` file inside your local workspace directory:
```env
DATABASE_URL="postgresql+psycopg2://<user>:<password>@<host>/upsc-exam-intelligence-db"
GROQ_API_KEY="gsk_your_secure_production_cloud_api_token_string"
```

### 3. Bulk Data Sanitation Ingestion
Stream raw textual notebook blocks right into your serverless cloud repository:
```bash
python uploader.py
```

### 4. Booting the Application UI Server
```bash
python -m streamlit run app.py
```

---

## 🛡️ Core FDE Technical Talking Points (Interview-Ready)

*   **Pessimistic Connection Pooling Handling:** Implements `pool_pre_ping=True` within the SQLAlchemy dialect layer. Every user transaction executes a 1ms heartbeat ping to verify the socket state. If a serverless compute cluster drop occurs due to idle sleep timeout blocks, the driver automatically drops the dead port channel and mounts a fresh handshake cleanly without triggering front-facing UI exceptions.
*   **LangChain Double-Curly Brace Variable Escaping:** Resolves the critical `INVALID_PROMPT_INPUT` loop error. To feed structured JSON formatting requirements to the system instructions without confusing LangChain's string parsing variable mappers, raw braces were doubled (`{{` and `}}`) to securely split textual directives from active input keys.
*   **Compact UI Line-Height Packing:** Utilizes customized target CSS injections to override default markdown parameters. By explicitly constraining paragraph and item layout margins to tight pixel properties, textual notes render in an exceptionally readable, dense framework optimized for reading core materials.
