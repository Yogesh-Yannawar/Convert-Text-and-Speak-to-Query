from flask import Flask, render_template, request, jsonify
import os
import sys
from pathlib import Path
import sqlite3

# Get the absolute path of the current directory
BASE_DIR = Path(__file__).resolve().parent

# Force load .env from the same directory as this script
from dotenv import load_dotenv
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

print("\n" + "="*60)
print("🔍 Environment Loading Debug Info")
print("="*60)
print(f"📁 Script directory: {BASE_DIR}")
print(f"📁 .env path: {env_path}")
print(f"📄 .env exists: {env_path.exists()}")

# Get API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    print(f"✅ GROQ_API_KEY loaded: {GROQ_API_KEY[:10]}...{GROQ_API_KEY[-4:]}")
else:
    print("❌ GROQ_API_KEY not found!")
    print("\n💡 Please check your .env file:")
    print(f"   Location: {env_path}")
    print(f"   Content should be: GROQ_API_KEY=your_actual_key")
print("="*60 + "\n")

app = Flask(__name__)

# Initialize Groq client
client = None
try:
    from groq import Groq
    
    if not GROQ_API_KEY:
        print("⚠️  WARNING: GROQ_API_KEY is empty or None")
    else:
        # Try to initialize with the key
        client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq client initialized successfully\n")
        
except Exception as e:
    print(f"❌ Error initializing Groq client: {e}\n")

def text_to_sql(question):
    """Convert natural language to SQL using Groq"""
    if not client:
        return "Error: Groq API client not initialized. Check your API key in .env file."
    
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY is not set. Check your .env file."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are a SQL expert. Convert natural language questions to SQL queries.
                    
Database Schema:
- Table name: STUDENT
- Columns: NAME (text), CLASS (text), SECTION (text), MARKS (integer)

Rules:
- Return ONLY the SQL query, no explanations
- Use proper SQL syntax
- Table name is STUDENT (uppercase)"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        sql_query = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        return sql_query
        
    except Exception as e:
        return f"Error: {str(e)}"

def execute_query(sql):
    """Execute SQL query on the database"""
    try:
        # Use absolute path for database
        db_path = BASE_DIR / 'student.db'
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        conn.close()
        
        return {"columns": columns, "data": results, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/converter')
def converter():
    return render_template('converter.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({"error": "Please enter a question"}), 400
    
    if not client:
        return jsonify({
            "error": "API client not initialized. Please ensure:\n1. .env file exists\n2. GROQ_API_KEY is set correctly\n3. Restart the server"
        }), 500
    
    # Generate SQL
    sql_query = text_to_sql(question)
    
    if sql_query.startswith("Error"):
        return jsonify({"error": sql_query}), 400
    
    # Execute query
    result = execute_query(sql_query)
    
    return jsonify({
        "sql": sql_query,
        "result": result
    })

if __name__ == '__main__':
    print("="*60)
    print("🔹 Text to SQL Converter - Starting Server 🔹")
    print("="*60)
    
    # Check database
    db_path = BASE_DIR / 'student.db'
    if db_path.exists():
        print(f"✅ Database found: {db_path}")
    else:
        print(f"⚠️  WARNING: Database not found at {db_path}")
        print(f"   Run: python setup_database.py")
    
    # Final check
    if GROQ_API_KEY and client:
        print("✅ All systems ready!")
    else:
        print("❌ System not ready - check errors above")
    
    print("\n🌐 Server starting at: http://localhost:5000")
    print("📖 Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000, use_reloader=False)
