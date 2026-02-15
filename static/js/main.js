/* =====================================================
   SOFNET MAIN JS UNIVERSAL
   Funciona en TODAS las páginas
===================================================== */


/* ================= CARRUSEL ================= */
const slides = document.querySelectorAll(".slide");

if (slides.length > 0) {
    let index = 0;

    setInterval(() => {
        slides[index].classList.remove("active");
        index = (index + 1) % slides.length;
        slides[index].classList.add("active");
    }, 3000);
}


/* ================= RELOJ FORMATO 24 HORAS ================= */
const clock = document.getElementById("clock");

if (clock) {
    function updateClock() {
        const now = new Date();

        const hours = String(now.getHours()).padStart(2, "0");
        const minutes = String(now.getMinutes()).padStart(2, "0");
        const seconds = String(now.getSeconds()).padStart(2, "0");

        const date = now.toLocaleDateString("es-ES");

        clock.innerText = `${date}  ${hours}:${minutes}:${seconds}`;
    }

    setInterval(updateClock, 1000);
    updateClock();
}


/* ================= ACCESIBILIDAD TEXTO ================= */
let size = 16;

function increaseText() {
    size += 2;
    document.body.style.fontSize = size + "px";
}

function decreaseText() {
    size = Math.max(12, size - 2);
    document.body.style.fontSize = size + "px";
}


/* ================= LECTOR DE VOZ ================= */
function readPage() {
    if ("speechSynthesis" in window) {
        const text = document.body.innerText;
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = "es-ES";

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(speech);
    } else {
        alert("Tu navegador no soporta lectura por voz");
    }
}


/* ================= MENU HAMBURGUESA GLOBAL ================= */
const toggle = document.getElementById("menu-toggle");
const nav = document.getElementById("nav");

if (toggle && nav) {
    toggle.addEventListener("click", () => {
        nav.classList.toggle("active");

        if (nav.classList.contains("active")) {
            toggle.innerHTML = '<i class="fa-solid fa-xmark"></i>';
        } else {
            toggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
        }
    });
}


/* ================= MODO OSCURO GLOBAL ================= */
const darkToggle = document.getElementById("dark-toggle");

if (darkToggle) {

    if (localStorage.getItem("modo") === "oscuro") {
        document.body.classList.add("dark-mode");
        darkToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
    }

    darkToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            darkToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
            localStorage.setItem("modo", "oscuro");
        } else {
            darkToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
            localStorage.setItem("modo", "claro");
        }
    });
}


/* ================= ANIMACIÓN SUAVE AL HACER SCROLL ================= */
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        }
    });
});

document.querySelectorAll(".animate").forEach((el) => {
    observer.observe(el);
});
