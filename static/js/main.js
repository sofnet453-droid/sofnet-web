let index = 0;
const slides = document.querySelectorAll(".slide");

setInterval(() => {
  slides[index].classList.remove("active");
  index = (index + 1) % slides.length;
  slides[index].classList.add("active");
}, 3000);


function updateClock() {
  const now = new Date();
  document.getElementById("clock").innerText =
    now.toLocaleDateString() + " " + now.toLocaleTimeString();
}
setInterval(updateClock, 1000);
updateClock();

function toggleTheme() {
  document.body.classList.toggle("dark");
}
