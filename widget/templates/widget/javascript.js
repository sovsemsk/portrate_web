body = document.querySelector("body")
const rating_widget = document.createElement("div")
const rating_widget_rating = document.createElement("div")
const rating_widget_stars = document.createElement("div")
const rating_widget_count = document.createElement("div")
const rating_widget_about = document.createElement("div")

const reviews_widget = document.createElement("div")
const theme = "{{theme}}"
const position = "{{position}}"
const rating = "{{company.portrate_rate}}"

rating_widget.style.position = "absolute"
rating_widget.style.zIndex = "9999"
rating_widget.style.display = "flex"
rating_widget.style.borderRadius = "10px"
rating_widget.style.width = "270px"
rating_widget.style.height = "80px"
rating_widget.style.boxShadow = "0 0 10px 0 rgba(0,0,0,0.20)"

rating_widget_rating.style.padding = "10px 10px 0 25px"
rating_widget_rating.style.fontFamily = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
rating_widget_rating.style.fontSize = "42px"
rating_widget_rating.style.fontWeight = "bold"

rating_widget_stars.style.padding = "18px 0 0 0"
rating_widget_stars.style.fontFamily = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
rating_widget_stars.style.fontSize = "16px"
rating_widget_stars.style.fontWeight = "bold"

rating_widget_count.style.fontSize = "14px"
rating_widget_count.style.fontFamily = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
rating_widget_count.style.fontWeight = "normal"

rating_widget_about.style.fontSize = "12px"
rating_widget_about.style.fontFamily = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
rating_widget_about.style.fontWeight = "normal"


if(theme=="light"){
    rating_widget.style.background="#F8F8F8"
}else{
    rating_widget.style.background="#2B2B2B"
}

if(position == "lb"){
    rating_widget.style.left = "20px"
    rating_widget.style.bottom = "20px"
}else if(position == "lt"){
    rating_widget.style.left = "20px"
    rating_widget.style.top = "20px"
}else if(position == "rt"){
    rating_widget.style.right = "20px"
    rating_widget.style.top = "20px"
}else if(position == "rb"){
    rating_widget.style.right = "20px"
    rating_widget.style.bottom = "20px"
}


rating_widget_rating.innerHTML = rating
rating_widget_stars.innerHTML = "★★★★★"
rating_widget_count.innerHTML = "20432 отзывов"

rating_widget_stars.appendChild(rating_widget_count)
rating_widget.appendChild(rating_widget_rating)
rating_widget.appendChild(rating_widget_stars)

body.appendChild(rating_widget)
