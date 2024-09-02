let swiper = new Swiper(".mySwiper", {
  slidesPerView: 3,
  spaceBetween: 30,
  grabCursor: true,
  loop: true,
  autoplay: {
    delay: 1800,
    disableOnInteraction: false,
  },
  breakpoints: {
    991: {
      slidesPerView: 3,
    },
    768: {
      slidesPerView: 2,
    },
    576: {
      slidesPerView: 1,
    },
  },
});
