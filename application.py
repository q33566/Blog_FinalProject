from flask import Flask, render_template
app = Flask(__name__)

@app.route('/about')
def aboutePage():
    return render_template('AboutPage.html')