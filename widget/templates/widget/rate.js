const pioRateTemplate = `{% include "widget/_rate.html" %}`
const pioRateBody = document.querySelector("body");
const pioRateNode = new DOMParser().parseFromString(pioRateTemplate, "text/html").body.firstElementChild;
const pioRateWidgetScriptTag = document.querySelector("#PIO_RATE_WIDGET_SCRIPT");
pioRateBody.appendChild(pioRateNode);
// starGray.onload = () => starYellow.onload = () => {};