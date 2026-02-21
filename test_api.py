import google.generativeai as genai

# Paste your key here
genai.configure(api_key="AIzaSyCvydkaMYRIva7jR5AZ2vZbUi9az-93ncY")
model = genai.GenerativeModel('gemini-1.5-flash')

try:
    response = model.generate_content("Say 'API is working!'")
    print(response.text)
except Exception as e:
    print(f"Still not working. Error: {e}")