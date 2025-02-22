// Initialize the map
let map = L.map('map').setView([20.5937, 78.9629], 5); // Default to India

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Get User's Location
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(async (position) => {
        let lat = position.coords.latitude;
        let lon = position.coords.longitude;

        document.getElementById("status").innerText = "Location found! Searching for hospitals...";

        // Add user marker
        let userMarker = L.marker([lat, lon]).addTo(map)
            .bindPopup("You are here").openPopup();

        map.setView([lat, lon], 14);

        // Find nearby hospitals
        let hospitals = await findHospitals(lat, lon);

        hospitals.forEach(hospital => {
            let hospLat = hospital.lat;
            let hospLon = hospital.lon;
            let name = hospital.display_name;

            L.marker([hospLat, hospLon]).addTo(map)
                .bindPopup(`<b>${name}</b>`);
        });

        document.getElementById("status").innerText = "Nearby hospitals loaded!";
    }, () => {
        document.getElementById("status").innerText = "Location access denied.";
    });
} else {
    document.getElementById("status").innerText = "Geolocation is not supported by this browser.";
}

// Fetch hospitals from OpenStreetMap's Nominatim API
async function findHospitals(lat, lon) {
    let response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=hospital&bounded=1&limit=10&viewbox=${lon-0.1},${lat-0.1},${lon+0.1},${lat+0.1}`
    );
    let data = await response.json();
    return data;
}
