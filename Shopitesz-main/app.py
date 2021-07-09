from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def inicio():
    #return "Bienvenido a la tienda en linea Shopitesz"
    return render_template('principal.html')
@app.route('/validarSesion')
def validarSesion():
    return render_template('usuarios/login.html')

@app.route('/registrarCuenta')
def registrarCuenta():
    return render_template('usuarios/registrarCuenta.html')

@app.route("/login",methods=['POST'])
def login():
    correo=request.form['correo']
    return "Validando al usuario:"+correo

@app.route("/productos")
def consultarProductos():
    #return "Retorna la lista de productos"
    return render_template("productos/consultaGeneral.html")

@app.route("/productos/agregar")
def agregarProducto():
    return "<b>agregando un producto</b><table><th>Prueba</th></table>"

@app.route("/productos/actualizar")
def actualizarProducto():
    return "actualizando un producto"
@app.route("/cesta")
def consultarCesta():
    return "consultando la cesta de compra"

@app.route("/productos/categoria/<int:id>")
def consultarProductosCategoria(id):
    return "consultando los productos de la cetogoria: "+str(id)

@app.route("/clientes/<string:nombre>")
def consultarCliente(nombre):
    return "consultando al cliente:"+nombre

@app.route("/productos/<float:precio>")
def consultarPorductosPorPrecio(precio):
    return "Hola"+str(precio)

if __name__=='__main__':
    app.run(debug=True)

