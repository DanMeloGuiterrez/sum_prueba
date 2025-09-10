// Transicion de Imagenes   
let imagenes = [
  {
    url: "/static/img/Imagenes/imagen1.jpg",
    descripcion: "CRONOGRAMA DE ACTIVIDADES ACADÉMICAS 2025 - PREGRADO",
    descripcion2: "Cursos de Verano 2025-0, Año Académico 2025 (Anual) y los Semestres Académicos 2025-I y 2025-II",
  
  },
  {
    url: "/static/img/Imagenes/imagen2.jpg",
    descripcion: "CRONOGRAMA DE ACTIVIDADES ACADÉMICAS 2025 - POSGRADO",
    descripcion2: "Doctorados, Maestrías y Segunda Especialidad",
  },
  {
    url: "/static/img/Imagenes/imagen3.jpg",
    descripcion: "GUÍA SUM",
    descripcion2: "Aquí encontrarás las guías para el manejo del SUM.",
  
  },
  {
    url: "/static/img/Imagenes/imagen4.jpg",
    descripcion: "CAPACITACIÓN DE INGRESO CARGA ACADÉMICA",
    descripcion2: "Entérate sobre lo ocurrido en el Taller de capacitación sobre el uso del aplicativo Actividad Académica de Docente.",
  },
];

let atras = document.getElementById("atras");
let adelante = document.getElementById("adelante");
let imagen = document.getElementById("img");
let puntos = document.getElementById("puntos");

let actual = 0;
posicionCarrusel();

atras.addEventListener("click", function () {
  actual -= 1;
  if (actual === -1) {
    actual = imagenes.length - 1;
  }
  imagen.innerHTML = `
        <img class="img" src="${imagenes[actual].url}" alt="logo pagina" loading="lazy"></img>
        <div class="texto_imagen">
            <p>${imagenes[actual].descripcion}</p>
            <p style="font-size: 10px;">${imagenes[actual].descripcion2}</p>
        </div>
    `;
  posicionCarrusel();
});

adelante.addEventListener("click", function () {
  actual += 1;
  if (actual === imagenes.length) {
    actual = 0;
  }
  imagen.innerHTML = `
        <img class="img" src="${imagenes[actual].url}" alt="logo pagina" loading="lazy"></img>
        <div class="texto_imagen">
            <p>${imagenes[actual].descripcion}</p>
            <p style="font-size: 10px;">${imagenes[actual].descripcion2}</p>
        </div>
    `;
  posicionCarrusel();
});

function posicionCarrusel() {
  puntos.innerHTML = "";
  for (var i = 0; i < imagenes.length; i++) {
    if (i == actual) {
      puntos.innerHTML += '<p class="bold">.<p>';
    } else {
      puntos.innerHTML += "<p>.<p>";
    }
  }
}

