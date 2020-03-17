from flask import Flask , render_template, request
app = Flask(__name__)

class temporary:
    table = None
@app.route('/')
def home():

    return render_template('index.html')
@app.route('/process',methods=['get'])
def process():
    selected = 1
    return render_template('index.html', selected=selected)
@app.route('/process2', methods=['POST'])
def process2():
    Tb_name = request.form['filename']
    columns = request.form['columns']
    columns = int(columns)
    return render_template('single.html', Tb_name=Tb_name, columns=columns)



@app.route('/blog')
def blog():
    return render_template('blog.html')
@app.route('/tabloid')
def tabloid():
    return render_template('single.html')
@app.route('/styles')
def style():
    return render_template('styles.html')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)