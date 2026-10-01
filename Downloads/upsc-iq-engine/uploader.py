import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load credentials securely from the local .env enclave configuration
load_dotenv()
db_uri = os.getenv("DATABASE_URL")

if db_uri and db_uri.startswith("postgresql://"):
    db_uri = db_uri.replace("postgresql://", "postgresql+psycopg2://", 1)

# Connect a managed database connection engine cluster instance configuration
db_engine = create_engine(db_uri)

def execute_bulk_syllabus_ingestion():
    """Reads a structural notebook layout text asset and streams everything to Neon Cloud Postgres."""
    if not os.path.exists("syllabus_source.txt"):
        print("❌ Ingestion Error: Missing syllabus_source.txt input file asset.")
        return

    print("📖 Reading localized text data blocks matrix...")
    with open("syllabus_source.txt", "r", encoding="utf-8") as file:
        raw_data = file.read()
        
    # Split individual database rows divided by our clean operational dashes divider
    data_chunks = raw_data.split("---")
    
    insertion_query = text("""
        INSERT INTO upsc_knowledge (subject_tag, topic_title, official_syllabus_context, landmark_case_law, high_yield_summary)
        VALUES (:tag, :title, :context, :cases, :summary)
        ON CONFLICT DO NOTHING;
    """)
    
    record_count = 0
    
    with db_engine.connect() as conn:
        with conn.begin(): # Open a secure operational database transaction parameters line
            for chunk in data_chunks:
                if not chunk.strip():
                    continue
                # Parse out the explicit table columns divided by our custom triple pipe characters matrix
                column_tokens = chunk.strip().split("|||")
                if len(column_tokens) == 5:
                    conn.execute(insertion_query, {
                        "tag": column_tokens[0].strip(),
                        "title": column_tokens[1].strip(),
                        "context": column_tokens[2].strip(),
                        "cases": column_tokens[3].strip(),
                        "summary": column_tokens[4].strip()
                    })
                    record_count += 1
                    
    print(f"🚀 SUCCESS: Bulk Data Sync Complete! {record_count} comprehensive syllabus rows injected smoothly to Neon.")

if __name__ == "__main__":
    execute_bulk_syllabus_ingestion()
