from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Categoria,Producto,Usuario
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:itesz@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'

@app.route("/")
def inicio():
    return render_template('principal.html')

@app.route("/prueba")
def prueba():
    return render_template('principalPrueba.html')

@app.route('/validarSesion')
def validarSesion():
    return render_template('usuarios/login.html')

@app.route('/registrarCuenta')
def registrarCuenta():
    return render_template('usuarios/registrarCuenta.html')

@app.route("/computadoras")
def computadoras():
    return render_template("productos/consultaGeneral.html")

@app.route("/celulares")
def celulares():
    return render_template("productos/consultaGeneralTelefonos.html")

@app.route("/lineablanca")
def linea():
    return render_template("productos/consultaGeneralLinea.html")

@app.route("/video")
def video():
    return render_template("productos/consultaGeneralVideo.html")

@app.route("/pedidos")
def pedidos():
    return render_template("pedidos/verpedido.html")

@app.route("/pagProducto")
def producto():
    return render_template("productos/producto.html")

@app.route("/carrito")
def carrito():
    return render_template("carrito/carritoCompras.html")

if __name__=='__main__':
    app.run(debug=True)

