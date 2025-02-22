from flask import Flask, render_template, request, flash, redirect,url_for
import pickle
import numpy as np
from PIL import Image
from flask_socketio import SocketIO, emit, join_room, leave_room



app = Flask(__name__)

app.config['SECRET_KEY'] = '12345'
socketio = SocketIO(app)
emergency_data = []
user_sockets = {} 
request_count=0

def predict(values, dic):
    if len(values) == 8:
        model = pickle.load(open('models/diabetes1.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 26:
        model = pickle.load(open('models/cancer.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 13:
        model = pickle.load(open('models/heart.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 18:
        model = pickle.load(open('models/kidney.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 10:
        model = pickle.load(open('models/liver.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]


@app.route("/")
def home():
    return render_template('index.html')




# Store emergency data and user socket mappings
 # Maps mobile_number to socket ID

@app.route('/user')
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/first-aid', methods=['GET'])
def first_aid():
    return redirect("http://127.0.0.1:8501", code=302) 
@app.route('/chat_bot', methods=['GET'])
def chat_bot():
    return redirect("http://127.0.0.1:8502", code=302) 
@app.route('/qrcode', methods=['GET'])
def qrcode():
    return redirect("http://127.0.0.1:3019", code=302)



@app.route('/hospital')
def hospital_dashboard():
    return render_template('hospital_dashboard.html', emergencies=emergency_data)

@socketio.on('connect')
def on_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def on_disconnect():
    print(f"Client disconnected: {request.sid}")
    # Remove disconnected users from user_sockets
    for symptoms,mobile, sid in list(user_sockets.items()):
        if sid == request.sid:
            del user_sockets[mobile]

@socketio.on('send_emergency')
def handle_emergency(data):
    mobile_number = data.get('mobile_number')
    symptoms = data.get('symptoms')

    latitude = data.get('latitude')
    longitude = data.get('longitude')
    global request_count

    if mobile_number and latitude and longitude:
        request_count += 1  # Increment request count

        emergency = {
            'id': len(emergency_data) + 1,
            'mobile_number': mobile_number,
            'symptoms':symptoms,
            'latitude': latitude,
            'longitude': longitude,
            'status': 'Pending',
            'sid': request.sid  # Store socket ID for this emergency
        }
        
        emergency_data.append(emergency)
        user_sockets[mobile_number] = request.sid  # Map mobile number to socket ID
        # Notify all connected hospitals about the new emergency
        socketio.emit('new_emergency', emergency, namespace='/')
        socketio.emit('update_request_count', {'count': request_count}, namespace='/')


@socketio.on('mark_as_sent')
def mark_as_sent(data):
    emergency_id = data.get('id')
    for emergency in emergency_data:
        if emergency['id'] == emergency_id:
            emergency['status'] = 'Sent'
            user_sid = emergency.get('sid')  # Get the socket ID of the user
            if user_sid:
                socketio.emit('emergency_sent', {'id': emergency_id}, to=user_sid, namespace='/')
            break

@socketio.on('acknowledge_emergency')
def acknowledge_emergency(data):
    emergency_id = data.get('id')
    for emergency in emergency_data:
        if emergency['id'] == emergency_id:
            emergency['status'] = 'Acknowledged'
            hospital_sid = request.sid
            # Notify the hospital dashboard with the updated status
            socketio.emit('emergency_acknowledged', emergency, to=hospital_sid, namespace='/')
            break

@socketio.on('assign_to_ambulance')
def assign_to_ambulance(data):
    emergency_id = data.get('id')
    for emergency in emergency_data:
        if emergency['id'] == emergency_id:
            emergency['status'] = 'Assigned to Ambulance'
            # Notify all hospitals about the status update
            socketio.emit('emergency_updated', emergency, namespace='/')
            break



@app.route("/disease")
def disease():
    return render_template('home.html')
@app.route("/hospital_locator")
def hospital():
    return render_template('hospital.html')
@app.route("/sign-in")
def sign():
    return redirect("http://127.0.0.1:3019/view", code=302)

@app.route("/diabetes", methods=['GET', 'POST'])
def diabetesPage():
    return render_template('diabetes.html')

@app.route("/cancer", methods=['GET', 'POST'])
def cancerPage():
    return render_template('breast_cancer.html')

@app.route("/heart", methods=['GET', 'POST'])
def heartPage():
    return render_template('heart.html')

@app.route("/kidney", methods=['GET', 'POST'])
def kidneyPage():
    return render_template('kidney.html')

@app.route("/liver", methods=['GET', 'POST'])
def liverPage():
    return render_template('liver.html')

@app.route("/malaria", methods=['GET', 'POST'])
def malariaPage():
    return render_template('malaria.html')

@app.route("/pneumonia", methods=['GET', 'POST'])
def pneumoniaPage():
    return render_template('pneumonia.html')

@app.route("/predict", methods = ['POST', 'GET'])
def predictPage():
    try:
        if request.method == 'POST':
            to_predict_dict = request.form.to_dict()
            to_predict_list = list(map(float, list(to_predict_dict.values())))
            pred = predict(to_predict_list, to_predict_dict)
    except:
        message = "Please enter valid Data"
        return render_template("home.html", message = message)

    return render_template('predict.html', pred = pred)

@app.route('/map')
def show_map():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    return render_template('map.html', lat=lat, lng=lng)

if __name__ == '__main__':
	socketio.run(app, debug=True)
    