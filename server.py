from flask import Flask, render_template, request, redirect
from openpyxl import Workbook, load_workbook
app = Flask(__name__)

class temporary:
    # table buat nama tabel yang di buat
    # columns buat nyimpen angka(type data belum integer) yang diinput sama user
    # store buat nyimpen semua data di setiap row pada setiap column. contoh : user input 2 column brarti di dlm store =(row1column1,row1column2,row2column1,row2column2,row3column1,row3column2,dst sampe usernya puas)
    table = None
    columns = None
    store = []
    changer = []
    added = None
    lister = []

    # coba panggil function
    def add_function(A):
        result = sum(A)
        return result
    # syntax manggil def add_function di html
    app.jinja_env.globals.update(add_function=add_function)

@app.route('/')
def home():

    return render_template('index.html')
@app.route('/process',methods=['get'])
def process():
    selected = 1
    # just to make sure everything restart
    temporary.table = None
    temporary.columns = None
    temporary.store = []
    temporary.changer = []
    temporary.added = None
    return render_template('index.html', selected=selected)
@app.route('/process2', methods=['POST'])
def process2():
    Tb_name = request.form['filename']
    columns = request.form['columns']
    columns = int(columns)
    try:
        wb = load_workbook(filename='data.xlsx')
    except:
        wb = Workbook()
        wb.save(filename='data.xlsx')

    for x in wb.sheetnames:
        if Tb_name == x:
            warning = 'this table is exist please delete or use other name'
            return render_template('index.html', warning=warning)

    # temporary adalah class untuk nyimpen data sementara bisa dilihat awal diatas
    temporary.table = Tb_name
    temporary.columns = columns
    return render_template('single.html', Tb_name=Tb_name, columns=columns)
@app.route('/storing_data', methods=['POST'])
def storing_data():
    Tb_name = temporary.table
    columns = temporary.columns
    columns = int(columns)
    for x in range(columns):
        # x perlu dijadiin string karena request.form perlunya string bkan integer
        x = str(x)
        data = request.form[x]
        temporary.store.append(data)
    stored = temporary.store
    #changer dipakai untuk memangil value setiap row, penjelasan lebih lanjut di single.html
    if temporary.added == None:
        temporary.changer.append(-columns)
        temporary.added = "yes"
        #kurang 1 karena isi changer awal diisi dgn -column
        for x in range(columns - 1):
            temporary.changer.append(columns)
    else:
        for x in range(columns):
            temporary.changer.append(columns)
    changer = temporary.changer

    #rows adalah jumlah row yang ada, pemakaian ada di single.html
    try:
        rows = len(temporary.store)/columns
        rows = int(rows)
    except:
        rows = int(0)
    # ini for buat mangil input dari html ny kalo diliat di html <input name=x> x itu range(column),
    # contohnya user input column 3 brarti setiap row dia masukin 3 data yaitu row1column1,row1column2,row1column3>>>nah x nya itu jadi x=1,2,3 >> 1 buat manggil row1column1, 2 buat manggil row1column2, dst


    return render_template('single.html', Tb_name=Tb_name, columns=columns, changer=changer, rows=rows, stored=stored)
@app.route('/save_reset')
def save_reset():
    # if buat mastiin user masuk ke single.html dari dpan bukan dari blakang karena di browser ada back button setelah user kluar dari single.html temporary semua value di dlmnya bakal ke reset jadi bisa ketangkep sama if kalo dy back button
    if temporary.table == None:
        warning2 = "table name not detected please create new table or edit table"
        return render_template('index.html', warning2=warning2)
    else:
        # pertama2 load dulu excel namanya data.xlsx di try kalo ternyata excelnya blom ke buat masuk ke except dy otomatis buat excel yang namanya data.xlsx
        try:
            wb = load_workbook(filename='data.xlsx')
        except:
            wb = Workbook()
            wb.save(filename='data.xlsx')
        #perlu Tb_name karena rencana nya pake 1 excel doank dimana didlm 1 excel itu ada banyak page/sheet, sheet nya itu diksh nama tabel yang diinput, jadi kalo mw hapus tinggal hapus nama sheet nya aja
        Tb_name = temporary.table
        ws = wb.create_sheet(Tb_name)
        #ini algorithm ngemisahin data di temporary.store
        columns = temporary.columns
        columns = int(columns)
        # row quantitiy untuk mengetahui jumlah row. dipake untuk openpyxl masukin value ke specific cell
        row_quantity = len(temporary.store)/columns
        row_quantity = int(row_quantity)
        for x in range(columns):
            # +1 gara x awal itu 0 bukan 1
            index = x + 1
            #ngeloop sebanyak x yaitu sebanyak kolom yang di pilih
            ws.insert_cols(0)
            for y in range(row_quantity):
                #ngeloop terus sebanyak row yang ada

                selector = str(y + 1)

                # dibawah ini ws['A' + selector], jika selectornya 1 jadi ws['A1'] artinya cell A1 selector didapat dari row_quantity
                ws['A' + selector] = temporary.store[-index]
                # untuk indexing kita dari belakang temporary.store[-index] ada minus yang artinya ambil dari paling blakang mengapa?
                # karena kita menggunakan ws.insert_rows(0) yang artinya buat kolom baru di existing kolom ke 0 artinya kolom pertama yang lama geser jadi kolom kedua dan kolom pertama jadi yang baru saja dibuat
                # makanya kita indexing dri blakang gara2 geser yang dimasukin awal jadi yang terakhir.
                index = index + columns
                #index diata diupdate dengan rumus yg terter diatas karena dari row1kolom1 ke row2kolom1 harus lompat sebanyak (column-1)
        wb.save(filename='data.xlsx')
        # reset smua value
        temporary.table = None
        temporary.columns = None
        temporary.store = []
        temporary.changer = []
        temporary.added = None
        return redirect('/')
@app.route('/cancel')
def cancel():
    temporary.store = []
    temporary.table = None
    temporary.columns = None
    temporary.changer = []
    temporary.added = None
    return redirect('/')
@app.route('/back')
def back():
    Tb_name = temporary.table
    columns = temporary.columns
    columns = int(columns)
    for x in range(columns):
        #hapus row trakir cnth user input 6 kolom brarti 1 row ada 6 value di pop 6 kali biar 6 value trakir di temporary store ilang
        temporary.store.pop()
        temporary.changer.pop()
    stored = temporary.store
    changer = temporary.changer
    #rows adalah jumlah row yang ada, pemakaian ada di single.html
    try:
        rows = len(temporary.store)/columns
        rows = int(rows)
    except:
        rows = int(0)
    return render_template('single.html', Tb_name=Tb_name, columns=columns, changer=changer, rows=rows, stored=stored)
@app.route('/process_delete')
def process_delete():
    try:
        wb = load_workbook(filename='data.xlsx')
        Q =len(wb.sheetnames)
        Q = int(Q)
        lister = []
        # perlu mulai dari satu soalnya sheet paling awal di excelny jgn di apus
        for x in wb.sheetnames[1:Q]:
            lister.append(x)
            temporary.lister.append(x)
    except:
        wb = "there is nothing to delete"
        lister = wb

    return render_template('index.html', lister=lister)
@app.route('/deleted', methods=['POST'])
def deleted():
    lister = temporary.lister
    wb = load_workbook(filename='data.xlsx')
    # perlu mulai dari satu soalnya sheet paling awal di excelny jgn di apus
    if request.method == 'POST':
        print(lister)
        for x in lister:
            x = str(x)
            try:
                if request.form['submit_button'] == x:
                    for item in wb.sheetnames:

                        if item == x:

                            item = str(item)
                            temp = wb[item]
                            wb.remove_sheet(temp)

                            lister.remove(x)

                            wb.save(filename='data.xlsx')
                            return render_template('index.html', lister=lister)
            except:
                print("excep")
                pass  # do something else
    return render_template('index.html', lister=lister)
@app.route('/view_table')
def view_table():
    try:
        wb = load_workbook(filename='data.xlsx')
        lister = []
        Q = len(wb.sheetnames)
        Q = int(Q)
        # perlu mulai dari satu soalnya sheet paling awal di excelny jgn di apus
        for x in wb.sheetnames[1:Q]:
            lister.append(x)
            temporary.lister.append(x)
        return render_template('index.html', lister=lister)
    except:
        warning2 = "table name not detected please create new table or edit table"
        return render_template('index.html', warning2=warning2)
@app.route('/view_process', methods=['POST'])
def view_process():
    if request.method == 'POST':
        for x in lister:
            x = str(x)
            try:
                if request.form['submit_button'] == x:
                    for item in wb.sheetnames:

                        if item == x:
                            Tb_name = str(item)

                            return redirect(url_for('viewed', Tb_name=Tb_name))
            except:
                pass  # do something else
    return '<h1>view_process error</h1>'
@app.route('/viewed/<Tb_name>')
def viewed(Tb_name):
    wb = load_workbook(filename='data.xlsx')
    ws = wb[Tb_name]

    return render_template('style.html')

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