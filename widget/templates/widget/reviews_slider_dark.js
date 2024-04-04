__519f87__=(__b791f1__,__2bd7b91__)=>{__b791f1__.parentNode.insertBefore(__2bd7b91__,__b791f1__.nextSibling);}
// Script
__d91262__=document.querySelector("script[data-{{api_secret}}]");
// Add node
__5dbd30__=new DOMParser().parseFromString(`{% include "widget/_reviews_slider_dark.html" %}`,"text/html").body.firstElementChild;
__519f87__(__d91262__,__5dbd30__);
// Reviews
__4913fc__=document.querySelector("div[data-4913fc]");
// Review first
__fd94a8__=document.querySelector("div[data-fd94a8]");
// Reviews texts
__b93be1__=document.querySelectorAll("div[data-20d8b7]");
// Left button
__32a461__=document.querySelector("button[data-32a461]");
// Right button
__cd7b94__=document.querySelector("button[data-cd7b94]");
// Left button click
__18e6c1__= () => {__4913fc__.scrollLeft -= __fd94a8__.clientWidth;}
// Right button click
__459b69__= () => {__4913fc__.scrollLeft += __fd94a8__.clientWidth;}
// Text scroll
__a4738e__= (__a5c5c7__) => {__a5c5c7__.scrollTop > 5 ? __a5c5c7__.previousElementSibling.style.display = "block" : __a5c5c7__.previousElementSibling.style.display = "none"; (__a5c5c7__.scrollTop + 275) > (__a5c5c7__.scrollHeight - 5) ? __a5c5c7__.nextElementSibling.style.display = "none" : __a5c5c7__.nextElementSibling.style.display = "block";};
// Show bottom text fade if need
__b93be1__.forEach(__a068fe__ => {if(__a068fe__.scrollHeight > 250){__a068fe__.style.paddingBottom = "25px";__a068fe__.nextElementSibling.style.display = "block";}});