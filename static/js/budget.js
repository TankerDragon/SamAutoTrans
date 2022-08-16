const form = document.getElementById("form");
let disappeared = false;
let current_driver;

//
function changeAmount() {
  let change =
    document.getElementById("original-rate").value != "" && document.getElementById("current-rate").value != ""
      ? parseFloat(document.getElementById("original-rate").value) - parseFloat(document.getElementById("current-rate").value)
      : 0;
  change = Math.round(change * 100) / 100;
  document.getElementById("input-amount").value = change;
  document.getElementById("input-amount").style.backgroundColor = change < 0 ? "#fcd9d9" : change > 0 ? "#e2fae1" : "white";
  document.getElementById("amount-message").style.color = change < 0 ? "red" : change > 0 ? "green" : "blue";
  document.getElementById("amount-message").innerText = change < 0 ? "overpaid" : change > 0 ? "saved" : "no change";
}
document.getElementById("original-rate").addEventListener("input", () => {
  changeAmount();
});
document.getElementById("current-rate").addEventListener("input", () => {
  changeAmount();
});

//
function exists(arr, e) {
  for (let i = 0; i < arr.length; i++) {
    if (e == arr[i]) {
      return true;
    }
  }
  return false;
}
function getChildIndex(node) {
  return Array.prototype.indexOf.call(node.parentElement.children, node);
}
function sort(e) {
  index = getChildIndex(e);

  //
  var parentRow = e.parentElement;
  for (let i = 0; i < parentRow.children.length; i++) {
    if (exists(parentRow.children[i].classList, "sorted") && parentRow.children[i] !== e) {
      parentRow.children[i].classList.toggle("sorted");
    }
  }

  e.classList.toggle("sorted");
  //
  var table, rows, switching, i, x, y, shouldSwitch;
  table = e.parentElement.parentElement.parentElement;
  switching = true;
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < rows.length - 1; i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[index];
      y = rows[i + 1].getElementsByTagName("TD")[index];
      // Check if the two rows should switch place:
      if (exists(e.classList, "sorted")) {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      } else {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}
function getBetweenDates() {
  var input1 = document.getElementById("date1");
  var input2 = document.getElementById("date2");
  var user = document.getElementById("userInList");

  fetch("between-dates/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRF(),
    },
    body: JSON.stringify({
      start_date: input1.value,
      end_date: input2.value,
      user: user.value,
    }),
  })
    .catch((error) => {
      window.alert(error);
    })
    .then((res) => res.json())
    .then((data) => {
      console.log("data***");
      console.log(data);
      document.getElementById("message").innerText = data.message;
      document.getElementById("d_total").innerText = data.D;
      document.getElementById("l_total").innerText = data.L;
      document.getElementById("r_total").innerText = data.R;
      document.getElementById("s_total").innerText = data.S;
      document.getElementById("total").innerText = data.T;
      //
      var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        title: {
          text: data.message,
          horizontalAlign: "center",
        },
        data: [
          {
            theme: "dark2",
            type: "doughnut",
            startAngle: 60,
            innerRadius: 60,
            indexLabelFontSize: 17,
            indexLabel: "{label} (#percent%)",
            toolTipContent: "<b>{label}:</b> {y} (#percent%)",
            dataPoints: [
              { y: data.D === 0 ? 0 : data.D, label: "Driver Budget" },
              { y: data.L === 0 ? 0 : data.L, label: "Lane Budget" },
              { y: data.R === 0 ? 0 : data.R, label: "Recovery Budget" },
              { y: data.S === 0 ? 0 : data.S, label: "Dirilis Budget" },
            ],
          },
        ],
      });
      chart.render();
    });
}
function getArchiveBetweenDates() {
  var start_date = document.getElementById("date1");
  var end_date = document.getElementById("date2");
  // filter_by =  ? window.location.href.split("/")[5] : "all";
  if (start_date.value && end_date.value) {
    if (document.getElementById("byDriver")) {
      location.href = `/budget/archive-between-dates/${window.location.href.split("/")[5]}/${start_date.value}&${end_date.value}`;
    } else {
      location.href = `/budget/archive-between-dates/${start_date.value}&${end_date.value}`;
    }
  } else {
    window.alert("Please complete dates input");
  }
}
function modify(e, id) {
  current_driver = id;
  // var this_row = e.parentElement.parentElement;
  // var rows = document.getElementById("tbody").children;
  // console.log(Array.prototype.indexOf.call(rows, this_row));
  //
  // document.getElementById("full-name").innerHTML = `<h3>${e.parentElement.parentElement.children[0].innerText} ${e.parentElement.parentElement.children[1].innerText}</h3>`;
  //
  // console.log(e.parentElement.parentElement.children[0].innerText);

  disappeared = false;
  form.style.display = "block";
  form.classList.toggle("active");
}
function reset(type) {
  var ENABLE_RESET = true;

  if (ENABLE_RESET) {
    message = "Are you sure to reset this budget? All budget of this type will be Zero";
    if (confirm(message) == true) {
      fetch("reset/" + type, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRF(),
        },
        body: JSON.stringify({}),
      })
        .catch((error) => {
          console.log("ERROR", error);
          window.alert(error);
        })
        .then(() => {
          location.href = "/budget";
        });
    }
  } else {
    window.alert("This action is temporarily unavailable");
  }
}
function archive(id) {
  location.href = "/budget/archive/" + id;
}
function driver_detail(id) {
  location.href = "/budget/driver-detail/" + id;
}
function user_detail(id) {
  location.href = "/budget/user-detail/" + id;
}
function deactivate_driver(id) {
  location.href = "/budget/deactivate-driver/" + id;
}
function activate_driver(id) {
  location.href = "/budget/activate-driver/" + id;
}
function edit_log(id) {
  location.href = "/budget/edit-log/" + id;
}
function prew_week() {
  arr = location.href.split("/");
  num = parseInt(arr[arr.length - 1]) + 1;
  location.href = "/budget/drivers-board/" + num;
}
function next_week() {
  arr = location.href.split("/");
  num = parseInt(arr[arr.length - 1]) - 1;
  if (num < 0) {
    window.alert("error: cant find next week!");
  } else {
    location.href = "/budget/drivers-board/" + num;
  }
}
function submit() {
  fetch(current_driver, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRF(),
    },
    body: JSON.stringify({
      original_rate: document.getElementById("original-rate").value,
      current_rate: document.getElementById("current-rate").value,
      total_miles: document.getElementById("total-miles").value,
      // amount: parseFloat(document.getElementById("input-amount").value),
      budget_type: document.getElementById("budget-type").value,
      bol_number: document.getElementById("bol-number").value,
      pcs_number: document.getElementById("pcs-number").value,
      note: document.getElementById("note").value,
    }),
  })
    .catch((error) => {
      console.log("ERROR", error);
      window.alert(error);
    })

    .then((data) => {
      console.log("DATA?: ", data);
      if (data.status != 200) {
        window.alert("Uncompleted Submit!!!");
      } else {
        document.getElementById("original-rate").value = "";
        document.getElementById("current-rate").value = "";
        // document.getElementById("input-amount").value = "";
        document.getElementById("budget-type").value = "D";
        document.getElementById("bol-number").value = "";
        document.getElementById("pcs-number").value = "";
        document.getElementById("note").value = "";
        //
        cancel();
        location.reload();
      }
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

function search() {
  // Declare variables
  var input, filter, table, tr, td1, td2, i, txtValue;
  var odd = true;
  input = document.getElementById("search-input");
  filter = input.value.toUpperCase();
  table = document.getElementById("tbody");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    tr[i].classList = "";
  }
  for (i = 0; i < tr.length; i++) {
    td1 = tr[i].getElementsByTagName("td")[0];
    td2 = tr[i].getElementsByTagName("td")[1];
    if (td1 || td2) {
      txtValue = td1.innerText + td2.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";

        if (odd) {
          odd = false;
          tr[i].classList.toggle("darker");
        } else {
          odd = true;
        }
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
search();
