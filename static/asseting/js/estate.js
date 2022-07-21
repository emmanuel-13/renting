/*=============== SHOW MENU ===============*/
const sidebar = document.getElementById("sidebar"),
  SidebarToggle = document.getElementById("sidebar-toggle"),
  SidebarClose = document.getElementById("close");

/*===== MENU SHOW =====*/
/* Validate if constant exists */
if (SidebarToggle) {
  SidebarToggle.addEventListener("click", () => {
    sidebar.classList.toggle("show-menu");
  });
}

/*===== MENU HIDDEN =====*/
/* Validate if constant exists */
if (SidebarClose) {
  SidebarClose.addEventListener("click", () => {
    sidebar.classList.remove("show-menu");
  });
}

/*=============== REMOVE MENU MOBILE ===============*/
const SidebarLink = document.querySelectorAll(".sidebar__link");

function linkAction() {
  const sidebar = document.getElementById("sidebar");
  // When we click on each nav__link, we remove the show-menu class
  sidebar.classList.remove("show-menu");
}
SidebarLink.forEach((n) => n.addEventListener("click", linkAction));

document.body.removeEventListener("click", linkAction);
