let slides = document.querySelectorAll('.slide');
let index = 0;

function showslide(){
    slides.forEach(slides=> slides.classList.remove('activate'));
    slides[index].classList.add('active')
    index++;

    if (index >= slides.length){
        index = 0;
    }
}

setInterval(showslide, 3000);