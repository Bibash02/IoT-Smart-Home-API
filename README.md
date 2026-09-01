# 🏠 SmartHome IoT API

> A scalable and secure **IoT Smart Home Backend API** built with **Python, Django REST Framework, MQTT, and JWT Authentication** for managing smart devices, sensors, automation, notifications, and energy consumption.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Django](https://img.shields.io/badge/Django-REST_Framework-green?logo=django)
![API](https://img.shields.io/badge/API-REST-orange)
![MQTT](https://img.shields.io/badge/IoT-MQTT-purple)
![Authentication](https://img.shields.io/badge/Auth-JWT-red)
![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

**SmartHome IoT API** is a backend system designed to provide a centralized platform for controlling and monitoring IoT devices in a smart home environment.

The system allows authenticated users to:

* 🏠 Manage rooms
* 💡 Manage smart devices
* 🌡️ Monitor sensors
* 🎛️ Send commands to devices
* 🤖 Create automation rules
* 🔔 Receive system notifications
* ⚡ Monitor energy consumption
* 📊 Analyze energy usage
* 📡 Communicate with IoT devices using MQTT
* 🔐 Secure APIs using JWT authentication

The project is designed with a modular architecture so that additional IoT devices, sensors, automation rules, and analytics features can be added easily.

---

# ✨ Features

## 🔐 Authentication & Authorization

* User authentication using JWT
* Access and refresh tokens
* Protected REST APIs
* User-specific resources
* Ownership-based authorization
* Secure device control

---

## 🏠 Room Management

Users can organize their smart home devices into different rooms.

Example:

```text
Home
├── Living Room
├── Bedroom
├── Kitchen
├── Bathroom
└── Office
```

Supported operations:

* Create room
* View rooms
* Update room
* Delete room
* View room-specific devices

---

## 💡 Smart Device Management

The system supports multiple device types:

```text
LIGHT
FAN
AC
TV
LOCK
CAMERA
SENSOR
SWITCH
OTHER
```

Each device can have:

* Name
* Device UID
* Device type
* Room
* Online/offline status
* Power status
* Owner

Example:

```text
Living Room Light
Device UID: LIGHT-001
Type: LIGHT
Status: ON
Online: Yes
```

---

# 🎛️ Device Command System

The API provides a centralized system for controlling IoT devices.

Supported commands:

```text
POWER
LIGHT
SPEED
TEMPERATURE
LOCK
UNLOCK
```

Example:

```json
{
    "command": "POWER",
    "value": "ON"
}
```

Command lifecycle:

```text
API Request
     ↓
Validate Command
     ↓
Check Device Ownership
     ↓
Check Device Online
     ↓
Create DeviceCommand
     ↓
Execute Command
     ↓
Update Device Status
     ↓
Return Response
```

Every command stores:

* Command type
* Value
* Status
* Response
* Created time
* Executed time

Command statuses:

```text
PENDING
SUCCESS
FAILED
```

---

# 🌡️ Sensor Monitoring

The system supports IoT sensor data collection and monitoring.

Sensor data can be used for:

* Temperature monitoring
* Humidity monitoring
* Motion detection
* Light detection
* Security monitoring
* Automation triggers

Example sensor data:

```json
{
    "temperature": 30.5,
    "humidity": 65
}
```

Sensor workflow:

```text
IoT Sensor
    ↓
MQTT
    ↓
Django MQTT Handler
    ↓
Sensor Reading
    ↓
Database
    ↓
Automation Engine
```

---

# 🤖 Smart Automation

Users can create automation rules based on sensor values.

Example:

```text
IF temperature > 30°C
THEN turn ON fan
```

Another example:

```text
IF temperature < 20°C
THEN turn OFF AC
```

Automation structure:

```text
Sensor
   ↓
Read Sensor Value
   ↓
Check Condition
   ↓
Compare Threshold
   ↓
Condition Satisfied?
   ↓
Execute Device Command
   ↓
Create Notification
```

Supported operators:

```text
>
<
=
>=
<=
```

Supported actions:

```text
TURN_ON
TURN_OFF
```

---

# ⚡ Energy Monitoring

The system tracks energy consumption of smart devices.

Energy readings include:

```text
Voltage
Current
Power
Energy Consumed
Timestamp
```

Example:

```json
{
    "voltage": 230,
    "current": 0.43,
    "power": 98.9
}
```

Energy calculation:

```text
Energy = Power × Time
```

The system provides:

* Device energy readings
* Daily energy usage
* Weekly energy usage
* Monthly energy usage
* Total energy consumption
* Highest consuming device
* Average power
* Maximum power
* Energy alerts

Energy flow:

```text
IoT Device
     ↓
Voltage / Current / Power
     ↓
MQTT
     ↓
Django
     ↓
EnergyReading
     ↓
Energy Calculation
     ↓
Analytics API
     ↓
Dashboard
```

---

# 🔔 Notification System

The notification system keeps users informed about important events.

Notification categories:

```text
SECURITY
SENSOR
DEVICE
AUTOMATION
ENERGY
SYSTEM
```

Examples:

```text
🔔 Device Offline

Bedroom Fan has gone offline.
```

```text
🔔 Automation Executed

Automation "Turn Fan On" executed successfully.
```

```text
🔔 High Energy Usage

Living Room AC has consumed 5.2 kWh today.
```

Notification features:

* Get notifications
* Unread notification count
* Mark notification as read
* Mark all notifications as read
* User-specific notifications

---

# 📡 MQTT IoT Communication

MQTT is used as the communication protocol between the Django backend and IoT devices.

Communication architecture:

```text
                    MQTT Broker
                   /           \
                  /             \
             Django             ESP32
               API                │
                │                 │
                └──── Commands ──┘
                │
                └──── Sensor Data
```

Example MQTT topics:

```text
smarthome/device/<device_uid>/sensor
smarthome/device/<device_uid>/status
smarthome/device/<device_uid>/response
smarthome/device/<device_uid>/heartbeat
smarthome/device/<device_uid>/energy
```

### Sensor Data

```text
ESP32
  ↓
MQTT Publish
  ↓
Django MQTT Subscriber
  ↓
Store Sensor Reading
```

### Device Command

```text
Frontend
   ↓
REST API
   ↓
Django
   ↓
DeviceCommand
   ↓
MQTT Publish
   ↓
ESP32
   ↓
Device
```

---

# 🏗️ System Architecture

```text
                         ┌──────────────────┐
                         │     Frontend     │
                         │ Web / Mobile App │
                         └────────┬─────────┘
                                  │
                              REST API
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │     Django REST API     │
                    ├─────────────────────────┤
                    │ Authentication          │
                    │ Room Management         │
                    │ Device Management       │
                    │ Sensor Management       │
                    │ Automation               │
                    │ Notifications            │
                    │ Energy Analytics         │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┼────────────────┐
                 │               │                │
                 ▼               ▼                ▼
             Database       MQTT Broker       Services
                 │               │                │
                 │               │                │
                 ▼               ▼                ▼
             User Data        ESP32          Automation
             Devices          Sensors         Energy
             Sensors          Devices         Notification
             Energy
```

---

# 🗄️ Database Design

The major models include:

```text
User
 │
 ├── Room
 │    └── Device
 │         ├── DeviceCommand
 │         └── EnergyReading
 │
 ├── Sensor
 │    └── SensorReading
 │
 ├── AutomationRule
 │
 └── Notification
```

### Main Models

| Model          | Purpose                         |
| -------------- | ------------------------------- |
| User           | Authentication and ownership    |
| Room           | Organizes devices               |
| Device         | Stores smart device information |
| DeviceCommand  | Stores device commands          |
| Sensor         | Stores IoT sensors              |
| SensorReading  | Stores sensor measurements      |
| AutomationRule | Defines automation logic        |
| Notification   | Stores user notifications       |
| EnergyReading  | Stores energy measurements      |

---

# 🔄 Complete Smart Home Workflow

```text
                    USER
                     │
                     ▼
                Login / JWT
                     │
                     ▼
              Smart Home API
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      Room         Device       Sensor
        │            │            │
        │            │            ▼
        │            │       Sensor Data
        │            │            │
        │            │            ▼
        │            │      Automation Rule
        │            │            │
        │            ▼            ▼
        │       Device Command ←─┘
        │            │
        │            ▼
        │       MQTT Broker
        │            │
        │            ▼
        │           ESP32
        │            │
        │            ▼
        │          Device
        │
        └──────────────┐
                       ▼
                 Notification
                       │
                       ▼
                  User 🔔

Energy:
ESP32 → MQTT → EnergyReading → Analytics → Dashboard
```

---

# 📁 Project Structure

```text
smart-home-api/
│
├── manage.py
│
├── smarthome/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── room/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── devices/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   └── urls.py
│
├── sensors/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── automation/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   └── urls.py
│
├── notifications/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   └── urls.py
│
├── energy/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   └── urls.py
│
├── iot/
│   ├── client.py
│   ├── handlers.py
│   └── topics.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# 🛠️ Technologies Used

### Backend

* Python
* Django
* Django REST Framework

### Authentication

* JWT
* Simple JWT

### IoT Communication

* MQTT
* ESP32

### Database

* SQLite for development
* PostgreSQL for production

### API Testing

* Postman

### API Documentation

* Swagger / OpenAPI

### Deployment

Can be deployed using:

* Gunicorn
* Nginx
* Docker
* PostgreSQL
* Cloud hosting

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/your-username/smart-home-api.git
```

```bash
cd smart-home-api
```

---

## 2. Create virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=smart_home
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
```

> Never commit your `.env` file to GitHub.

---

## 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Create superuser

```bash
python manage.py createsuperuser
```

---

## 7. Start Django server

```bash
python manage.py runserver
```

API will be available at:

```text
http://127.0.0.1:8000/
```

---

# 🔑 Authentication

Login:

```http
POST /api/auth/login/
```

Request:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

Response:

```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```

Use the access token:

```http
Authorization: Bearer <access_token>
```

---

# 📡 API Endpoints

## Authentication

```text
POST   /api/auth/login/
POST   /api/auth/token/refresh/
GET    /api/auth/me/
```

## Rooms

```text
GET      /api/rooms/
POST     /api/rooms/
GET      /api/rooms/<id>/
PUT      /api/rooms/<id>/
PATCH    /api/rooms/<id>/
DELETE   /api/rooms/<id>/
```

## Devices

```text
GET      /api/devices/
POST     /api/devices/
GET      /api/devices/<id>/
PUT      /api/devices/<id>/
PATCH    /api/devices/<id>/
DELETE   /api/devices/<id>/
POST     /api/devices/<id>/command/
```

## Sensors

```text
GET      /api/sensors/
POST     /api/sensors/
GET      /api/sensors/<id>/
PUT      /api/sensors/<id>/
DELETE   /api/sensors/<id>/
```

## Automation

```text
GET      /api/automation/
POST     /api/automation/
GET      /api/automation/<id>/
PUT      /api/automation/<id>/
DELETE   /api/automation/<id>/
```

## Notifications

```text
GET      /api/notifications/
GET      /api/notifications/unread-count/
PATCH    /api/notifications/<id>/read/
PATCH    /api/notifications/read-all/
```

## Energy

```text
GET      /api/energy/readings/
GET      /api/energy/summary/
GET      /api/energy/today/
GET      /api/energy/weekly/
```

---

# 🧪 Testing

The API can be tested using **Postman**.

Recommended testing flow:

```text
1. Register/Login
        ↓
2. Get JWT Token
        ↓
3. Create Room
        ↓
4. Create Device
        ↓
5. Create Sensor
        ↓
6. Send Sensor Data
        ↓
7. Create Automation Rule
        ↓
8. Trigger Automation
        ↓
9. Execute Device Command
        ↓
10. Generate Notification
        ↓
11. Generate Energy Reading
        ↓
12. Check Energy Analytics
```

---

# 🔒 Security

The project follows several security practices:

* JWT authentication
* Protected API endpoints
* User-based authorization
* Device ownership validation
* Sensor ownership validation
* Notification ownership
* Environment variables for secrets
* Input validation
* Command validation
* Device online-status validation

A user cannot control or access another user's smart-home devices.

---

# 🚀 Future Improvements

Planned features include:

* [ ] Real-time WebSocket notifications
* [ ] Real-time device status updates
* [ ] Mobile application
* [ ] Web dashboard
* [ ] Advanced energy cost calculation
* [ ] Electricity tariff/slab configuration
* [ ] AI-based energy optimization
* [ ] AI-powered automation suggestions
* [ ] Voice-controlled devices
* [ ] Camera monitoring
* [ ] Security alerts
* [ ] Device scheduling
* [ ] Scene management
* [ ] Multi-home support
* [ ] Docker deployment
* [ ] PostgreSQL production setup
* [ ] CI/CD pipeline
* [ ] Automated testing
* [ ] Cloud deployment

---

# 💡 Example Automation

### Scenario

Turn on the fan automatically when the temperature becomes greater than 30°C.

```text
Temperature Sensor
       │
       │ 32°C
       ▼
Automation Engine
       │
       │ 32 > 30
       ▼
Condition TRUE
       │
       ▼
TURN_ON Fan
       │
       ▼
DeviceCommand
       │
       ▼
MQTT
       │
       ▼
ESP32
       │
       ▼
Fan ON
       │
       ▼
Notification 🔔
```

---

# 📊 Example Energy Dashboard

```text
┌──────────────────────────────────────────┐
│             ENERGY DASHBOARD             │
├──────────────────────────────────────────┤
│                                          │
│ Today's Usage       Monthly Usage        │
│    4.82 kWh            87.35 kWh         │
│                                          │
│ Highest Consumer                          │
│ Living Room AC       42.80 kWh           │
│                                          │
│ Average Power                             │
│ 435 W                                    │
│                                          │
│ Weekly Usage                              │
│ Mon ███                                  │
│ Tue █████                                │
│ Wed ████                                 │
│ Thu ██████                               │
│ Fri █████                                │
│ Sat ███████                              │
│ Sun █████                                │
│                                          │
└──────────────────────────────────────────┘
```

---

# 🎯 Project Goals

The main goals of this project are:

1. Build a centralized smart-home backend.
2. Provide secure REST APIs for IoT devices.
3. Enable real-time communication using MQTT.
4. Automate devices based on sensor conditions.
5. Monitor energy consumption.
6. Provide meaningful notifications.
7. Build a scalable architecture for future IoT features.

---

# 👨‍💻 Author

**Bibash Bayalkoti**

Backend Developer | Python | Django | REST API | IoT

### Skills demonstrated in this project

```text
Python
Django
Django REST Framework
REST API Design
JWT Authentication
MQTT
IoT Architecture
Database Design
Automation Logic
Energy Analytics
API Security
Postman
Swagger / OpenAPI
```
