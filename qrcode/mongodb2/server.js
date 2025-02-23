const express=require('express')
const mongoose=require('mongoose')
const path=require('path')
const qr = require('qr-image'); // Import qr-image for QR code generation
const multer = require('multer'); // Middleware for file uploads
const { GridFSBucket } = require('mongodb'); // Import GridFSBucket for storing images
const fs = require('fs');
const port=3019
const app=express()
app.use(express.static(__dirname))
app.use(express.urlencoded({extended:true}))
app.use(express.static('static')); // Serving from 'static' 


mongoose.connect('mongodb://127.0.0.1:27017/students', { useNewUrlParser: true, useUnifiedTopology: true })
const db=mongoose.connection
let bucketPrescriptions;
let bucketQR;
db.once('open', () => {
    console.log("MongoDB connection successful");
    bucketPrescriptions = new GridFSBucket(db.db, { bucketName: 'prescriptions' }); // Store prescriptions
    bucketQR = new GridFSBucket(db.db, { bucketName: 'qrCodes' }); 
});
const storage = multer.memoryStorage();
const upload = multer({ storage });



const userSchema=new mongoose.Schema({
    regd_no:String,
    name:String,
    email:String,
    dob: String,
    gender: String,
    contact: String,
    address: String,
    emergency_contact: String,
    allergies: String,
    medications: String,
    chronic: String,
    symptoms: String,
    prescription_images: [String],
    qr_code:String
})

const Users=mongoose.model("data",userSchema)
app.get('/',(req,res)=>{
    res.sendFile(path.join(__dirname,'./templates/form.html'))
})

app.get('/view', (req, res) => {
    res.sendFile(path.join(__dirname, './templates/view.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, './templates/.html'));
});
app.post('/post', upload.array('prescriptions', 5), async (req, res) => {
    try {
        const { regd_no, name, email,  dob, gender, contact, address, emergency_contact, allergies, medications, chronic, symptoms } = req.body;
        const files = req.files;

        if (!files || files.length === 0) return res.status(400).send("No prescription images uploaded.");

        let imageFilenames = [];

        
        for (const file of files) {
            await new Promise((resolve, reject) => {
                const filename = `${regd_no}_${file.originalname}`;
                const uploadStream = bucketPrescriptions.openUploadStream(filename);
                uploadStream.end(file.buffer, (err) => {
                    if (err) return reject(err);
                    imageFilenames.push(filename);
                    resolve();
                });
            });
        }


            // Generate QR Code URL
            const qrData = `http://localhost:${port}/patient/${regd_no}`;
            const qrImage = qr.imageSync(qrData, { type: 'png' });

            // Save QR Code in GridFS
            const qrUploadStream = bucketQR.openUploadStream(`${regd_no}_qr.png`);
            qrUploadStream.end(qrImage, async (err) => {
                if (err) {
                    console.error('Error saving QR code:', err);
                    return res.status(500).send("Error generating QR code.");
                }

                // Save Patient Data in MongoDB
                const user = new Users({
                    regd_no,
                    name,
                    email,
                    dob,
                    gender, 
                    contact, 
                    address, 
                    emergency_contact, 
                    allergies, 
                    medications, 
                    chronic, 
                    symptoms,
                    prescription_images: imageFilenames,
                    qr_code: `${regd_no}_qr.png`
                });

                await user.save();
                res.sendFile(path.join(__dirname, './templates/success.html'));
            });
        
    } catch (error) {
        console.error('Error processing request:', error);
        res.status(500).send("An error occurred while processing your request.");
    }
});


app.get('/patient/:regd_no', async (req, res) => {
    const regd_no = req.params.regd_no;
    const user = await Users.findOne({ regd_no });
    if (!user) {
        return res.status(404).send("Patient not found.");
    }

    let imagesHtml = "";
    user.prescription_images.forEach(img => {
        imagesHtml += `<img src="/image/${img}" alt="Prescription Image" style="max-width: 300px; display: block; margin-bottom: 10px;">`;
    });
    res.send(`
        <link rel="stylesheet" href="/css/display.css">
        <div class="top">
        <img src="/images/Ellipse 145.png" alt="">
        </div>
        <div class="bottom">
        <img src="/images/Ellipse 144.png" alt="">
        </div>
        <div class="container">
            <h1>Patient Information</h1>
            <p><strong>Registration Number:</strong> ${user.regd_no}</p>
            <p><strong>Full Name:</strong> ${user.name}</p>
            <p><strong>Email:</strong> ${user.email}</p>
            <p><strong>Date of Birth:</strong> ${user.dob}</p>
            <p><strong>Gender:</strong> ${user.gender}</p>
            <p><strong>Contact:</strong> ${user.contact}</p>
            <p><strong>Address:</strong> ${user.address}</p>
            <p><strong>Emergency Contact:</strong> ${user.emergency_contact}</p>
            <p><strong>Allergies:</strong> ${user.allergies}</p>
            <p><strong>Medications:</strong> ${user.medications}</p>
            <p><strong>Chronic Diseases:</strong> ${user.chronic}</p>
            <p><strong>Symptoms:</strong> ${user.symptoms}</p>
            <img src="/qr/${user.regd_no}" alt="QR Code" />
            <h3>Prescription:</h3>
            ${imagesHtml}
        </div>
    `);
    
});

// Serve Prescription Image
app.get('/image/:filename', async (req, res) => {
    const filename = req.params.filename;

    const downloadStream = bucketPrescriptions.openDownloadStreamByName(filename);
    res.set("Content-Type", "image/png");
    downloadStream.pipe(res);
});

app.get('/qr/:regd_no', async (req, res) => {
    const regd_no = req.params.regd_no;
    const user = await Users.findOne({ regd_no });
    if (!user || !user.qr_code) {
        return res.status(404).send("QR code not found.");
    }

    
    const downloadStream = bucketQR.openDownloadStreamByName(user.qr_code);
    res.set("Content-Type", "image/png");
    downloadStream.pipe(res);
});

// Add this route to serve the login page
app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, './templates/login.html'));
});

// Handle login request
app.post('/login', async (req, res) => {
    const { regd_no, contact } = req.body;

    // Find the user by registration number
    const user = await Users.findOne({ regd_no });
    if (!user) {
        return res.status(404).send("Patient not found.");
    }

    // Check if the provided contact number matches the stored contact number
    if (user.contact !== contact) {
        return res.status(401).send("Invalid phone number.");
    }

    // Redirect to the patient details page
    res.redirect(`/patient/${regd_no}`);
});

app.listen(port,()=>(
    console.log("Server started")
))