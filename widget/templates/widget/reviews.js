const pioReviewsInsertAfter = (referenceNode, newNode) => {referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling)}
const pioReviewsTemplate = `{% include "widget/_reviews.html" %}`;
const pioReviewsBody = document.querySelector("body");
const pioReviewsNode = new DOMParser().parseFromString(pioReviewsTemplate, "text/html").body.firstElementChild;
const pioReviewsWidgetScriptTag = document.querySelector("#PIO_REVIEWS_WIDGET_SCRIPT");
pioReviewsInsertAfter(pioReviewsWidgetScriptTag, pioReviewsNode);
const pioReviewsWidgetContainer = document.querySelector("#PIO_REVIEWS_WIDGET_CONTAINER");
const pioReviewsWidgetContainerWidth = pioReviewsWidgetContainer.offsetWidth;
const pioReviewsWidgetCards = document.querySelectorAll(".PIO_REVIEWS_WIDGET_CARD");
if(pioReviewsWidgetContainerWidth < 480){pioReviewsWidgetCards.forEach(element => {element.classList.add("PIO_REVIEWS_WIDGET_CARD_1")})}
if(pioReviewsWidgetContainerWidth > 481 && pioReviewsWidgetContainerWidth < 768){pioReviewsWidgetCards.forEach(element => {element.classList.add("PIO_REVIEWS_WIDGET_CARD_2")})}
if(pioReviewsWidgetContainerWidth > 769 && pioReviewsWidgetContainerWidth < 1024){pioReviewsWidgetCards.forEach(element => {element.classList.add("PIO_REVIEWS_WIDGET_CARD_3")})}
if(pioReviewsWidgetContainerWidth > 1025 && pioReviewsWidgetContainerWidth < 1200){pioReviewsWidgetCards.forEach(element => {element.classList.add("PIO_REVIEWS_WIDGET_CARD_4")})}
if(pioReviewsWidgetContainerWidth > 1200){pioReviewsWidgetCards.forEach(element => {element.classList.add("PIO_REVIEWS_WIDGET_CARD_5")})}