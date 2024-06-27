let swiper = new Swiper(".mySwiper", {
  slidesPerView: 3,  // Mostrar 3 imágenes a la vez
  spaceBetween: 30,  // Espacio entre las imágenes
  grabCursor: true,
  loop: true,
  breakpoints: {
    991: {
      slidesPerView: 3,  // Mostrar 3 imágenes a la vez en pantallas grandes
    },
    768: {
      slidesPerView: 2,  // Mostrar 2 imágenes a la vez en pantallas medianas
    },
    576: {
      slidesPerView: 1,  // Mostrar 1 imagen a la vez en pantallas pequeñas
    },
  },
});


