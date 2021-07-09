from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

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

