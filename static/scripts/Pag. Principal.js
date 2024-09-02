// Inicialización de Swiper (ya existe)
let swiper = new Swiper(".mySwiper", {
  slidesPerView: 3,
  spaceBetween: 30,
  grabCursor: true,
  loop: true,
  autoplay: {
    delay: 1800,
    disableOnInteraction: false,
  },
  breakpoints: {
    991: {
      slidesPerView: 3,
    },
    768: {
      slidesPerView: 2,
    },
    576: {
      slidesPerView: 1,
    },
  },
});

// Ejemplo de datos de sugerencias (puedes obtener estos datos de un servidor o API)
const suggestionsData = [
  'tratamiento facial',
  'tratamiento corporal',
  'tratamiento capilar',
  'tratamiento de uñas',
  'tratamiento de pies',
  'tratamiento relajante',
  'tratamiento antiedad'
];

// Mostrar sugerencias al usuario
function showSuggestions(query) {
  const suggestionsContainer = document.getElementById('suggestions');
  suggestionsContainer.innerHTML = ''; // Limpiar sugerencias previas

  if (query.length === 0) {
      suggestionsContainer.style.display = 'none';
      return;
  }

  const filteredSuggestions = suggestionsData.filter(item => item.toLowerCase().includes(query.toLowerCase()));
  
  filteredSuggestions.forEach(suggestion => {
      const suggestionItem = document.createElement('div');
      suggestionItem.textContent = suggestion;
      suggestionItem.classList.add('suggestion-item');
      suggestionItem.onclick = () => selectSuggestion(suggestion);
      suggestionsContainer.appendChild(suggestionItem);
  });

  suggestionsContainer.style.display = 'block'; // Mostrar las sugerencias
}

function selectSuggestion(suggestion) {
  document.getElementById('search-input').value = suggestion;
  document.getElementById('suggestions').style.display = 'none'; // Ocultar las sugerencias
}

// Ocultar sugerencias al hacer clic fuera
document.addEventListener('click', function(event) {
  if (!event.target.closest('.search-container')) {
      document.getElementById('suggestions').style.display = 'none';
  }
});


