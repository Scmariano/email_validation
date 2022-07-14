
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.email import Email


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods= ['POST'])
def register():
    if Email.is_valid(request.form):
        Email.save(request.form)
        return redirect('/result')
    return redirect('/')


@app.route('/result')
def results():
    return render_template('result.html', emails = Email.get_all())


@app.route('/delete/<int:id>')
def delete(id):
    data = {
        'id':id
    }
    Email.delete(data)
    return redirect ('/result')