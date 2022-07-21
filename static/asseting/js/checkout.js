const selectButton = document.getElementById("select-button");
const selectDropdown = document.getElementById("select-dropdown");
const selectLabel = document.getElementById("select-label");
const options = document.querySelectorAll(".process__form-option");

selectButton.addEventListener("click", (e) => {
  e.preventDefault();
  toggleHidden();
  if (e.target.id === "select-label") {
    selectDropdown.classList.remove("dropdown--hidden");
  }
});

function toggleHidden() {
  selectDropdown.classList.toggle("dropdown--hidden");
}

// run a function when the user clicks on the body
document.addEventListener("click", (e) => {
  // if the dropdown is visible
  if (e.target.id !== "select-button" && e.target.id !== "select-label") {
    // hide the dropdown
    selectDropdown.classList.add("dropdown--hidden");
  } else if (e.target.id == "select-button" && e.target.id == "select-label") {
    selectDropdown.classList.remove("dropdown--hidden");
  } else {
    return;
  }
});

options.forEach(function (option) {
  option.addEventListener("click", function (e) {
    setSelectTitle(e);
  });
});

function setSelectTitle(e) {
  const labelElement = document.querySelector(
    `label[for="${e.target.id}"]`
  ).innerText;
  selectLabel.innerText = labelElement;
  toggleHidden();
}

const switches = document.querySelectorAll(".process__form--radio-input");

switches.forEach(function (verify) {
  verify.addEventListener("click", function (e) {
    if (e.target.id == "bvn" || e.target.id == "nin") {
      setTextContent(e);
    }
  });
});

function setTextContent(e) {
  const nextInput = document.getElementById("verification");
  const labelElementVerify = document.querySelector(
    `label[for="${e.target.id}"]`
  ).innerText;
  nextInput.innerText = `enter ${labelElementVerify} number`;
  //  selectLabel.innerText = labelElement;
  //  toggleHidden();
}
