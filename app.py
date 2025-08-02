from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-python-code')
def run_python_code():
    print("Python code is running!")  # You can replace this with your actual code
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
