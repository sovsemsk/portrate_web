const template = `{% include 'widget/_rate.html' %}`
const body = document.querySelector("body");
const node = new DOMParser().parseFromString(template, "text/html").body.firstElementChild;
body.appendChild(node);
//const starGray = document.getElementById('STAR_GRAY');
//const starYellow = document.getElementById('STAR_YELLOW');
//starGray.onload = () => starYellow.onload = () => { alert("Hello") };