from flask import Blueprint, render_template, request, redirect, url_for, current_app, session
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename

user_bp = Blueprint('user_bp', __name__)
bcrypt = Bcrypt()

# Define the upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/img')  # Asegúrate de que esta ruta sea correcta
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    connection = current_app.connection
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        descripcion = request.form['descripcion']
        correo = request.form['correo']
        fecha_nacimiento = request.form['fecha_nacimiento']
        contraseña = request.form['contraseña']
        rol_id_rol = request.form['role']
        foto = request.files.get('foto')

        # Manejo de la foto
        if foto and allowed_file(foto.filename):
            filename = secure_filename(foto.filename)
            foto_path = os.path.join(UPLOAD_FOLDER, filename)

            # Asegúrate de que la carpeta de subida exista
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            try:
                foto.save(foto_path)
                foto_url = url_for('static', filename=f'img/{filename}', _external=True)
            except Exception as e:
                current_app.logger.error(f"Error al guardar el archivo: {e}")
                foto_url = url_for('static', filename='img/default_profile.png', _external=True)
        else:
            foto_url = url_for('static', filename='img/default_profile.png', _external=True)

        hashed_password = bcrypt.generate_password_hash(contraseña).decode('utf-8')

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuario (cedula, nombre, apellido, telefono, direccion, descripcion, correo, fecha_nacimiento, contraseña, rol_id_rol, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (cedula, nombre, apellido, telefono, direccion, descripcion, correo, fecha_nacimiento, hashed_password, rol_id_rol, foto_url)
                )
                connection.commit()
            
            # Redirige al perfil basado en el rol
            if rol_id_rol == '1':  # Suponiendo que 1 es el ID de Contratista
                return redirect(url_for('contra_bp.perfil_contratista'))
            elif rol_id_rol == '2':  # Suponiendo que 2 es el ID de Prestador
                return redirect(url_for('pres_bp.perfil_prestador'))
            else:
                return "Rol no reconocido."
        except Exception as e:
            current_app.logger.error(f"Error al registrar usuario: {e}")
            return "Ocurrió un error al registrar el usuario."

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_rol, nombre_rol FROM rol")
            roles = cursor.fetchall()
    except Exception as e:
        current_app.logger.error(f"Error al obtener roles: {e}")
        return "Ocurrió un error al obtener los roles."
    
    return render_template('registro.html', roles=roles)

@user_bp.route('/inicio_de_sesion', methods=['GET', 'POST'])
def inicio_de_sesion():
    connection = current_app.connection
    
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        rol_id_rol = request.form['role']  # Asegúrate de que el nombre del campo coincida con el HTML

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT contraseña FROM usuario WHERE correo=%s AND rol_id_rol=%s", (correo, rol_id_rol))
                result = cursor.fetchone()
                if result and bcrypt.check_password_hash(result['contraseña'], contraseña):
                    session['user_email'] = correo  # Guarda el email del usuario en la sesión
                    session['user_role'] = rol_id_rol  # Guarda el rol del usuario en la sesión
                    
                    # Redirige basado en el rol
                    if rol_id_rol == '1':  # Suponiendo que 1 es el ID de Contratista
                        return redirect(url_for('contra_bp.perfil_contratista'))
                    elif rol_id_rol == '2':  # Suponiendo que 2 es el ID de Prestador
                        return redirect(url_for('pres_bp.perfil_prestador'))
                    else:
                        return "Rol no reconocido."
                else:
                    return "Correo, contraseña o rol incorrectos. Por favor, inténtalo de nuevo."
        except Exception as e:
            current_app.logger.error(f"Error al iniciar sesión: {e}")
            return "Ocurrió un error al iniciar sesión."

    # Maneja el caso GET
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_rol, nombre_rol FROM rol")
            roles = cursor.fetchall()
    except Exception as e:
        current_app.logger.error(f"Error al obtener roles: {e}")
        return "Ocurrió un error al obtener los roles."
    
    return render_template('inicio_de_sesion.html', roles=roles)
