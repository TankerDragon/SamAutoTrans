const form = document.getElementById("form");
let disappeared = false;
let current_driver;
function modify(e, id) {
  current_driver = id;
  // var this_row = e.parentElement.parentElement;
  // var rows = document.getElementById("tbody").children;
  // console.log(Array.prototype.indexOf.call(rows, this_row));
  document.getElementById(
    "full-name"
  ).innerHTML = `<h3>${e.parentElement.parentElement.children[0].innerText} ${e.parentElement.parentElement.children[1].innerText}</h3>`;
  console.log(e.parentElement.parentElement.children[0].innerText);

  disappeared = false;
  form.style.display = "block";
  form.classList.toggle("active");
}
function archive(id) {
  location.href = "/budget/archive/" + id;
}
function submit() {
  fetch(current_driver, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRF(),
    },
    body: JSON.stringify({
      amount: parseFloat(document.getElementById("input-amount").value),
      budget_type: document.getElementById("budget-type").value,
      bol_number: document.getElementById("bol-number").value,
      pcs_number: document.getElementById("pcs-number").value,
    }),
  })
    .catch((error) => {
      console.log("ERROR", error);
      window.alert(error);
    })

    .then((data) => {
      console.log("DATA_OK?: ", data);
      if (data.status != 200) {
        window.alert("Uncompleted Submit!!!");
      } else {
        document.getElementById("input-amount").value = "";
        document.getElementById("budget-type").value = "D";
        document.getElementById("bol-number").value = "";
        document.getElementById("pcs-number").value = "";
      }
      location.reload();
      cancel();
    });
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
function getCSRF() {
  arr = document.getElementById("csrf").innerHTML.split("value");
  arr = arr[1].split('"');
  return arr[1];
}
