# CareSathi

CareSathi is a healthcare web application designed to enhance accessibility for differently-abled individuals.This project aims to provide a seamless experience for patients, caregivers, and medical professionals by integrating various technologies like AI, Blockchain, and NLP.

## Features
- **AI-Powered Chatbot**: Provides real-time assistance to users by retrieving relevant medical information.
- **Blockchain-Based Medical Records**: Ensures secure and tamper-proof storage of patient data.
- **Emergency Services**: Helps users quickly connect with emergency responders and hospitals.
- **Accessible UI**: Designed for ease of use, particularly for visually impaired or physically disabled individuals.
- **Prescription Management**: Generates and manages digital prescriptions using QR codes.
- **Appointment Scheduling**: Streamlines the booking process for medical consultations.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: MongoDB
- **AI & NLP**: LangChain, Hugging Face Models
- **Blockchain**: Used for secure medical record management
- **QR Code**: Used for prescription storage and retrieval

## Multi Disease Predictor
This module predicts the likelihood of multiple diseases based on user input.

### Prerequisites
- Python 3.x
- Required Python packages (listed in `requirements.txt`)

### Setup Instructions
#### Clone the Repository:
```bash
git clone https://github.com/div9ya/caresathi.git
cd caresathi/Multi_Disease_Predictor
```

#### Create a Virtual Environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

#### Install Dependencies:
```bash
pip install -r requirements.txt
```

#### Run the Application:
```bash
python app.py
```
The application should now be running locally. Access it via [http://localhost:5000](http://localhost:5000) in your browser.

---

## Chatbot (Using Streamlit)
An interactive chatbot designed to assist users with healthcare-related queries.

### Prerequisites
- Python 3.x
- Required Python packages (listed in `requirements.txt`)
- Streamlit for UI

### Setup Instructions
#### Navigate to the Chatbot Directory:
```bash
cd caresathi/chatbot
```

#### Create a Virtual Environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

#### Install Dependencies:
```bash
pip install -r requirements.txt
```

#### Run the Streamlit Chatbot Application:
```bash
streamlit run chatbot.py
```
The chatbot should now be running, and you can access it via the URL displayed in the terminal.

---

## Medical Bot First Aid (Using Streamlit)
A bot providing first aid information and guidance.

### Prerequisites
- Python 3.x
- Required Python packages (listed in `requirements.txt`)
- Streamlit for UI

### Setup Instructions
#### Navigate to the Medical Bot Directory:
```bash
cd caresathi/medical_bot_first_aid
```

#### Create a Virtual Environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

#### Install Dependencies:
```bash
pip install -r requirements.txt
```

#### Run the Streamlit Medical Bot Application:
```bash
streamlit run first_aid.py
```
The first-aid bot should now be running, and you can access it via the URL displayed in the terminal.

---

## QR Code Generator with MongoDB (Using Node.js & Nodemon)
This module generates QR codes and integrates with a MongoDB database using Node.js.

### Prerequisites
- Node.js (Latest LTS version recommended)
- npm (Node Package Manager)
- MongoDB (local or remote instance)
- Nodemon (for automatic server restarts)

### Setup Instructions
#### Navigate to the QR Code Directory:
```bash
cd caresathi/qrcode/mongodb2
```

#### Install Dependencies:
```bash
npm install
```

#### Ensure MongoDB is Running
If using local MongoDB, start the service:
```bash
mongod --dbpath /path/to/data/db
```
If using remote MongoDB (Atlas), update the MongoDB connection string in `config.js` or `.env` file.

#### Run the Application (with Nodemon for Auto Restarting):
```bash
npx nodemon server.js
```
If you don’t have nodemon installed globally, install it first:
```bash
npm install -g nodemon
```
Then run:
```bash
nodemon server.js
```

#### Access the Application
The QR code service should be running at:
```bash
http://localhost:3019
```
Test the API using Postman or any browser.


## Contributors
- **Divya Verma**
- **Mridul Singh Soam**
- **Akshat Srivastava**
- **Saksham Katiyar**

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it.

## Contact
For any queries or contributions, feel free to open an issue or reach out to the contributors.

