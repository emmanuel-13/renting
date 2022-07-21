// IMAGE SLIDER FOR LOGINS & LISTING
let swiper = new Swiper(".loginRightSwiper", {
  loop: true,
  autoplay: {
    delay: 2500,
    disableOnInteraction: true,
  },
  // Disable preloading of all images
  preloadImages: false,
  // Enable lazy loading
  lazy: true,
});

// LAZYLOAD IMAGES ON LOAD
const lazyImages = document.querySelectorAll(".swiper-lazy");
// const imagePreloader = document.querySelector(".swiper-lazy-preloader");

lazyImages.forEach((lazyImage) => {
  lazyImage.addEventListener("load", () => {
    lazyImage.classList.remove("swiper-lazy");
    // imagePreloader.classList.remove(".swiper-lazy-preloader");
  });
});
