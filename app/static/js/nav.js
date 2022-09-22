const btn = document.querySelector(".mobile-menu")
const menu = document.querySelector(".navmenu")

// Add Event Listener
btn.addEventListener("click", () =>{
menu.classList.toggle("hidden")
})