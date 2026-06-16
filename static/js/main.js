const drawer = document.querySelector("[data-cart-drawer]");
const openButtons = document.querySelectorAll("[data-cart-open]");
const closeButtons = document.querySelectorAll("[data-cart-close]");

function openCart() {
  if (!drawer) return;
  drawer.classList.add("is-open");
  drawer.setAttribute("aria-hidden", "false");
  document.body.classList.add("cart-open");
}

function closeCart() {
  if (!drawer) return;
  drawer.classList.remove("is-open");
  drawer.setAttribute("aria-hidden", "true");
  document.body.classList.remove("cart-open");
}

openButtons.forEach((button) => button.addEventListener("click", openCart));
closeButtons.forEach((button) => button.addEventListener("click", closeCart));

document.querySelectorAll("[data-zoom]").forEach((zoomArea) => {
  zoomArea.addEventListener("click", () => zoomArea.classList.toggle("is-zoomed"));
});

document.querySelectorAll("[data-thumb]").forEach((thumb) => {
  thumb.addEventListener("click", () => {
    const main = document.querySelector("[data-zoom] img");
    if (!main) return;
    main.src = thumb.src;
    main.alt = thumb.alt;
  });
});

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeCart();
});
