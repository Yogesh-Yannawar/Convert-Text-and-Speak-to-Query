# 🚀 Quick Start Guide

Follow these simple steps to get your Text to SQL converter running:

## Step 1: Get Groq API Key (2 minutes)

1. Go to https://console.groq.com/
2. Sign up or log in (it's free!)
3. Click on "API Keys" in the sidebar
4. Click "Create API Key"
5. Copy the key (starts with `gsk_`)

## Step 2: Setup Project (2 minutes)

1. **Copy this entire folder to your computer**
   ```
   Copy the text_to_sql_website folder to E:\text_to_sql_website
   ```

2. **Install Python packages**
   ```bash
   cd E:\text_to_sql_website
   pip install -r requirements.txt
   ```

3. **Create .env file**
   - Rename `.env.example` to `.env`
   - Open `.env` and paste your Groq API key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

4. **Create the database**
   ```bash
   python setup_database.py
   ```
   This will create `student.db` with sample data.

## Step 3: Run the Application (1 minute)

1. **Start the server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   - Go to: `http://localhost:5000`
   - You'll see the beautiful homepage!

3. **Try the converter**
   - Click "Try It Now" button
   - Or go directly to: `http://localhost:5000/converter`

## Step 4: Test It Out

Try these example questions:

1. **Simple query**
   ```
   Show all students
   ```

2. **Filter by department**
   ```
   Show all students from Computer department
   ```

3. **Filter by marks**
   ```
   List students with marks greater than 85
   ```

4. **Count records**
   ```
   Count total students in each class
   ```

5. **Top performers**
   ```
   Show top 5 students by marks
   ```

## 🎯 Tips

- **Keyboard Shortcut**: Press `Ctrl+Enter` (Windows) or `Cmd+Enter` (Mac) to convert quickly
- **Copy SQL**: Click the "Copy" button to copy the generated SQL query
- **Clear**: Use the "Clear" button to reset and start fresh
- **Examples**: Click on any example button to auto-fill the question

## 📁 Project Structure

```
E:\text_to_sql_website\
├── app.py                 ← Flask server
├── setup_database.py      ← Creates the database
├── requirements.txt       ← Python packages
├── .env                   ← Your API key (create this!)
├── student.db            ← Database (auto-created)
├── templates\
│   ├── index.html        ← Home page
│   └── converter.html    ← Converter page
└── static\
    ├── css\style.css     ← Styles
    └── js\converter.js   ← JavaScript
```

## ❓ Common Issues

### "No module named 'flask'"
**Solution**: Run `pip install -r requirements.txt`

### "Error code: 401"
**Solution**: Check your Groq API key in `.env` file

### "No such table: STUDENT"
**Solution**: Run `python setup_database.py`

### Port 5000 already in use
**Solution**: 
- Kill the process using port 5000, OR
- Change the port in `app.py`:
  ```python
  app.run(debug=True, port=5001)  # Use 5001 instead
  ```

## 🎉 You're Done!

Your Text to SQL converter is now running! Enjoy converting natural language to SQL queries with AI power!

## 📞 Need Help?

- Check the full README.md for detailed information
- Review the code comments in app.py
- Test with the example queries provided

---

**Estimated Total Setup Time**: 5-10 minutes

Happy querying! 🚀
