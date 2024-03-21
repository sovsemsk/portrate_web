const d = document;

const insertAfter = (referenceNode, newNode) => {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

const truncateString = (string, length) => {
  if(string.length > length){
    return string.slice(0, length) + "...";
  }else{
    return string;
  }
}


// Get script element
const scriptEl = d.querySelector("script[data-pio-reviews-widget='true'");

/*
Create new css classes
*/
d.head.insertAdjacentHTML("beforeend", `
<style>
    .pioReviewsWidget{
        background:white;
        border: 2px solid rgba(0, 0, 0, 0.1);
        border-radius:20px;
        font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
        padding:20px;
    }
    .pioReviewsWidget-reviews{
        display:flex;
        overflow-x:scroll;
        padding-bottom:20px;
        scroll-snap-type: x mandatory;
        width: 100%;
    }

    .pioReviewsWidget-reviews::-webkit-scrollbar{
        background-color:rgba(0, 0, 0, 0.1);
        height:10px;
        border-radius:5px;
    }
    .pioReviewsWidget-reviews::-webkit-scrollbar-thumb{
        border-radius:5px;
        background-color:rgba(0, 0, 0, 0.1);
        background-clip: content-box;
    }

    .pioReviewsWidget-reviews-item{
        scroll-snap-align:start;
    }

    .pioReviewsWidget-reviews-item-name{
        font-size: small;
        font-weight: bold;
    }

    .pioReviewsWidget-reviews-item-date{
        color: rgba(0,0,0,0.5);
        font-size: small;
        padding-bottom: 5px;
    }

    .pioReviewsWidget-reviews-item-stars{
        padding-bottom: 5px;
    }

    .pioReviewsWidget-reviews-item__1{flex:1 0 100%}
    .pioReviewsWidget-reviews-item__2{flex:1 0 calc(100% / 2)}
    .pioReviewsWidget-reviews-item__3{flex:1 0 calc(100% / 3)}
    .pioReviewsWidget-reviews-item__4{flex:1 0 calc(100% / 4)}
    .pioReviewsWidget-reviews-item__5{flex:1 0 calc(100% / 5)}

    .pioReviewsWidget-reviews-item-text{
        padding-right: 30px;
        line-height: 1.4;
        text-overflow: ellipsis;
    }

</style>
`)

/*
Create new elements
*/

// Create container
const containerEl = d.createElement("div")
containerEl.classList.add("pioReviewsWidget");
insertAfter(scriptEl, containerEl);
const containerWidth = containerEl.offsetWidth;


// Create reviews
const reviewsEl = d.createElement("div");
reviewsEl.classList.add("pioReviewsWidget-reviews");
containerEl.appendChild(reviewsEl);

// Create review
fetch('http://127.0.0.1:8000/widget/067f2lIy/reviews.json').then(response => response.json()).then(result => {
    response = result[0];

    response.reviews.forEach((item) => {
        const reviewEl = d.createElement("div");
        reviewEl.classList.add("pioReviewsWidget-reviews-item");
        reviewsEl.appendChild(reviewEl);

        if(containerWidth < 480){
            reviewEl.classList.add("pioReviewsWidget-reviews-item__1");
        }else if(containerWidth > 481 && containerWidth <= 768){
            reviewEl.classList.add("pioReviewsWidget-reviews-item__2");
        }else if(containerWidth > 769 && containerWidth  <= 1200){
            reviewEl.classList.add("pioReviewsWidget-reviews-item__3");
        }else if(containerWidth > 1201 && containerWidth  <= 1400){
            reviewEl.classList.add("pioReviewsWidget-reviews-item__4");
        }else if(containerWidth > 1401){
            reviewEl.classList.add("pioReviewsWidget-reviews-item__5");
        }


        const nameEl = d.createElement("div");
        nameEl.classList.add("pioReviewsWidget-reviews-item-name");
        nameEl.innerHTML = item.name;
        reviewEl.appendChild(nameEl);

        const dateEl = d.createElement("div");
        const date = new Date(item.created_at);


        dateEl.classList.add("pioReviewsWidget-reviews-item-date");
        dateEl.innerHTML = date.toLocaleDateString("ru-ru", {year: 'numeric', month: 'short', day: 'numeric' });
        reviewEl.appendChild(dateEl);

        const starsEl = d.createElement("img");
        starsEl.classList.add("pioReviewsWidget-reviews-item-stars");
        starsEl.src = `https://geo.portrate.io/static/images/stars/${item.stars}.0.svg`;
        reviewEl.appendChild(starsEl);

        const textEl = d.createElement("div");
        textEl.classList.add("pioReviewsWidget-reviews-item-text");
        textEl.innerHTML = truncateString(item.text, 200);
        reviewEl.appendChild(textEl);
    });
})


