from flask import Flask , render_template
app = Flask(__name__)

@app.route('/')
def home():

    return render_template('index.html')
@app.route('/blog')
def blog():
    return render_template('blog.html')
@app.route('/single')
def single():
    return render_template('single.html')
@app.route('/styles')
def style():
    return render_template('styles.html')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)