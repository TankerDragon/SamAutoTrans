function getCSRF() {
  arr = document.getElementById("csrf").innerHTML.split("value");
  arr = arr[1].split('"');
  return arr[1];
}
function update(data) {
  body = "";
  for (let i = 0; i < data.length; i++) {
    body += `
    <tr>
      <td>${data[i].id}</td>
      <td>${data[i].name}</td>
      <td>${Math.round(data[i].odometer * 0.000621371)}</td>
      <td>${data[i].latitude}</td>
      <td>${data[i].longitude}</td>
      <td>${data[i].speed}</td>
      <td>${data[i].location}</td>
    </tr>
    `;
    // console.log(data[i]);
  }
  document.getElementById("tbody").innerHTML = body;
  sortTable();
}
function get() {
  fetch("/samsara/get-data/")
    .then((res) => res.json())
    .then((data) => {
      // console.log("json data: ", data);
      update(data.data);
    });
}
get();
setInterval(get, 5000);

///
function sortTable() {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("tbody");
  switching = true;
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    console.log(table.rows);
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 0; i < rows.length - 1; i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[1];
      y = rows[i + 1].getElementsByTagName("TD")[1];
      //check if the two rows should switch place:
      if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
        //if so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}
