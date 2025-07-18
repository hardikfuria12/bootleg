from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Load backend URL from environment variable
NGROK_BACKEND_URL = os.environ.get('NGROK_BACKEND_URL')
print("🔧 NGROK_BACKEND_URL =", NGROK_BACKEND_URL)

@app.route('/', methods=['GET'])
def upload_form():
    return render_template('upload.html')

@app.route('/submit', methods=['POST'])
def submit():
    file = request.files.get('file')
    username = request.form.get('username')
    password = request.form.get('password')

    if not file:
        print("🚫 No file received")
        return "No file received", 400

    print(f"📦 Received file: {file.filename}, type: {file.content_type}")

    files = {
        'file': (file.filename, file.stream, file.mimetype)
    }

    try:
        response = requests.post(
            f"{NGROK_BACKEND_URL}/receive_login",
            data={'username': username, 'password': password},
            files=files
        )

        if response.status_code != 200:
            return f"Backend error: {response.text}", 500

        data = response.json()

        return render_template(
            "result.html",
            user_id=data['user_id'],
            table_html=data['table_html'],
            sales_clean_html=data['sales_clean_html'],
            sales_dirty_html=data.get('sales_dirty_html'),  # Might be None
        )

    except requests.exceptions.RequestException as e:
        print("❌ Backend unreachable:", e)
        return f"Backend unreachable: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
