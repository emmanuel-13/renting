/*=============== FULLWIDTH GRID || 3 COLUMN GRID SWITCH LAYOUT ===============*/

let listFull = document.querySelector(".list-full");
let listHalf = document.querySelector(".list-half");
let listContainer = document.querySelector(".listing__container");

listHalf.addEventListener("click", () => {
  listContainer.classList.add("active");
  listHalf.classList.add("active");
  listFull.classList.remove("active");
});

listFull.addEventListener("click", () => {
  listContainer.classList.remove("active");
  listHalf.classList.remove("active");
  listFull.classList.add("active");
});

/*=============== ACTIVATE 1 X 1 GRID ON SCREEN <=600 @resize & reload ===============*/
const BrowserResize = () => {
  if (window.innerWidth <= 600) {
    listHalf.classList.add("active");
    listContainer.classList.add("active");
    listFull.style.display = "none";
  } else {
    listFull.style.display = "block";
    listHalf.classList.remove("active");
    listFull.classList.add("active");
    listContainer.classList.remove("active");
  }
};
window.addEventListener("resize", BrowserResize);
window.addEventListener("DOMContentLoaded", BrowserResize);

// let mixerProducts = mixitup(".listing__container", {
//   selectors: {
//     target: ".cards",
//   },
//   animation: {
//     duration: 300,
//   },
// });

// // Default Filter Products
// mixerProducts.filter("all");

/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById("nav-menu"),
  navToggle = document.getElementById("nav-toggle"),
  navTheme = document.getElementById("nav__theme"),
  toast = document.querySelector(".toast"),
  Message = document.querySelector(".message-text"),
  progress = document.querySelector(".progress"),
  navClose = document.getElementById("nav-close");

/*===== MENU SHOW ======*/
// validate if constant exist
if (navToggle) {
  navToggle.addEventListener("click", () => {
    navMenu.classList.add("show__menu");
  });
}

/*===== MENU HIDDEN ======*/
if (navClose) {
  navClose.addEventListener("click", () => {
    navMenu.classList.remove("show__menu");
  });
}

if (navTheme) {
  navTheme.addEventListener("click", () => {
    navMenu.classList.remove("show__menu");
    if (navTheme.childNodes[1].classList.contains("bx-sun")) {
      let timer1, timer2;
      Message.textContent = "Dark Mode Activated";
      toast.classList.add("active");
      progress.classList.add("active");

      timer1 = setTimeout(() => {
        toast.classList.remove("active");
      }, 2000); //1s = 1000 milliseconds

      timer2 = setTimeout(() => {
        progress.classList.remove("active");
      }, 2300);
    } else {
      let timer1, timer2;
      Message.textContent = "Light Mode Activated";
      toast.classList.add("active");
      progress.classList.add("active");

      timer1 = setTimeout(() => {
        toast.classList.remove("active");
      }, 2000); //1s = 1000 milliseconds

      timer2 = setTimeout(() => {
        progress.classList.remove("active");
      }, 2300);
    }
  });
}

/*=============== REMOVE MOBILE MENU ===============*/
const navLink = document.querySelectorAll(".nav__link");

function linkAction() {
  const navMenu = document.getElementById("nav-menu");
  //when we click on each nav__link, we remove the show__menu class
  navMenu.classList.remove("show__menu");
}

navLink.forEach((n) => {
  n.addEventListener("click", linkAction);
});
