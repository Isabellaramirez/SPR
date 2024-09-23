from flask import Blueprint, render_template, request, redirect, url_for, current_app, session
from flask_bcrypt import Bcrypt

pres_bp = Blueprint('pres_bp', __name__)
bcrypt = Bcrypt()

@pres_bp.route('/perfil/prestador')
def perfil_prestador():
    user_email = session.get('user_email')  # Cambiado a 'user_email' para coincidir con el código de inicio de sesión
    connection = current_app.connection
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuario WHERE correo=%s", (user_email,))
            user = cursor.fetchone()
    except Exception as e:
        current_app.logger.error(f"Error al obtener información del usuario: {e}")
        return "Ocurrió un error al obtener la información del usuario."
    
    return render_template('perfil_prestador.html', user=user)

@pres_bp.route('/listar_prestador')
def listar_prestador():
    connection = current_app.connection
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuario WHERE rol_id_rol = 2")  # Suponiendo que 2 es el ID de Prestador
            prestadores = cursor.fetchall()  # Cambiado a 'prestadores'
    except Exception as e:
        current_app.logger.error(f"Error al obtener prestadores: {e}")
        return "Ocurrió un error al obtener los prestadores."
    
    return render_template('listar_prestador.html', prestadores=prestadores)  # Cambiado a 'prestadores'

