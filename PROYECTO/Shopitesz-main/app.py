from datetime import timedelta
from urllib import request

from flask import Flask,render_template,request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db, Categoria, Producto, Usuario, Tarjetas, Paqueterias, Carrito, Pedido, DetallePedido
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
import json

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:Shopit3sz.123@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'
#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"

# Urls defininas para el control de usuario
@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=10)

@app.route("/")
def inicio():
    #return "Bienvenido a la tienda en linea Shopitesz"
    return render_template('principal.html')

@app.route('/Usuarios/iniciarSesion')
def mostrar_login():
    if current_user.is_authenticated:
        return render_template('principal.html')
    else:
        return render_template('usuarios/login.html')

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))

@app.route('/Usuarios/nuevo')
def nuevoUsuario():
    if current_user.is_authenticated and not current_user.is_admin():
        return render_template('principal.html')
    else:
        return render_template('usuarios/registrarCuenta.html')

@app.route('/Usuarios/agregar',methods=['post'])
def agregarUsuario():
    try:
        usuario=Usuario()
        usuario.nombreCompleto=request.form['nombre']
        usuario.telefono=request.form['telefono']
        usuario.direccion=request.form['direccion']
        usuario.email=request.form['email']
        usuario.genero=request.form['genero']
        usuario.password=request.form['password']
        usuario.tipo=request.values.get("tipo","Comprador")
        usuario.estatus='Activo'
        usuario.agregar()
        flash('¡ Usuario registrado con exito')
    except:
        flash('¡ Error al agregar al usuario !')
    return render_template('usuarios/registrarCuenta.html')


@app.route("/Usuarios/validarSesion",methods=['POST'])
def login():
    correo=request.form['email']
    password=request.form['password']
    usuario=Usuario()
    user=usuario.validar(correo,password)
    if user!=None:
        login_user(user)
        return render_template('principal.html')
    else:
        flash('Nombre de usuario o contraseña incorrectos')
        return render_template('usuarios/login.html')

@app.route('/Usuarios/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('mostrar_login'))

@app.route('/Usuarios/verPerfil')
@login_required
def consultarUsuario():
    return render_template('usuarios/editar.html')

@app.route('/Usuarios/Clientes')
@login_required
def consultarClientes():
    if current_user.is_authenticated and current_user.is_admin():
        user=Usuario()
        return render_template('usuarios/clientes.html',user=user.consultaUsuarios())
    else:
        return render_template('usuarios/login.html')
@app.route('/Usuarios/Vendedores')
@login_required
def consultarVendedores():
    if current_user.is_authenticated and current_user.is_admin():
        user=Usuario()
        return render_template('usuarios/vendedores.html',user=user.consultaUsuarios())
    else:
        return render_template('usuarios/login.html')
@app.route('/Usuarios/Admin')
@login_required
def consultarAdmin():
    if current_user.is_authenticated and current_user.is_admin():
        user=Usuario()
        return render_template('usuarios/admins.html',user=user.consultaUsuarios())
    else:
        return render_template('usuarios/login.html')
#fin del manejo de usuarios

@app.route('/Usuarios/<int:id>')
@login_required
def consultarUnUsuario(id):
    if current_user.is_authenticated and current_user.is_admin():
        user=Usuario()
        return render_template('usuarios/editarUsu.html',user=user.consultaIndividual(id))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Usuarios/modificar',methods=['POST'])
@login_required
def modificarUsuario():
    if current_user.is_authenticated:
        try:
            user=Usuario()
            user.idUsuario=request.form['ID']
            user.nombreCompleto=request.form['nombre']
            user.email=request.form['email']
            user.direccion=request.form['direccion']
            user.genero=request.form['genero']
            user.tipo=request.form['tipo']
            user.editarUsua()
            flash('¡ Usuario editado con exito !')
        except:
            flash('¡ Error al editar el usuario !')
        if user.tipo == 'Comprador':
            return redirect(url_for('consultarClientes'))
        else:
            if user.tipo == 'Vendedor':
                return redirect(url_for('consultarVendedores'))
            else :
                return redirect(url_for('consultarAdmin'))

    else:
        return redirect(url_for('mostrar_login'))
#PRODUCTOS

@app.route("/productos")
def consultarProductos():
    producto=Producto()
    return render_template("productos/consultaGeneral.html",productos=producto.consultaGeneral())

@app.route("/productos/categorias")
def productosPorCategoria():
    categoria=Categoria()
    return render_template('productos/productosPorCategoria.html',categorias=categoria.consultaGeneral())

@app.route("/productos/categoria/<int:id>")
def consultarProductosPorCategoria(id):
    producto=Producto()
    if id==0:
        lista=producto.consultaGeneral()
    else:
        lista=producto.consultarProductosPorCategoria(id)
    #print(lista)
    listaProductos=[]
    #Generacion de un diccionario para convertir los datos a JSON
    for prod in lista:
        prod_dic={'idProducto':prod.idProducto,'nombre':prod.nombre,'descripcion':prod.descripcion,'precio':prod.precioVenta,'existencia':prod.existencia}
        listaProductos.append(prod_dic)
    #print(listaProductos)
    var_json=json.dumps(listaProductos)
    return var_json

@app.route('/producto/<int:id>')

def consultarProducto(id):
    if current_user.is_authenticated and  current_user.is_comprador():
        prod=Producto()
        prod=prod.consultaIndividual(id)
        dict_producto={"idProducto":prod.idProducto,"nombre":prod.nombre,"descripcion":prod.descripcion,"precio":prod.precioVenta,"existencia":prod.existencia}
        return json.dumps(dict_producto)
    else:
        msg={"estatus":"error","mensaje":"Debes iniciar sesion"}
        return json.dumps(msg)

@app.route('/productos/foto/<int:id>')
def consultarFotoPorducto(id):
    prod=Producto()
    return prod.consultarFoto(id)


@app.route('/Productos/nuevo')
@login_required
def nuevoProducto():
    if current_user.is_authenticated and current_user.is_admin():
            return render_template('productos/agregarP.html')
    else:
        abort(404)

@app.route('/Productos/agregar',methods=['post'])
@login_required
def agregarProducto():
    try:
        if current_user.is_authenticated:
            if current_user.is_admin():
                try:
                    prod=Producto()
                    prod.idCategoria=1
                    prod.nombre=request.form['nombre']
                    prod.descripcion=request.form['desc']
                    prod.precioVenta=request.form['precio']
                    prod.existencia=request.form['exist']
                    prod.foto=request.files['imagen'].stream.read()
                    prod.especificaciones=request.files['espe'].stream.read()
                    prod.estatus='Activo'
                    prod.agregar()
                    flash('¡ Producto agregada con exito !')
                except:
                    flash('¡ Error al agregar el producto !')
                return redirect(url_for('consultarProductos'))
            else:
                abort(404)

        else:
            return redirect(url_for('mostrar_login'))
    except:
        abort(500)

@app.route('/Productos/editar',methods=['POST'])
@login_required
def editarProducto():
    if current_user.is_authenticated and current_user.is_admin():
        try:
            prod=Producto()
            prod.idCategoria=request.form['idCategoria']
            prod.nombre=request.form['nombre']
            prod.descripcion = request.form['descripcion']
            prod.precioVenta = request.form['precioVenta']
            prod.existencia = request.form['existencia']
            prod.estatus = request.form['estatus']
            imagen=request.files['imagen'].stream.read()
            if imagen:
                prod.imagen=imagen
            prod.estatus=request.values.get("estatus","Inactivo")
            prod.editar()
            flash('¡ Producto editado con exito !')
        except:
            flash('¡ Error al editar el producto !')

        return redirect(url_for('consultarProductos'))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Productos/eliminar/<int:id>')
@login_required
def eliminarProducto(id):
    if current_user.is_authenticated and current_user.is_admin():
        try:
            prod=Producto()
            prod.eliminar(id)
            flash('Producto eliminado con exito')
        except:
            flash('Error al eliminar el producto')
        return redirect(url_for('consultarProductos'))
    else:
        return redirect(url_for('mostrar_login'))


#Categorias
@app.route('/Categorias')
def consultaCategorias():
    cat=Categoria()
    return render_template('categorias/consultaGeneral.html',categorias=cat.consultaGeneral())

@app.route('/Categorias/consultarImagen/<int:id>')
def consultarImagenCategoria(id):
    cat=Categoria()
    return cat.consultarImagen(id)


@app.route('/Categorias/nueva')
@login_required
def nuevaCategoria():
    if current_user.is_authenticated and current_user.is_admin():
            return render_template('categorias/agregar.html')
    else:
        abort(404)

@app.route('/Categorias/agregar',methods=['post'])
@login_required
def agregarCategoria():
    try:
        if current_user.is_authenticated:
            if current_user.is_admin():
                try:
                    cat=Categoria()
                    cat.nombre=request.form['nombre']
                    cat.imagen=request.files['imagen'].stream.read()
                    cat.estatus='Activa'
                    cat.agregar()
                    flash('¡ Categoria agregada con exito !')
                except:
                    flash('¡ Error al agregar la categoria !')
                return redirect(url_for('consultaCategorias'))
            else:
                abort(404)

        else:
            return redirect(url_for('mostrar_login'))
    except:
        abort(500)


@app.route('/Categorias/<int:id>')
@login_required
def consultarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        cat=Categoria()
        return render_template('categorias/editar.html',cat=cat.consultaIndividuall(id))
    else:
        return redirect(url_for('mostrar_login'))


@app.route('/Categorias/editar',methods=['POST'])
@login_required
def editarCategoria():
    if current_user.is_authenticated and current_user.is_admin():
        try:
            cat=Categoria()
            cat.idCategoria=request.form['id']
            cat.nombre=request.form['nombre']
            imagen=request.files['imagen'].stream.read()
            if imagen:
                cat.imagen=imagen
            cat.estatus=request.values.get("estatus","Inactiva")
            cat.editar()
            flash('¡ Categoria editada con exito !')
        except:
            flash('¡ Error al editar la categoria !')

        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Categorias/eliminar/<int:id>')
@login_required
def eliminarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        try:
            categoria=Categoria()
            #categoria.eliminar(id)
            categoria.eliminacionLogica(id)
            flash('Categoria eliminada con exito')
        except:
            flash('Error al eliminar la categoria')
        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))

#Fin del crud de categorias

#manejo de errores
@app.errorhandler(404)
def error_404(e):
    return render_template('comunes/error_404.html'),404

@app.errorhandler(500)
def error_500(e):
    return render_template('comunes/error_500.html'),500

#TARJETAS
@app.route('/Tarjetas')
@login_required
def consultarTarjetas():
    if current_user.is_authenticated and current_user.is_comprador():
        tar = Tarjetas()
        return render_template('/tarjetas/consultaT.html',tarjetas = tar.consultaTarjeta())
    else:
        abort(404)

@app.route('/Tarjetas/nueva')
@login_required
def nuevaTarjetas():
    if current_user.is_authenticated and current_user.is_comprador():
            return render_template('tarjetas/agregarT.html')
    else:
        abort(404)

@app.route('/Tarjetas/agregar',methods=['post'])
@login_required
def agregarTarjetas():
    try:
        if current_user.is_authenticated:
            if current_user.is_comprador():
                try:
                    tar=Tarjetas()
                    tar.idUsuario=request.form['id']
                    tar.noTarjeta=request.form['tarjeta']
                    tar.saldo=request.form['saldo']
                    tar.Banco=request.form['bancoE']
                    tar.estatus='Activa'
                    tar.agregar()
                    flash('¡ Tarjeta agregada con exito !')
                except:
                    flash('¡ Error al agregar la tarjeta !')
                return redirect(url_for('consultarTarjetas'))
            else:
                abort(404)

        else:
            return redirect(url_for('mostrar_login'))
    except:
        abort(500)

@app.route('/Tarjetas/editar',methods=['post'])
@login_required
def editarTarjeta():
    if current_user.is_authenticated and current_user.is_comprador():
        try:
            tar=Tarjetas()
            tar.idTarjeta=request.form['idT']
            tar.noTarjeta=request.form['tarjeta']
            tar.Banco=request.form['bancoE']
            tar.editar()
            flash('¡ Tarjeta editada con exito !')
        except:
            flash('¡ Error al editar la tarjeta !')

        return redirect(url_for('consultarTarjetas'))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Tarjetas/<int:id>')
@login_required
def consultarTarjeta(id):
    if current_user.is_authenticated and current_user.is_comprador():
        tar=Tarjetas()
        return render_template('tarjetas/editarT.html',tar=tar.consultaIndividuall(id))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Tarjetas/eliminar/<int:id>')
@login_required
def eliminarTarjeta(id):
    if current_user.is_authenticated and current_user.is_comprador():
        try:
            tar=Tarjetas()
            tar.eliminar(id)
            flash('Tarjeta eliminada con exito')
        except:
            flash('Error al eliminar la tarjeta')
        return redirect(url_for('consultarTarjetas'))
    else:
        return redirect(url_for('mostrar_login'))

#PAQUETERÍAS
@app.route('/Paqueterias')
@login_required
def consultarPaqueterias():
    if current_user.is_authenticated and current_user.is_admin():
        paq=Paqueterias()
        return render_template('/paqueterias/consultaP.html',paqueterias = paq.consultaPaqueterias())
    else:
        return render_template('usuarios/login.html')

@app.route('/Paqueterias/nueva')
@login_required
def nuevaPaqueterias():
    if current_user.is_authenticated and current_user.is_admin():
            return render_template('paqueterias/agregarP.html')
    else:
        abort(404)

@app.route('/Paqueterias/agregar',methods=['post'])
@login_required
def agregarPaqueterias():
    try:
        if current_user.is_authenticated:
            if current_user.is_admin():
                try:
                    paq=Paqueterias()
                    paq.nombre=request.form['nombre']
                    paq.paginaWeb=request.form['paginaWeb']
                    paq.precioGr=request.form['precio']
                    paq.Telefono=request.form['telefono']
                    paq.estatus='Activa'
                    paq.agregar()
                    flash('¡ Paqueteria agregada con exito !')
                except:
                    flash('¡ Error al agregar la Paqueteria !')
                return redirect(url_for('consultarPaqueterias'))
            else:
                abort(404)
        else:
            return redirect(url_for('mostrar_login'))
    except:
        abort(500)

@app.route('/Paqueterias/editar',methods=['POST'])
@login_required
def editarPaqueteria():
    if current_user.is_authenticated and current_user.is_admin():
        try:
            paq = Paqueterias()
            paq.idPaqueteria = request.form['id']
            paq.nombre = request.form['nombre']
            paq.paginaWeb = request.form['paginaWeb']
            paq.precioGr = request.form['precioGr']
            paq.Telefono = request.form['telefono']
            paq.estatus = 'Activa'
            paq.editar()
            flash('¡  Paqueteria editada con exito !')
        except:
            flash('¡ Error al editar la  paqueteria!')

        return redirect(url_for('consultarPaqueterias'))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Paqueterias/<int:id>')
@login_required
def consultarPaqueteria(id):
    if current_user.is_authenticated:
        paq=Paqueterias()
        return render_template('/Paqueterias/editarP.html',paq=paq.consultaIndividuall(id))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Paqueterias/eliminar/<int:id>')
@login_required
def eliminarPaqueteria(id):
    if current_user.is_authenticated and current_user.is_admin():
        try:
            paq=Paqueterias()
            #paq.eliminacionLogica(id)
            paq.eliminar(id)
            flash('Paqueteria eliminada con exito')
        except:
            flash('Error al eliminar la Paqueteria')
        return redirect(url_for('consultarPaqueterias'))
    else:
        return redirect(url_for('mostrar_login'))

#Carrito
@app.route('/carrito/agregar/<data>',methods=['get'])
def agregarProductoCarrito(data):
    msg=''
    if current_user.is_authenticated and current_user.is_comprador():
        datos=json.loads(data)
        carrito=Carrito()
        carrito.idProducto=datos['idProducto']
        carrito.idUsuario=current_user.idUsuario
        carrito.cantidad=datos['cantidad']
        carrito.agregarCarrito()
        msg={'estatus':'ok','mensaje':'Producto agregado a la cesta.'}
    else:
        msg = {"estatus": "error", "mensaje": "Debes iniciar sesion"}
    return json.dumps(msg)

@app.route("/carrito")
@login_required
def consultarCesta():
    if current_user.is_authenticated:
        carrito = Carrito()
        return render_template('carrito/consultaGeneral.html',cesta=carrito.consultaGeneralCar(current_user.idUsuario))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/carrito/eliminar/<int:id>')
@login_required
def eliminarDeCarrito(id):
    if current_user.is_authenticated and current_user.is_comprador():
        try:
            carrito=Carrito()
            #paq.eliminacionLogica(id)
            carrito.eliminarProductoDeCarrito(id)
            flash(' eliminad con exito')
        except:
            flash('Error al eliminar ')
        return redirect(url_for('consultarCesta'))
    else:
        return redirect(url_for('mostrar_login'))



#PEDIDOS
@app.route("/Pedidos")
@login_required
def consultarPedidos():
    if current_user.is_authenticated:
        ped = Pedido()
        return render_template('Pedidos/consulta.html',pedido=ped.consultaPedidos())
    else:
        return redirect(url_for('mostrar_login'))


@app.route('/Pedidos/verpedidos/detallespedidos/<int:id>')
@login_required
def verDetallesPedido(id):
    detallepedido=DetallePedido()
    if current_user.is_authenticated and current_user.is_comprador() or current_user.is_vendedor():
     return render_template("/detallesPedidos/consultaDetallespedido.html",detallepedido=detallepedido.consultaGeneral())

@app.route('/Pedidos/verpedidos/detallespedidos/en/<int:id>')
@login_required
def editarDetallesPedidos(id):
    detallepedido=DetallePedido()
    if current_user.is_authenticated and current_user.is_comprador() or current_user.is_vendedor():
        return render_template("detallesPedidos/editarDetallespedido.html",detallepedido=detallepedido.consultaIndividual(id))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Pedidos/verpedidos/detallespedidos/editarPedidos',methods=['POST'])
@login_required
def modDetallesPedidos():
    if current_user.is_authenticated and current_user.is_comprador() or current_user.is_vendedor():
        try:
            detallepedido=DetallePedido()
            detallepedido.idDetalle = request.form['idDetalle']
            detallepedido.idPedido = request.form['idPedido']
            detallepedido.idProducto = request.form['idProducto']
            detallepedido.precio = request.form['precio']
            detallepedido.cantidadPedida = request.form['cantidadPedida']
            detallepedido.cantidadEnviada = request.form['cantidadEnviada']
            detallepedido.cantidadAceptada = request.form['cantidadAceptada']
            detallepedido.cantidadRechazada = request.form['cantidadRechazada']
            detallepedido.subtotal = request.form['subtotal']
            detallepedido.comentario = request.form['comentario']
            detallepedido.estatus = request.form['estatus']
            detallepedido.editar()
            flash('! Detalles Pedido editada con exito')
            return redirect(url_for('mostrar_login'))
        except:
            flash('! Error al editar Detalles Pedido ')

@app.route('/Pedidos/editarPedidos/<int:id>',methods=['post'])
@login_required
def editarPedidos():
    if current_user.is_authenticated:
        try:
            ped=Pedido()
            ped.idPedido = request.form['idPedido']
            ped.idComprador = request.form['idComprador']
            ped.idVendedor = request.form['idVendedor']
            ped.idTarjeta = request.form['idTarjeta']
            ped.fechaRegistro = request.form['fechaRegistro']
            ped.fechaAtencion = request.form['fechaAtencion']
            ped.fechaRecepcion = request.form['fechaRecepcion']
            ped.fechaCierre = request.form['fechaCierre']
            ped.total = request.form['total']
            ped.estatus = request.form['ESTATUS']
            ped.editar()
            flash('! Pedido editado con exito')
        except:
            flash('! Error al editar el pedido ')
        return redirect(url_for('mostrar_login'))
    else:
         return redirect(url_for('mostrar_login'))


# manejo de detallesPedidos
@app.route('/Pedidos/detallespedidos')
@login_required
def consultarDP():
    dp=DetallePedido()
    return render_template("/detallesPedidos/consulta.html",detped=dp.consultaDP())


# fin del manejo de detallesPedidos
if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)



