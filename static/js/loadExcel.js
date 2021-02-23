// // loaded
// window.onload = function () {
//   console.log('Page is loaded');
// };
// jsonData
let jsonData = []
// get file id
const fileSelector = document.getElementById('file');

// cuando cargo un archivo lo convierto en json
fileSelector.addEventListener('change', (event) => {
  var selectedFile = event.target.files[0];
  var reader = new FileReader();
  reader.onload = function (event) {
    var data = event.target.result;
    var workbook = XLSX.read(data, {
      type: 'binary'
    });
    workbook.SheetNames.forEach(function (sheetName) {

      var XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
      var json_object = XL_row_object;

      // lo muestor en la preview
      output = document.getElementById('preview-data');
      output.innerHTML = json2Table(json_object);
      // genero los selects para elegir las cosas
      choicesFromData(json_object);
      jsonData = json_object;
      // console.log('done xls');
    })
  };
  reader.onerror = function (event) {
    alert("Hubo algún tipo de error con el archivo " + event.target.error.code);
  };
  
  reader.readAsBinaryString(selectedFile);
});

// armo 2 selects con los headers del excel para ver que es cada cosa
function choicesFromData(jsonData) {
  // select de qué es cada cosa
  const selectHeaders = document.getElementsByClassName('select-headers');
  Object.keys(jsonData[0]).forEach((el) => {
    Array.from(selectHeaders).forEach((sel) => {
      var option = document.createElement("option");
      option.text = el;
      sel.add(option);
    });
  });
}

// tabla de preview
function json2Table(jsonData) {
  let cols = Object.keys(jsonData[0]);

  //Map over columns, make headers,join into string
  let headerRow = cols
    .map(col => `<th scope="col">${col}</th>`)
    .join("");

  //map over array of json objs, for each row(obj) map over column values,
  //and return a td with the value of that object for its column
  //take that array of tds and join them
  //then return a row of the tds
  //finally join all the rows together
  let rows = jsonData
    .map(row => {
      let tds = cols.map(col => `<td>${row[col]}</td>`).join("");
      return `<tr>${tds}</tr>`;
    })
    .join("");

  //build the table
  const table = `
	<table class="table">
		<thead>
			<tr>${headerRow}</tr>
		<thead>
		<tbody>
			${rows}
		<tbody>
	<table>`;

  return table;
}
// color picker
function changeColors(colorList) {
  const output = document.getElementById('color-scheme-preview');
  
  let rows = colorList
  .map(row => {
    let box = `<span class="border" style="background-color:${row}"></span>`
    return `<tr>${box}</tr>`;
  })
  .join("");
  
  output.innerHTML = rows;
}
const colorSchemeInput = document.getElementById('color-scheme');
colorSchemeInput.value = "['#ffffe5','#f7fcb9','#d9f0a3','#addd8e','#78c679','#41ab5d','#238443','#006837','#004529']";
changeColors(['#ffffe5','#f7fcb9','#d9f0a3','#addd8e','#78c679','#41ab5d','#238443','#006837','#004529']);

colorSchemeInput.addEventListener('change', (event) => {
  const colors = event.target.value.replace(/[\[\]']+/g,'').split(',');
  changeColors(colors);

});

// send data to backend
form = document.getElementById('form');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  
  var btn = document.getElementById('submit-btn');
  var loadingText = '<div class="spinner-border spinner-border-sm" role="status"><span class="sr-only">Generando...span></div>\
                     Generando...</span></div>';
  btn.innerHTML = loadingText;
  btn.disabled = true;
  
  formData = {
    data: jsonData,
    colors: document.getElementById('color-scheme').value.replace(/[\[\]']+/g,'').split(','),
    provincia: document.getElementById('select-headers-provincia').value,
    datos: document.getElementById('select-headers-data').value,
    title: document.getElementById('title').value,
    classification: document.getElementById('classification').value.split(','),
    datatable: document.getElementById('datatable').checked,
    legend: document.getElementById('color-legend').checked
  }
  // console.log(formData)
  // request options
  const options = {
    method: 'POST',
    body: JSON.stringify(formData),
    headers: {
      'Content-Type': 'application/json'
    }
  };

  // send post request+
  fetch('/process', options)
    .then(res => res.text())
    .then((res) => {
      document.getElementById('output-img')
          .setAttribute(
              'src', 'data:image/png;base64, '+res
          );
      document.getElementById('output-img').style.visibility = "visible";
      // console.log(res)
      btn.innerHTML = 'Generar'
      btn.disabled = false;
    })
    .catch((err) => {
      console.log(err)
      alert('Hubo un error, ¿elegiste bien la columna de datos?')
    });

});
