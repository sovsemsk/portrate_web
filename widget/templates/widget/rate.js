const template = `{% include 'widget/_rate.html' %}`
const body = document.querySelector("body");
const node = new DOMParser().parseFromString(template, "text/html").body.firstElementChild;
body.appendChild(node);