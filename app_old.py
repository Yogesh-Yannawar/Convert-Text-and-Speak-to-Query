# from flask import Flask, render_template, request, jsonify
# from groq import Groq
# import os
# from dotenv import load_dotenv
# import sqlite3

# load_dotenv()

# app = Flask(__name__)
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def text_to_sql(question):
#     """Convert natural language to SQL using Groq"""
#     try:
#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": """You are a SQL expert. Convert natural language questions to SQL queries.
                    
# Database Schema:
# - Table name: STUDENT
# - Columns: NAME (text), CLASS (text), SECTION (text), MARKS (integer)

# Rules:
# - Return ONLY the SQL query, no explanations
# - Use proper SQL syntax
# - Table name is STUDENT (uppercase)"""
#                 },
#                 {
#                     "role": "user",
#                     "content": question
#                 }
#             ],
#             temperature=0.1,
#             max_tokens=200
#         )
        
#         sql_query = response.choices[0].message.content.strip()
#         sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
#         return sql_query
        
#     except Exception as e:
#         return f"Error: {str(e)}"

# def execute_query(sql):
#     """Execute SQL query on the database"""
#     try:
#         conn = sqlite3.connect('student.db')
#         cursor = conn.cursor()
#         cursor.execute(sql)
#         results = cursor.fetchall()
        
#         # Get column names
#         columns = [description[0] for description in cursor.description]
#         conn.close()
        
#         return {"columns": columns, "data": results, "success": True}
#     except Exception as e:
#         return {"error": str(e), "success": False}

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/converter')
# def converter():
#     return render_template('converter.html')

# @app.route('/convert', methods=['POST'])
# def convert():
#     data = request.json
#     question = data.get('question', '')
    
#     if not question:
#         return jsonify({"error": "Please enter a question"}), 400
    
#     # Generate SQL
#     sql_query = text_to_sql(question)
    
#     if sql_query.startswith("Error"):
#         return jsonify({"error": sql_query}), 400
    
#     # Execute query
#     result = execute_query(sql_query)
    
#     return jsonify({
#         "sql": sql_query,
#         "result": result
#     })

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)



from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import sqlite3

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client with error handling
try:
    from groq import Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("⚠️  WARNING: GROQ_API_KEY not found in .env file")
        client = None
    else:
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Groq client: {e}")
    client = None

def text_to_sql(question):
    """Convert natural language to SQL using Groq"""
    if not client:
        return "Error: Groq API client not initialized. Check your API key."
    
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
        conn = sqlite3.connect('student.db')
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
        return jsonify({"error": "API client not initialized. Please check your GROQ_API_KEY in .env file"}), 500
    
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
    print("\n" + "="*50)
    print("🔹 Text to SQL Converter - Starting Server 🔹")
    print("="*50)
    
    # Check if database exists
    if os.path.exists('student.db'):
        print("✅ Database found: student.db")
    else:
        print("⚠️  WARNING: student.db not found. Run 'python setup_database.py' first")
    
    # Check API key
    if os.getenv("GROQ_API_KEY"):
        print("✅ GROQ_API_KEY loaded from .env")
    else:
        print("⚠️  WARNING: GROQ_API_KEY not found in .env file")
    
    print("\n🌐 Server starting at: http://localhost:5000")
    print("📖 Press CTRL+C to stop the server\n")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)

