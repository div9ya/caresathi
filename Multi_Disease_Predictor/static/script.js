var swiper = new Swiper(".mySwiper", {
	slidesPerView: 2,
	centeredSlides: true,
	spaceBetween: 30,
	loop: true,
	pagination: {
		el: ".swiper-pagination",
		type: "fraction",
	},
	navigation: {
		nextEl: ".swiper-button-next",
		prevEl: ".swiper-button-prev",
	},
});
document.getElementById("sos-system").addEventListener("click", function() {
	window.location.href = "/user";  
	 } );
document.getElementById("chat_bot").addEventListener("click", function() {
	window.location.href = "/chat_bot";  
	 } );
document.getElementById("qrcode").addEventListener("click", function() {
	window.location.href = "/qrcode";  
	 } );