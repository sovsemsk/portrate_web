const pioRateTemplate = `{% include "widget/_rate.html" %}`
const pioRateBody = document.querySelector("body");
const pioRateNode = new DOMParser().parseFromString(pioRateTemplate, "text/html").body.firstElementChild;
const pioRateWidgetScriptTag = document.querySelector("#PIO_RATE_WIDGET_SCRIPT");
pioRateBody.appendChild(pioRateNode);

//const starGray = document.getElementById("STAR_GRAY");
//const starYellow = document.getElementById("STAR_YELLOW");
//starGray.onload = () => starYellow.onload = () => { alert("Hello") };