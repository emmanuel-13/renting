/*=============== HIDE CALENDLY ON PAGE LOAD ===============*/
window.addEventListener("load", (e) => {
  const calendlyWidget = document.querySelector(".calendly-badge-widget");
  calendlyWidget.classList.add("calendly-badge-hide");
});

/*=============== SHOW MODAL ===============*/
const showModal = (openButton, modalContent) => {
  const openBtn = document.getElementById(openButton),
    modalContainer = document.getElementById(modalContent);

  if (openBtn && modalContainer) {
    openBtn.addEventListener("click", () => {
      const calendlyWidget = document.querySelector(".calendly-badge-widget");
      modalContainer.classList.add("show-modal");
      calendlyWidget.classList.remove("calendly-badge-hide");
    });
  }
};
showModal("open-modal", "modal-container");

/*=============== CLOSE MODAL ===============*/
const closeBtn = document.querySelector(".close-modal");
function closeModal() {
  const modalContainer = document.getElementById("modal-container");
  const calendlyWidget = document.querySelector(".calendly-badge-widget");
  modalContainer.classList.remove("show-modal");
  calendlyWidget.classList.add("calendly-badge-hide");
}
closeBtn.addEventListener("click", closeModal);

/*=============== COPY TEXT ===============*/

const copyTextareaBtn = document.querySelector(".textareacopybtn");
const instructionalText = document.querySelector(".instructional-text");

copyTextareaBtn.addEventListener("click", function (event) {
  let copyTextarea = document.querySelector(".copytextarea");
  copyTextarea.focus();
  copyTextarea.select();
  instructionalText.textContent =
    "Copied! Now you can schedule a meeting by clicking the button ☝️.";
  instructionalText.style.color = "green";
  instructionalText.style.backgroundColor = `rgba(106, 186, 80, 0.10)`;

  try {
    const successful = document.execCommand("copy");
    const msg = successful ? "successful" : "unsuccessful";
    Message.textContent = `Copy ${msg}`;
    toast.classList.add("active");
    progress.classList.add("active");

    timer1 = setTimeout(() => {
      toast.classList.remove("active");
    }, 2000); //1s = 1000 milliseconds

    timer2 = setTimeout(() => {
      progress.classList.remove("active");
    }, 2300);
  } catch (err) {
    Message.textContent = `Oops, unable to copy`;
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
