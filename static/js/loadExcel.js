// globales
let jsonData = [];
var workbook = null;
let imgName = 'img.png'
// cuando cargo un archivo hago elegir la hoja
let fileSelector = document.getElementById('file');
fileSelector.addEventListener('change', (event) => {

  var selectedFile = event.target.files[0];
  imgName = selectedFile.name;
  var reader = new FileReader();
  reader.onload = function (event) {
    var data = event.target.result;
    workbook = XLSX.read(data, {
      type: 'binary'
    });

    // limpio el select y lo populo
    let select = document.getElementById('sheet-data');
    select.innerHTML = '<option>Elegí que hoja del excel usar</option>';
    workbook.SheetNames.forEach(function (sheetName) {
      let option = document.createElement("option");
      option.text = sheetName;
      select.add(option);
    });

  };
  reader.onerror = function (event) {
    alert("Hubo algún tipo de error con el archivo " + event.target.error.code);
  };
  
  reader.readAsBinaryString(selectedFile);
});

// preview de la hoja elegida
document.getElementById('sheet-data').addEventListener('change', (event) => {
  // jsonData
  jsonData = [];
  // console.log(event)
  // console.log(workbook)
  sheetName = document.getElementById('sheet-data').value;

  var XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
  var json_object = XL_row_object;

  // lo muestor en la preview
  output = document.getElementById('preview-data');
  output.innerHTML = json2Table(json_object);
  // genero los selects para elegir las cosas
  choicesFromData(json_object);
  jsonData = json_object;
  // console.log(jsonData)

});


// armo 2 selects con los headers del excel para ver que es cada cosa
function choicesFromData(jsonData) {
  // select de qué es cada cosa
  let selectHeaders = document.getElementsByClassName('select-headers');
  Array.from(selectHeaders).forEach((sel) => {
    sel.innerHTML = '<option>Elegí que columna del excel usar</option>';
  })
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
  let table = `
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

// send data to backend
form = document.getElementById('form');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  
  var btn = document.getElementById('submit-btn');
  var loadingText = '<div class="spinner-border spinner-border-sm" role="status"><span class="sr-only">Generando...span></div>\
                     Generando...</span></div>';
  btn.innerHTML = loadingText;
  btn.disabled = true;

  let values = document.querySelectorAll('.values');
  let arrVals = []
  values.forEach(userInput => {
    arrVals.push(userInput.value);
  });
  let colors = document.querySelectorAll('.input-color');
  let colorVals = []
  colors.forEach(userInput => {
    colorVals.push(userInput.value);
  });

  formData = {
    data: jsonData,
    colors: colorVals,
    provincia: document.getElementById('select-headers-provincia').value,
    datos: document.getElementById('select-headers-data').value,
    title: document.getElementById('title').value,
    classification: arrVals,
    datatable: document.getElementById('datatable').checked,
    legend: document.getElementById('color-legend').checked,
    antartida: document.getElementById('antartida').checked
  };
  // console.log(formData)
  // request options
  console.log(JSON.stringify(formData));
  let options = {
    method: 'POST',
    body: JSON.stringify(formData),
    headers: {
      'Content-Type': 'application/json'
    }
  };

  // send post request+
  fetch('/process', options)
    .then((res) => {
      console.log(res)
      if(res.status === 200) {
        return res.text()
      }
      throw new Error('Something went wrong.');

    })
    .then((res) => {
      document.getElementById('output-img')
          .setAttribute(
              'src', 'data:image/png;base64, '+res
          );
      document.getElementById('output-link').style.visibility = "visible";
      document.getElementById('output-link').href = 'data:application/octet-stream;base64, '+res;
      document.getElementById('output-link').download = `${imgName.substring(0, imgName.lastIndexOf('.'))}.png`;
            document.getElementById('output-img').download = `${imgName.substring(0, imgName.lastIndexOf('.'))}.png`;
      document.getElementById('output-img').style.visibility = "visible";
      // console.log(res)
      btn.innerHTML = 'Generar'
      btn.disabled = false;
    })
    .catch((err) => {
      console.log(err)
      alert('Hubo un error, ¿elegiste bien la columna de datos?')
      btn.innerHTML = 'Generar'
      btn.disabled = false;
    });

});

function makeColorPicker (colorsAndVals) {
  // rows de input de valor + color picker
  let colorDiv = document.getElementById('colors');
  colorDiv.innerHTML = '';
  colorsAndVals.forEach(function (el, i) {
    let colorRow = `
            <div class="row">
              <div class="col-3">
                <div class="form-group">
                  <label for="val${i}">Valor ${i}</label>
                  <input type="number" class="values" id="val${i}" value="${el[0]}">
                </div>
              </div>
              <div class="col-3">
                <div class="color">
                  <input type="color" class="input-color" value="${el[1]}">
                  <div class="invalid-feedback">
                    No es un color válido.
                  </div>
                </div>
              </div>
            </div>`;
    colorDiv.insertAdjacentHTML('beforeend', colorRow);
  });
};


let values = []
document.getElementById('select-headers-data').addEventListener('change', (event) => {
  let col = document.getElementById('select-headers-data').value;
  values = jsonData.map(a => a[col]);

  console.log(values)
  let datas = new geostats(values);
  document.getElementById('data-info').innerHTML = datas.info()
  document.getElementById('hidden-form').style.visibility = "visible";

});

function makeIntervalos () {
  let inter = parseInt(document.getElementById('intervalos').value);
  let e = document.getElementById('classification');
  let classificacion =  e.value;

  let datas = new geostats(values);

  let classValues = []
  if (classificacion == '1') {
    console.log('getClassEqInterval', datas.getClassEqInterval(inter));
    classValues = datas.getClassEqInterval(inter);
  }
  if (classificacion == '4') {
        console.log('getClassGeometricProgression', datas.getClassGeometricProgression(inter));
    classValues = datas.getClassGeometricProgression(inter);
  }
  if (classificacion == '2') {
    console.log('getClassStdDeviation', datas.getClassStdDeviation(inter));
    classValues = datas.getClassStdDeviation(inter);
  }
  if (classificacion == '3') {
    console.log('getClassArithmeticProgression', datas.getClassArithmeticProgression(inter));
    classValues = datas.getClassArithmeticProgression(inter);
  }
  if (classificacion == '5') {
    console.log('getClassQuantile', datas.getClassQuantile(inter));
    classValues = datas.getClassQuantile(inter);
  }
  if (classificacion == '6') {
    console.log('getClassJenks', datas.getClassJenks(inter));
    classValues = datas.getClassJenks(inter);
  }

  classValues.shift();
  
  const colors = palletes[inter+1];

  console.log(classValues);
  const colorsAndVals = [];
  if (document.getElementById('parse-int').checked){
    classValues.forEach((el, i) => {
      colorsAndVals.push([Math.round(el), colors[i]]);
    });
  } else {
    classValues.forEach((el, i) => {
      colorsAndVals.push([el, colors[i]]);
    });
  }

  console.log(colorsAndVals);
  makeColorPicker(colorsAndVals);
}
document.getElementById('classification').addEventListener('change', (event) => {
  makeIntervalos();
});

document.getElementById('intervalos').addEventListener('change', (event) => {
  makeIntervalos();
});


const palletes = {
    "2": [
        "#deebf7",
        "#9ecae1",
        "#3182bd"
    ],
    "3": [
        "#deebf7",
        "#9ecae1",
        "#3182bd"
    ],
    "4": [
        "#eff3ff",
        "#bdd7e7",
        "#6baed6",
        "#2171b5"
    ],
    "5": [
        "#eff3ff",
        "#bdd7e7",
        "#6baed6",
        "#3182bd",
        "#08519c"
    ],
    "6": [
        "#eff3ff",
        "#c6dbef",
        "#9ecae1",
        "#6baed6",
        "#3182bd",
        "#08519c"
    ],
    "7": [
        "#eff3ff",
        "#c6dbef",
        "#9ecae1",
        "#6baed6",
        "#4292c6",
        "#2171b5",
        "#084594"
    ],
    "8": [
        "#f7fbff",
        "#deebf7",
        "#c6dbef",
        "#9ecae1",
        "#6baed6",
        "#4292c6",
        "#2171b5",
        "#084594"
    ],
    "9": [
        "#f7fbff",
        "#deebf7",
        "#c6dbef",
        "#9ecae1",
        "#6baed6",
        "#4292c6",
        "#2171b5",
        "#08519c",
        "#08306b"
    ]
};