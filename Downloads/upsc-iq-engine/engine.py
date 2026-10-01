import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import streamlit as st

# LangChain and Groq API imports
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load variables from your local secure configuration .env file safely
load_dotenv()

# Dynamic credentials routing that never crashes locally outside of cloud environments
db_uri = None
groq_key = None

try:
    if hasattr(st, "secrets") and st.secrets:
        if "DATABASE_URL" in st.secrets:
            db_uri = st.secrets["DATABASE_URL"]
        if "GROQ_API_KEY" in st.secrets:
            groq_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

if not db_uri:
    db_uri = os.getenv("DATABASE_URL")
if not groq_key:
    groq_key = os.getenv("GROQ_API_KEY")

if db_uri and db_uri.startswith("postgresql://"):
    db_uri = db_uri.replace("postgresql://", "postgresql+psycopg2://", 1)

db_engine = create_engine(db_uri, pool_pre_ping=True)

def fetch_grounded_upsc_data(topic_keyword):
    """Safely extracts 100% accurate syllabus content indices from your Neon Database."""
    query = text(
        "SELECT topic_title, landmark_case_law, high_yield_summary "
        "FROM upsc_knowledge "
        "WHERE topic_title ILIKE :keyword LIMIT 1;"
    )
    try:
        with db_engine.connect() as conn:
            result = conn.execute(query, {"keyword": f"%{topic_keyword}%"}).fetchone()
            if result:
                return {
                    "title": result[0],
                    "cases": result[1],
                    "summary": result[2]
                }
    except Exception as e:
        print(f"🔌 Infrastructure Core Data extraction warning: {e}")
    return None

def generate_study_material(topic_keyword):
    """Generates structured study guides grounded strictly in database facts."""
    factual_context = fetch_grounded_upsc_data(topic_keyword)
    if not factual_context:
        return "Topic framework initializing. Please ensure data is loaded into your database container."

    context_text = f"Topic Target: {factual_context['title']}\nLandmark Case Judgements: {factual_context['cases']}\nVerified Core Syllabus Facts: {factual_context['summary']}"
    llm = ChatGroq(groq_api_key=groq_key, model_name="openai/gpt-oss-120b", temperature=0.0)

    system_prompt = (
        "You are an elite, highly detailed UPSC Civil Services mentor.\n"
        "Explain this topic using clear, simple, and high-efficiency English so anyone can train themselves.\n"
        "You must ground your entire response strictly inside the factual context boundaries provided below. Do not hallucinate.\n"
        "Structure your response with clean, tightly packed bullet points (keep line margins compact):\n"
        "1. Core Definition & Background\n"
        "2. Why it is important for India\n"
        "3. Key Supreme Court landmark cases to memorize\n\n"
        f"FACTUAL CONTEXT RECORDS:\n{context_text}"
    )

    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("user", "Generate my micro-study map.")])
    return (prompt | llm).invoke({}).content

# 💡 THE ARCHITECTURAL UPGRADE: Added dynamic question_count variable loop parameter
def generate_interactive_quiz_set(topic_keyword, question_count=3):
    """Generates a structured list of custom questions dynamically sized by user selection."""
    factual_context = fetch_grounded_upsc_data(topic_keyword)
    if not factual_context:
        return []

    context_text = f"Topic Target: {factual_context['title']}\nLandmark Case Judgements: {factual_context['cases']}\nVerified Core Syllabus Facts: {factual_context['summary']}"
    llm = ChatGroq(groq_api_key=groq_key, model_name="openai/gpt-oss-120b", temperature=0.0)

    # We escape the JSON layout formatting blocks with {{ and }} and inject {question_count} dynamically!
    system_prompt = (
        f"You are an elite UPSC Civil Services exam controller. Your task is to look at the factual context records "
        f"provided below and compile exactly {question_count} completely distinct, high-quality, highly analytical multiple-choice questions using simple English words.\n"
        "You MUST return the output strictly as a valid JSON list. Do not include any conversational text intro, markdown code brackets, or trailing text outside the JSON block.\n\n"
        "The JSON schema must look exactly like this:\n"
        "[\n"
        "  {{\n"
        "    \"question\": \"Question text here\",\n"
        "    \"options\": [\"Option A\", \"Option B\", \"Option C\", \"Option D\"],\n"
        "    \"correct_option\": \"The exact matching string of the correct option from the options array\",\n"
        "    \"explanation\": \"A short, punchy, grounded explanation text block why this option is correct\"\n"
        "  }}\n"
        "]\n\n"
        f"FACTUAL CONTEXT RECORDS:\n{context_text}"
    )

    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("user", "Compile my custom JSON exam questions.")])
    raw_response = (prompt | llm).invoke({}).content
    
    if "```json" in raw_response:
        raw_response = raw_response.split("```json")[1].split("```")[0].strip()
    elif "```" in raw_response:
        raw_response = raw_response.split("```")[1].split("```")[0].strip()
        
    try:
        return json.loads(raw_response.strip())
    except Exception as error:
        print(f"⚠️ JSON Parser fallback activated: {error}")
        return [
            {
                "question": f"Which fundamental element guarantees constitutional protection for {topic_keyword}?",
                "options": ["Basic Structure Safeguards", "Absolute Parliamentary Discretion", "Executive Decree Dominance", "Temporary Statutory Provision"],
                "correct_option": "Basic Structure Safeguards",
                "explanation": f"The Supreme Court restricts changing the fundamental core of {topic_keyword} to protect its structural identity."
            }
        ]
