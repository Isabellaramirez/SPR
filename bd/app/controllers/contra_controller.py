from flask import Blueprint, render_template, request, redirect, url_for, current_app, session
from flask_bcrypt import Bcrypt

contra_bp = Blueprint('contra_bp', __name__)
bcrypt = Bcrypt()

@contra_bp.route('/perfil/contratista')
def perfil_contratista():
    user_correo = session.get('user_correo')
    connection = current_app.connection
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuario WHERE correo=%s", (user_correo,))
            user = cursor.fetchone()
    except Exception as e:
        current_app.logger.error(f"Error al obtener información del usuario: {e}")
        return "Ocurrió un error al obtener la información del usuario."
    
    return render_template('perfil_contratista.html', user=user)

@contra_bp.route('/listar_contratistas')
def listar_contratistas():
    connection = current_app.connection
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuario WHERE rol_id_rol = 2")  # Suponiendo que 1 es el ID de Contratista
            contratistas = cursor.fetchall()
    except Exception as e:
        current_app.logger.error(f"Error al obtener contratistas: {e}")
        return "Ocurrió un error al obtener los contratistas."
    
    return render_template('listar_contratistas.html', contratistas=contratistas)

# Agrega otras rutas relacionadas con contratistas aquí si es necesario
