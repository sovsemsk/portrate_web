__519f87__=(__b791f1__,__2bd7b91__)=>{__b791f1__.parentNode.insertBefore(__2bd7b91__,__b791f1__.nextSibling);}
__d91262__=document.querySelector("script[data-{{api_secret}}]");                                                                           // Script
__5dbd30__=new DOMParser().parseFromString(`{% include "widget/_reviews_slider_light.html" %}`,"text/html").body.firstElementChild;
__519f87__(__d91262__,__5dbd30__);
__4913fc__=document.querySelector("div[data-4913fc]");                                                                                      // Reviews
__fd94a8__=document.querySelector("div[data-fd94a8]");                                                                                      // First review
__32a461__=document.querySelector("button[data-32a461]");                                                                                   // Left button
__cd7b94__=document.querySelector("button[data-cd7b94]");                                                                                   // Right button
__18e6c1__= () => {__4913fc__.scrollLeft -= __fd94a8__.clientWidth;}                                                                        // Left button click
__459b69__= () => {__4913fc__.scrollLeft += __fd94a8__.clientWidth;}                                                                        // Right button click