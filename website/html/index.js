let num_heads = 0;
let num_tails = 0;
let num_slide = 1;
window.addEventListener("DOMContentLoaded", domLoaded);

function domLoaded() {
	if (document.getElementsByClassName("button")[0]) {
		document.getElementsByClassName("button")[0].addEventListener("click", coinFlip);
		updateCoinInfo();
	}

	if (document.getElementById("add")) {
		document.getElementById("add").addEventListener("click", newPara);
	}
	
	if (document.getElementById("slideImg")) {
		var timer = setInterval(slideShow, 30000);
	}
}

function updateCoinInfo() {
	document.getElementById("num_heads").innerHTML = num_heads;
	document.getElementById("num_tails").innerHTML = num_tails;
}

function coinFlip() {
	rand = Math.floor(Math.random() * 2) + 1;
	console.log(rand);
	document.getElementById("coinImg").src = "Media/coin" + rand + ".png";
	rand == 1 ? num_heads++ : num_tails++;
	updateCoinInfo();
}

function newPara() {
	console.log("click");
	userPara = document.createElement("p");
	userPara.innerHTML = document.getElementById("paragraph").value;
	console.log("textt: "+userPara.innerHTML);
	document.getElementById("essay_body").append(userPara);
	document.getElementById("paragraph").value = '';
}

function slideShow() {
	num_slide == 5 ? num_slide = 1 : num_slide++;
	document.getElementById("slideImg").src = "Media/Slideshow/Image" + num_slide + ".jpg"
}
