import os
"""
Simple test to verify your Groq API key works
"""

# Manually set your API key here for testing
# Replace 'YOUR_KEY_HERE' with your actual Groq API key
TEST_API_KEY =  os.getenv("GROQ_API_KEY")  # <-- PUT YOUR ACTUAL KEY HERE

print("\n" + "="*60)
print("🧪 GROQ API KEY TEST")
print("="*60 + "\n")

# Test 1: Check if key is set
if TEST_API_KEY == "YOUR_KEY_HERE":
    print("❌ ERROR: You need to edit this file and put your real API key")
    print("   Open this file in Notepad and replace 'YOUR_KEY_HERE'")
    print("   with your actual Groq API key (starts with gsk_)")
    print("\n" + "="*60 + "\n")
    exit()

print(f"1️⃣ API Key provided")
print(f"   Length: {len(TEST_API_KEY)} characters")
print(f"   Starts with: {TEST_API_KEY[:10]}...")
print(f"   Ends with: ...{TEST_API_KEY[-4:]}")

if TEST_API_KEY.startswith("gsk_"):
    print("   ✅ Format looks correct (starts with gsk_)")
else:
    print("   ⚠️  Warning: Key doesn't start with 'gsk_'")

print()

# Test 2: Try to import groq
print("2️⃣ Testing groq module...")
try:
    from groq import Groq
    print("   ✅ groq module imported successfully")
except ImportError as e:
    print(f"   ❌ groq module not found: {e}")
    print("   💡 Install it: pip install groq==0.11.0")
    exit()

print()

# Test 3: Initialize client
print("3️⃣ Initializing Groq client...")
try:
    client = Groq(api_key=TEST_API_KEY)
    print("   ✅ Client initialized successfully")
except Exception as e:
    print(f"   ❌ Failed to initialize: {e}")
    exit()

print()

# Test 4: Make a simple API call
print("4️⃣ Testing API call...")
try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": "Say 'Hello' in one word"
            }
        ],
        max_tokens=10
    )
    
    result = response.choices[0].message.content
    print(f"   ✅ API call successful!")
    print(f"   Response: {result}")
    
except Exception as e:
    print(f"   ❌ API call failed: {e}")
    print("\n   Common issues:")
    print("   - Invalid API key")
    print("   - No credits/quota remaining")
    print("   - Network connection issue")
    exit()

print()
print("="*60)
print("🎉 SUCCESS! Your API key is working perfectly!")
print("="*60)
print("\nNow you can use it in your app. Copy this key to your .env file:")
print(f"\nGROQ_API_KEY={TEST_API_KEY}")
print("\n" + "="*60 + "\n")
