from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Path to your unsubscribe list (or replace with DB)
UNSUBSCRIBE_FILE = "unsubscribed_emails.txt"

# Simple email validation
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route('/api/unsubscribe', methods=['POST'])
def unsubscribe():
    data = request.get_json()
    email = data.get('email')

    if not email or not is_valid_email(email):
        return jsonify({"error": "Invalid email"}), 400

    # Save email to file if not already there
    try:
        with open(UNSUBSCRIBE_FILE, "a+") as f:
            f.seek(0)
            existing = f.read().splitlines()
            if email not in existing:
                f.write(email + "\n")
        return jsonify({"message": f"{email} unsubscribed successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
