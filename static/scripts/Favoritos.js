document.addEventListener('DOMContentLoaded', function () {
    const btnsFavorite = document.querySelectorAll('.favorite');
    const products = document.querySelectorAll('.card-product');
    const counterFavorites = document.querySelector('.counter-favorite');

    // Asegúrate de que este selector sea correcto y apunte al contenedor de la lista de favoritos
    const listFavorites = document.querySelector('.list-favorites');
    const containerListFavorites = document.querySelector('.container-list-favorites'); // Asegúrate de que este exista

    let favorites = [];

    // Actualizar favoritos en localStorage
    const updateFavoritesInLocalStorage = () => {
        localStorage.setItem('favorites', JSON.stringify(favorites));
    };

    // Cargar favoritos desde localStorage
    const loadFavoritesFromLocalStorage = () => {
        const storedFavorites = localStorage.getItem('favorites');

        if (storedFavorites) {
            favorites = JSON.parse(storedFavorites);
            showHTML();  // Mostrar HTML con los favoritos cargados
            updateFavoriteMenu();  // Actualizar el menú de favoritos cargados
        }
    };

    // Alternar favoritos (añadir o eliminar)
    const toggleFavorite = product => {
        const index = favorites.findIndex(favorite => favorite.id === product.id);

        if (index > -1) {
            favorites.splice(index, 1); // Eliminar si ya está en favoritos
        } else {
            favorites.push(product); // Agregar si no está en favoritos
        }
        updateFavoritesInLocalStorage();
        updateFavoriteMenu(); // Actualiza el menú cada vez que cambias los favoritos
    };

    // Función para eliminar el producto de favoritos
    const removeFromFavorites = (productId) => {
        favorites = favorites.filter(fav => fav.id !== productId);
        updateFavoritesInLocalStorage();  // Actualizar el localStorage
        showHTML();  // Actualizar la interfaz
        updateFavoriteMenu();  // Actualizar la lista de favoritos
    };

    // Actualizar la lista de favoritos en el menú
    const updateFavoriteMenu = () => {
        if (listFavorites) { // Verifica si listFavorites existe
            listFavorites.innerHTML = ''; // Limpiar lista

            // Recorrer todos los favoritos y mostrarlos en la lista
            favorites.forEach(fav => {
                // Crear un nuevo elemento 'div' para el producto favorito
                const favoriteCard = document.createElement('div');
                favoriteCard.classList.add('card-favorite');

                // Crear y añadir el título del producto
                const titleElement = document.createElement('p');
                titleElement.classList.add('title');
                titleElement.textContent = fav.title;
                favoriteCard.appendChild(titleElement);

                // Crear y añadir el precio del producto
                const priceElement = document.createElement('p');
                priceElement.textContent = fav.price;
                favoriteCard.appendChild(priceElement);

                // Crear y añadir el botón de eliminar
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'X';  // Texto para el botón de eliminar
                deleteButton.classList.add('delete-favorite');
                deleteButton.addEventListener('click', () => {
                    removeFromFavorites(fav.id);  // Llamar a la función para eliminar
                });
                favoriteCard.appendChild(deleteButton);

                // Añadir el producto favorito a la lista
                listFavorites.appendChild(favoriteCard);
            });

            // Actualizar el contador de favoritos
            counterFavorites.textContent = favorites.length;
        }
    };

    // Mostrar HTML actualizado
    const showHTML = () => {
        btnsFavorite.forEach(button => {
            const card = button.closest('.content-card-product');
            const productId = card.dataset.productId;

            const isFavorite = favorites.some(favorite => favorite.id === productId);

            button.classList.toggle('active', isFavorite); // Alternar clase 'active' en un solo ícono
        });

        updateFavoriteMenu();  // Asegurarse de que la lista de favoritos esté actualizada
    };

    // Añadir eventos a los botones de favorito
    btnsFavorite.forEach(button => {
        if (button) {  // Verifica si los botones existen
            button.addEventListener('click', e => {
                const card = e.target.closest('.content-card-product');

                const product = {
                    id: card.dataset.productId,
                    title: card.querySelector('h3').textContent,
                    price: card.querySelector('.price').textContent,
                };

                toggleFavorite(product);
                showHTML();
            });
        }
    });

    // Controlar apertura y cierre del menú de favoritos
    const btnClose = document.querySelector('#btn-close');
    const buttonHeaderFavorite = document.querySelector('#button-header-favorite');

    if (buttonHeaderFavorite) {
        buttonHeaderFavorite.addEventListener('click', () => {
            containerListFavorites.classList.toggle('show');
        });
    }

    if (btnClose) {
        btnClose.addEventListener('click', () => {
            containerListFavorites.classList.remove('show');
        });
    }

    // Cargar favoritos al iniciar la página
    loadFavoritesFromLocalStorage();
});

