function openLightbox(src, alt){const box=document.getElementById("lightbox");if(!box)return;document.getElementById("lightbox-img").src=src;document.getElementById("lightbox-img").alt=alt||"";box.classList.add("show");}
function closeLightbox(){const box=document.getElementById("lightbox");if(box)box.classList.remove("show");}
document.addEventListener("keydown",e=>{if(e.key==="Escape")closeLightbox();});
