

function initrequest(){
	const xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/initscanner");
	xhr.send();

};


function Yplus(){
	const xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/incY");
	xhr.send();

};

function Yminus(){
	const xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/decY");
	xhr.send();

};
function PlateUp(){
	const xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/decZ");
	xhr.send();

};
function PlateDown(){
	const xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/incZ");
	xhr.send();

};
// Theresa's function 
function Process(){
	const xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/processing");
	xhr.send()
};
// end of Theresa's function

//added af Z:
function Increase(){
	const xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/increase");
	xhr.send()
};

function Decrease(){
	const xhr = new XMLHttpRequest();
	xhr.open("GET", "http://127.0.0.1:5000/processing");
	xhr.send()
};
function ulshow() {
    document.getElementById('im1').style.display = 'block'; // Display the ultrasound image
    document.getElementById('im2').style.display = 'none';  // Hide the webcam feed
    document.getElementById('li1').classList.add('is-active');  // Make Ultrasound tab active
    document.getElementById('li2').classList.remove('is-active'); // Deactivate Overview Video tab
}

function feedshow() {
    document.getElementById('im1').style.display = 'none';  // Hide the ultrasound image
    document.getElementById('im2').style.display = 'block'; // Display the webcam feed
    document.getElementById('li1').classList.remove('is-active'); // Deactivate Ultrasound tab
    document.getElementById('li2').classList.add('is-active');  // Make Overview Video tab active
}
