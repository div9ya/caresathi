document.getElementById('qrForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const regd_no = document.getElementById('regd_no').value;
    fetch(`/qr/${regd_no}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('QR code not found');
            }
            return response.blob();
        })
        .then(imageBlob => {
            const imageObjectURL = URL.createObjectURL(imageBlob);
            document.getElementById('qrCodeDisplay').innerHTML = `<img src="${imageObjectURL}" alt="QR Code">`;
        })
        .catch(error => {
            alert(error.message);
        });
});