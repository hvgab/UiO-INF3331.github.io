from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/handle_login', methods=['POST'])
def handle_login():           
    
    assert request.method == 'POST'   # Check that we are really in a POST request
    
    # Access the form data:
    username = request.form["username"]
    password = request.form["password"]
    
    if username == "simon" and password == "safe":
        return "You are logged in Simon"
    else:
        error = "Invalid credentials"
        return render_template("login.html", error=error)     

if __name__ == "__main__":
    app.run()