from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    # Render an HTML page with a link
    return render_template('index.html')

@app.route('/run-python-code')
def run_python_code():
    # Put your Python code logic here
    print("Python code is running!")  # example action
    # You can do more complex operations here
    
    # Then redirect back to home or another page
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

