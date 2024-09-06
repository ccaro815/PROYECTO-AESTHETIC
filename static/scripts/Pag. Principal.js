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

const suggestionsData = [
  { nombre: 'Tratamientos Faciales', ruta: '/tratamientos_facial' },
  { nombre: 'Tratamientos Corporales', ruta: '/tratamientos_corporales' },
  { nombre: 'Depilación', ruta: '/tratamientos_depilacion' },
  { nombre: 'Masajes', ruta: '/tratamientos_masajes' },
  { nombre: 'Spa de Manos', ruta: '/tratamientos_spa_de_manos' },
  { nombre: 'Gift Card', ruta: '/gif_card' }

];

function showSuggestions(query) {
  const suggestionsContainer = document.getElementById('suggestions');
  suggestionsContainer.innerHTML = '';

  if (query.length === 0) {
    suggestionsContainer.style.display = 'none';
    return;
  }
  const filteredSuggestions = suggestionsData.filter(item => item.nombre.toLowerCase().includes(query.toLowerCase()));
  filteredSuggestions.forEach(suggestion => {
    const suggestionItem = document.createElement('div');
    suggestionItem.textContent = suggestion.nombre;
    suggestionItem.classList.add('suggestion-item');
    suggestionItem.onclick = () => {
      document.getElementById('search-input').value = suggestion.nombre;
      window.location.href = suggestion.ruta;
    };
    suggestionsContainer.appendChild(suggestionItem);
  });

  suggestionsContainer.style.display = 'block';
}

function searchService(event) {
  if (event.key === 'Enter') {
    const query = document.getElementById('search-input').value.toLowerCase();

    const match = suggestionsData.find(item => item.nombre.toLowerCase().includes(query));
    if (match) {
      window.location.href = match.ruta;
    } else {
      alert('Servicio no encontrado. Intente con términos como: facial, corporal, depilacion, masajes, manos, o gift card.');
    }
  }
}

document.addEventListener('click', function(event) {
  if (!event.target.closest('.search-container')) {
    document.getElementById('suggestions').style.display = 'none';
  }
});


