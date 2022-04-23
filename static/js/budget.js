const form = document.getElementById("form");
let disappeared = false;
function modify(e, id) {
  console.log(id);

  disappeared = false;
  form.style.display = "block";
  form.classList.toggle("active");
}
function cancel() {
  form.classList.toggle("inactive");
  disappeared = true;
}
form.onanimationend = () => {
  if (disappeared) {
    form.style.display = "none";
    form.classList = "";
  }
};
