from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,BLOB,ForeignKey,Float
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
db=SQLAlchemy()

class Categoria(db.Model):
    __tablename__='Categorias'
    idCategoria=Column(Integer,primary_key=True)
    nombre=Column(String,unique=True)
    estatus=Column(String,nullable=False)
    imagen=Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividuall(self,id):
        return Categoria.query.get(id)

    def consultarImagen(self,id):
        return self.consultaIndividuall(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        cat=self.consultaIndividuall(id)
        db.session.delete(cat)
        db.session.commit()

    def eliminacionLogica(self,id):
        cat = self.consultaIndividuall(id)
        cat.estatus='Inactiva'
        cat.editar()

class Producto(db.Model):
    __tablename__='Productos'
    idProducto=Column(Integer,primary_key=True)
    idCategoria=Column(Integer,ForeignKey('Categorias.idCategoria'))
    nombre=Column(String,nullable=False)
    descripcion=Column(String,nullable=True)
    precioVenta=Column(Float,nullable=False)
    existencia=Column(Integer,nullable=False)
    foto=Column(BLOB)
    especificaciones=Column(BLOB)
    estatus=Column(String,nullable=False)
    categoria=relationship('Categoria',backref='productos',lazy='select')

    def consultaGeneral(self):
        return self.query.all()

class Usuario(UserMixin,db.Model):
    __tablename__='Usuarios'
    idUsuario=Column(Integer,primary_key=True)
    nombreCompleto=Column(String,nullable=False)
    direccion=Column(String,nullable=False)
    telefono=Column(String,nullable=False)
    email=Column(String,unique=True)
    password_hash=Column(String(128),nullable=False)
    tipo=Column(String,nullable=False)
    estatus=Column(String,nullable=False)
    genero=Column(String,nullable=False)

    @property #Implementa el metodo Get (para acceder a un valor)
    def password(self):
        raise AttributeError('El password no tiene acceso de lectura')

    @password.setter #Definir el metodo set para el atributo password_hash
    def password(self,password):#Se informa el password en formato plano para hacer el cifrado
        self.password_hash=generate_password_hash(password)

    def validarPassword(self,password):
        return check_password_hash(self.password_hash,password)
    #Definición de los métodos para el perfilamiento
    def is_authenticated(self):
        return True

    def is_active(self):
        if self.estatus=='Activo':
            return True
        else:
            return False
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUsuario

    def is_admin(self):
        if self.tipo=='Administrador':
            return True
        else:
            return False
    def is_vendedor(self):
        if self.tipo=='Vendedor':
            return True
        else:
            return False
    def is_comprador(self):
        if self.tipo=='Comprador':
            return True
        else:
            return False
    #Definir el método para la autenticacion
    def validar(self,email,password):
        usuario=Usuario.query.filter(Usuario.email==email).first()
        if usuario!=None and usuario.validarPassword(password) and usuario.is_active():
            return usuario
        else:
            return None
    #Método para agregar una cuenta de usuario
    def agregar(self):
        db.session.add(self)
        db.session.commit()

class Envios(db.Model):
    __tablename__='ENVIOS'
    IDENVIO=Column(Integer,primary_key=True)
    IDPEDIDO=Column(Integer,ForeignKey('Pedidos.IDPEDIDO'))
    IDPAQUETERIA=Column(Integer,ForeignKey('Paqueterias.IDPAQUETERIA'))
    FECHAENVIO=Column(String,nullable=True)
    FECHAENTREGA=Column(String,nullable=False)
    NOGUIA=Column(Integer,nullable=False)
    PESOPAQUETE=Column(Float,nullable=False)
    PRECIOGR=Column(Float,nullable=False)
    TOTOALPAGAR=Column(Float,nullable=False)
    ESTATUS = Column(String,nullable=False)
    #paqueteria = relationship('Paqueterias', backref='envios', lazy='select')
    def agregar(self):
        db.session.add(self)
        db.session.commit()

class Paqueterias(db.Model):
    __tablename__ = 'PAQUETERIAS'
    IDPAQUETERIA = Column(Integer,primary_key=True)
    NOMBRE = Column(String,nullable=False)
    PAGINAWEB = Column(String,nullable=False)
    PRECIOGR = Column(Float, nullable=False)
    TELEFONO = Column(String, nullable=False)
    ESTATUS = Column(String,nullable=False)

class Pedidos(db.Model):
    __tablename__= 'Pedidos'
    IDPEDIDO=Column(Integer,primary_key=True)
    IDCOMPRADOR = Column(Integer, ForeignKey('Usuarios.idUsuario'))
    IDVENDEDOR = Column(Integer, ForeignKey('Usuarios.idUsuario'))
    IDTARJETA = Column(Integer, ForeignKey('Tarjetas.idTarjeta'))
    PAGINAWEB = Column(String, nullable=False)
    FECHAREGISTRO = Column(String, nullable=False)
    FECHAATENCION = Column(String, nullable=False)
    FECHARECEOCION = Column(String, nullable=False)
    FECHACIERRE = Column(String, nullable=False)
    TOTAL = Column(Float, nullable=False)
    ESTATUS = Column(String, nullable=False)


class Tarjetas(db.Model):
    __tablename__ = 'Tarjetas'
    idTarjeta = Column(Integer,primary_key=True)
    idUsuario = Column(Integer, ForeignKey('Usuarios.idUsuario'))
    noTarjeta = Column(String, nullable=False)
    Banco = Column(String, nullable=False)
    estatus = Column(String, nullable=False)
