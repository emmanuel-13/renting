const showPassword = document.querySelector(".password-show");
const showConfirmPassword = document.querySelector(".confirm-password-show");
const passwordInput = document.querySelector(".password");
const ConfirmpasswordInput = document.querySelector(".confirm-password");

showPassword.addEventListener("click", () => {
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    showPassword.classList.replace("bxs-low-vision", "bxs-show");
  } else {
    passwordInput.type = "password";
    showPassword.classList.replace("bxs-show", "bxs-low-vision");
  }
});

showConfirmPassword.addEventListener("click", () => {
  if (ConfirmpasswordInput.type === "password") {
    ConfirmpasswordInput.type = "text";
    showConfirmPassword.classList.replace("bxs-low-vision", "bxs-show");
  } else {
    ConfirmpasswordInput.type = "password";
    showConfirmPassword.classList.replace("bxs-show", "bxs-low-vision");
  }
});
