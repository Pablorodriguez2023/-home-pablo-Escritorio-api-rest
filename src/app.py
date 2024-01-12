from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

conexion = MySQL(app)


@app.route('/usuarios', methods = ['GET'])
def listar_usuarios():
    try:
        cursor=conexion.connection.cursor()
        
        sql="SELECT id, first_name, last_name, email, password, token, age, image, description FROM usuarios"
        
        cursor.execute(sql)
        
        datos=cursor.fetchall()
        
        usuarios=[]
        for fila in datos:
            usuario={'id': fila[0], 'first_name': fila[1], 'last_name': fila[2], 'email': fila[3], 'password': fila[4], 'token': fila[5], 'age': fila[6], 'image': fila[7], 'description': fila[8]}
            
            usuarios.append(usuario)
                   
        return jsonify({'usuarios':usuarios, 'mensaje':"usuarios listados"})
          
    except Exception as ex:
        return jsonify({'mensaje':"error"})
    

@app.route('/usuarios/<id>', methods =['GET'])
def leer_usuarios(id):
    try:               
        cursor=conexion.connection.cursor()
        
        sql="SELECT id, first_name, last_name, email, password, token, age, image, description FROM usuarios WHERE id = '{0}'". format(id)
        
        cursor.execute(sql)
        
        datos=cursor.fetchone()
        
        if datos != None:
            usuario={'id': datos[0], 'first_name': datos[1], 'last_name': datos[2], 'email': datos[3], 'password': datos[4], 'token': datos[5], 'age': datos[6], 'image': datos[7], 'description': datos[8]}
            return jsonify({'usuario': usuario, 'mensaje':"usuario encontrado"})    
        else: 
            return jsonify({'mensaje': "usuario no encontrado"})
            
    except Exception as ex:
        return jsonify({'mensaje':"error"})
    
    
@app.route('/usuarios', methods =['POST'])
def registro_usuarios():
    try:
        cursor=conexion.connection.cursor()    
        
        sql = """INSERT INTO usuarios (id, first_name, last_name, email, password, token, age, image, description) 
        VALUES({0}, '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}', '{8}')""".format(request.json['id'], request.json['first_name'], request.json['last_name'], request.json['email'], request.json['password'], request.json['token'], request.json['age'], request.json['image'], request.json['description'])
        
        cursor.execute(sql) #ejecuta la conexion
        
        conexion.connection.commit()  #confirma la insercion    
        #print(request.json)
        return jsonify({'mensaje':"usuario registrado"})      
                
    except Exception as ex:
        return jsonify({'mensaje':"error"})
    

@app.route('/usuarios/<id>', methods =['PUT'])
def actualizar_usuarios(id):
    try:
        cursor=conexion.connection.cursor()
               
        sql = """UPDATE usuarios SET first_name='{0}', last_name='{1}', email='{2}', password='{3}', token='{4}', age={5}, image='{6}', description='{7}' 
                 WHERE id={8}""".format(request.json['first_name'], request.json['last_name'], request.json['email'], request.json['password'],request.json['token'], request.json['age'], request.json['image'], request.json['description'], id)
        
        cursor.execute(sql)
        
        conexion.connection.commit()
        
        return jsonify({'mensaje':"usuario actualizado"})
                
    except Exception as ex:
        return jsonify({'mensaje':"error"})
    

  
@app.route('/usuarios/<id>', methods =['DELETE'])
def eliminar_usuarios(id):
    try:
        cursor=conexion.connection.cursor()
        
        sql="DELETE FROM usuarios WHERE id = '{0}'".format(id)
        
        cursor.execute(sql) #ejecuta la conexion
        
        conexion.connection.commit()  #confirma la insercion    
        #print(request.json)
        return jsonify({'mensaje':"usuario eliminado"})      
                
    except Exception as ex:
        return jsonify({'mensaje':"error"})
       
    
        
def pagina_no_encontrada(error):
    return "<h1>La página no existe...</h1>", 404   
   
if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()
    