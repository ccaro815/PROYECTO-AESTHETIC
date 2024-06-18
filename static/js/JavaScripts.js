let swiper = new Swiper('.mySwiper', {
    sliderPerview: 1,
    spaceBetween: 30,
    grabCursor: true,
    loop:true,
    breakpoints: {
        991: {
            sliderPerview:4
        }
    }
});