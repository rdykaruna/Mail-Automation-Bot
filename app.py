from flask import Flask, render_template_string, request

app = Flask(__name__)

# This is the "Semester - IV" page you wanted to start with
form_html = """
<html>
<head>
    <title>FXEC Registration Portal</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 350px; text-align: center; }
        h2 { color: #1a73e8; margin-bottom: 1.5rem; }
        input { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #1a73e8; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; margin-top: 10px; }
        button:hover { background-color: #1557b0; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Semester - IV Registration</h2>
        <form action="/confirm" method="POST">
            <input type="text" id="name" name="name" placeholder="Full Name" required>
            <input type="email" id="email" name="email" placeholder="College Email" required>
            <input type="text" id="dept" name="dept" placeholder="Department" required>
            <button type="submit" id="register_btn">Register Now</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/') # Now the main link goes straight to the form
def registration_page():
    return render_template_string(form_html)

@app.route('/confirm', methods=['POST'])
def confirm():
    user_name = request.form.get('name')
    return f"<h1>Success!</h1><p>Thank you {user_name}, you are registered for the Assessment.</p>"