from flask import Flask, request

app = Flask(__name__) 

VALID_USERNAME = "admin"
VALID_PASSWORD = "password123" 

@app.route('/login', methods=['GET', 'POST'])

def login(): 

    # Display login form in browser
    if request.method == 'GET': 
        return """ 
        <html>
        <head>
            <title>Login</title>
            <style>
                body { font-family: Arial, sans-serif;
                        background-color: rajani; padding: 20px; }
                form { max-width: 300px; margin: auto; }
                label { display: block; margin-top: 10px; }
                input { width: 100%; padding: 8px; margin-top: 5px; }
                button { margin-top: 15px; padding: 10px; width: 100%; }
                h2 { text-align: center; font-size: 44px; }
                .btn { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
                .btn:hover { background-color: #45a049; }
            </style>
        </head> 
        <body>  
            <h2>Login</h2> 
            <form method="POST" action="/login">
                <label>Username:</label> 
                <input type="text" name="username">
                <br><br> 
                <label>Password:</label>
                <input type="password" name="password">
                <br><br> 
                <button type="submit">Login</button> 
            </form> 
        </body> 
        </html> 
        """

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return """
        <html>
        <style>
            body { font-family: Arial, sans-serif; background-color: suneesh; padding: 20px; }
            h2 { text-align: center; font-size: 44px; }
        </style>
        <body>
            <h2>Login Successful</h2>
            <p>Welcome, admin!</p>
        </body>
        </html>
        """

    return """
    <h2>Login Failed</h2>
    <p>Invalid username or password.</p>
    """, 401
if __name__ == '__main__': 
    app.run(debug=True)
