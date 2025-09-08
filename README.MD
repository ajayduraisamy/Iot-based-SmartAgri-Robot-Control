# SmartAgri Robot - Control Center
==================================

This is the **SmartAgri Robot Control Center**, a web-based system built using **Flask (Python)** to monitor and control an agricultural robot. It provides a dashboard for real-time sensor data, device controls, and user management. The system integrates **software and hardware** to allow remote operation and monitoring of a robot for precision agriculture.

---

## Features
------------

- **User Management**
  - Register with name, email, phone, and profile image.
  - Login/logout with session management.
  - Profile view and update.

- **Robot Sensor Monitoring**
  - Collects data from robot sensors: temperature, humidity, soil moisture.
  - Stores sensor readings in the database and displays them in real-time.

- **Robot Control**
  - Control robot movements: front, back, left, right.
  - Commands are sent to the robot hardware through the web interface.

- **Dashboard**
  - Real-time visualization of robot sensor data.
  - Update and monitor system parameters.

- **Security**
  - Passwords are securely hashed.
  - Profile image uploads are validated and sanitized.

- **Responsive Web Interface**
  - Built with Flask and Jinja2 templates.
  - Displays current year dynamically.

---

## Technologies Used
-------------------

- **Backend:** Python, Flask, MySQL
- **Frontend:** HTML, CSS, Jinja2 Templates, Bootstrap (optional)
- **Hardware:** SmartAgri Robot sensors and actuators
- **Other Libraries:** Werkzeug, os, datetime

---




## Installation
----------------

1. **Clone the repository**

```bash
git clone https://github.com/ajayduraisamy/Iot-based-SmartAgri-Robot-Control.git
cd Iot-based-SmartAgri-Robot-Control




1. **Api url to hardware**

http://192.168.1.15:5000/update_sensor_data?temperature=20&humidity=30&soil_moisture=10

http://192.168.1.15:5000/control_data

http://192.168.1.15:5000/dashboard_data