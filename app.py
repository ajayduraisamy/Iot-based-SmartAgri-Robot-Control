from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import mysql.connector
from model import get_db_connection
from datetime import datetime


def allowed_file(filename, filetype):
    if filetype == 'image':
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
    return False



app = Flask(__name__)
app.secret_key = 'wverihdfuvuwi2482'



app.config['PROFILE_UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'profiles')
os.makedirs(app.config['PROFILE_UPLOAD_FOLDER'], exist_ok=True)


@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        password = request.form['password']
        profile_image = request.files['profile_image']

        if profile_image and allowed_file(profile_image.filename, 'image'):
            filename = secure_filename(profile_image.filename)
            image_path = os.path.join(app.config['PROFILE_UPLOAD_FOLDER'], filename)
            profile_image.save(image_path)
        else:
            flash('Invalid image file.', 'danger')
            return redirect(request.url)

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (name, email, number, password, image_path) VALUES (%s, %s, %s, %s, %s)',
                (name, email, number, hashed_password, filename)
            )
            conn.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Email already exists.', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html', title="Register")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()
    
        if user and check_password_hash(user['password'], password):
            print("Stored hash:", user['password'])
            print("Entered password:", password)

            session['email'] = user['email']
            session['name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', title="Login")

@app.route('/contact' , methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/profile')
def profile():
    if 'email' not in session:
        flash('Please login to view your profile.', 'warning')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) 
    cursor.execute("SELECT * FROM users WHERE email = %s", (session['email'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('login'))

    return render_template('profile.html', user=user)





@app.route('/controls', methods=['GET', 'POST'])
def controls():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form.get('value', '0')  

        action_map = {
            '1': 'Front',
            '2': 'Back',
            '3': 'Left',
            '4': 'Right'
        }
        action_text = action_map.get(action, 'Unknown')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE control_data SET action = %s WHERE id = 1",
            (action,)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f'Control : {action_text}', 'success')
        return redirect(url_for('controls'))

    return render_template('controls.html', title="Controls")


@app.route('/control_data', methods=['GET', 'POST'])
def control_data():
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  
        cursor.execute('SELECT * FROM control_data WHERE id = 1')
        control = cursor.fetchone()
        cursor.close()
        conn.close()

        if control:
            return str(control['action']), 200
        else:
            return "No control data found", 404


@app.route('/update_sensor_data', methods=['GET'])
def get_sensor_data():
   
    temperature = request.args.get("temperature", "0")
    humidity = request.args.get("humidity", "0")
    soil_moisture = request.args.get("soil_moisture", "0")

   
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor_data (temperature, humidity, soil_moisture) VALUES (%s, %s, %s)",
        (str(temperature), str(humidity), str(soil_moisture))
    )
    conn.commit()
    cursor.close()
    conn.close()

    return "Sensor Data Stored Successfully", 200





@app.route('/sensordata')
def sensordata():
    if 'email' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) 
    cursor.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC')
    sensor_data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('sensordata.html', title="Sensor Data", sensor_data=sensor_data)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        value = request.form.get('value', '0')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE dashboard_data SET value = %s WHERE id = 1",
            (value,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        flash(f'Dashboard updated with value {value}', 'success')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', title="Dashboard")

@app.route('/dashboard_data', methods=['GET'])
def dashboard_data():

    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  
        cursor.execute('SELECT * FROM dashboard_data WHERE id = 1')
        control = cursor.fetchone()
        cursor.close()
        conn.close()

        if control:
            return str(control['value']), 200
        else:
            return "No control data found", 404

    return jsonify({"message": "Dashboard data"})



@app.route('/camera', methods = ['GET', 'POST'])
def camera_feed():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('camera.html', title="Camera ")


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
