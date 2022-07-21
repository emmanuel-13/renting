/*=============== CHANGE BACKGROUND HEADER ===============*/
function scrollHeader() {
  const navbar = document.getElementById("navbar");
  // When the scroll is greater than 50 viewport height, add the scroll-navbar class to the header tag
  if (this.scrollY >= 50) navbar.classList.add("scroll-navbar");
  else navbar.classList.remove("scroll-navbar");
}
window.addEventListener("scroll", scrollHeader);

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

/*=============== DARK LIGHT THEME ===============*/
const themeButton = document.getElementById("theme-button");
const darkTheme = "dark-theme";
const iconTheme = "bx-sun";

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem("selected-theme");
const selectedIcon = localStorage.getItem("selected-icon");

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () =>
  document.body.classList.contains(darkTheme) ? "dark" : "light";
const getCurrentIcon = () =>
  themeButton.classList.contains(iconTheme) ? "bx bx-moon" : "bx bx-sun";

// We validate if the user previously chose a topic
if (selectedTheme) {
  // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
  document.body.classList[selectedTheme === "dark" ? "add" : "remove"](
    darkTheme
  );
  themeButton.classList[selectedIcon === "bx bx-moon" ? "add" : "remove"](
    iconTheme
  );
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener("click", () => {
  // Add or remove the dark / icon theme
  document.body.classList.toggle(darkTheme);
  themeButton.classList.toggle(iconTheme);
  // We save the theme and the current icon that the user chose
  localStorage.setItem("selected-theme", getCurrentTheme());
  localStorage.setItem("selected-icon", getCurrentIcon());
});
