from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/cante'
db = SQLAlchemy(app)


class Usuario(db.Model):
    __usuario__ = "usuario"
    id_usuario = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True)
    senha = db.Column(db.String(255))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    usuario = Usuario.query.all()
    msg = ""
    id_usuario = 0
    if request.method == 'POST':
        try:
            login = request.form['login']
            senha = request.form['senha']
            usuario = Usuario.query.filter(and_(
                Usuario.login == login,
                Usuario.senha == senha)).all()

            if usuario:
                for e in usuario:
                    id_usuario = (e.id_usuario)
                return redirect(f"/index/{id_usuario}")
            else:
                msg = ("Usuario ou senha errada")
        except:
            msg = ("usuario ou senha errada")
    return render_template("login.html", msg=msg, id_usuario=id_usuario)


@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastrar():
    msg = ""
    if request.method == 'POST':
        try:
            login = Usuario(request.form['login'], request.form['senha'],)
            db.session.add(login)
            db.session.commit()
            msg = ("usuario criado com sucesso!")
        except:
            msg = ("esse usuario ja existe!")
    return render_template('cadastrar.html', msg=msg)


if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)
