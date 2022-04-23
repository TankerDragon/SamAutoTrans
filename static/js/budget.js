const form = document.getElementById("form");
let disappeared = false;
function modify(e, id) {
  // var this_row = e.parentElement.parentElement;
  // var rows = document.getElementById("tbody").children;
  // console.log(Array.prototype.indexOf.call(rows, this_row));
  document.getElementById("full-name").innerHTML = `<h3>${e.parentElement.parentElement.children[0].innerText} ${e.parentElement.parentElement.children[1].innerText}</h3>`;
  console.log(e.parentElement.parentElement.children[0].innerText);

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
