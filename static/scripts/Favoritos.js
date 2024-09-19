const btnsFavorite = document.querySelectorAll('.favorite');
const products = document.querySelectorAll('.card-product');
const counterFavorites = document.querySelector('.counter-favorite');

const containerListFavorites = document.querySelector(
	'.container-list-favorites'
);
const listFavorites = document.querySelector('.list-favorites');

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
		showHTML();
	}
};

// Alternar favoritos (añadir o eliminar)
const toggleFavorite = product => {
	const index = favorites.findIndex(
		element => element.id === product.id
	);

	if (index > -1) {
		// Si ya está en favoritos, lo eliminamos
		favorites.splice(index, 1);
	} else {
		// Si no está, lo agregamos
		favorites.push(product);
	}
	// Actualizar el localStorage después de modificar favoritos
	updateFavoritesInLocalStorage();
};

// Función para eliminar el producto de favoritos
const removeFromFavorites = (productId) => {
	favorites = favorites.filter(fav => fav.id !== productId);
	updateFavoritesInLocalStorage();  // Actualizar el localStorage
	showHTML();  // Actualizar la interfaz
};

// Actualizar la lista de favoritos en el menú
const updateFavoriteMenu = () => {
	listFavorites.innerHTML = '';

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
};

// Mostrar HTML actualizado
const showHTML = () => {
	products.forEach(product => {
		const contentProduct = product.querySelector(
			'.content-card-product'
		);
		const productId = contentProduct.dataset.productId;
		const isFavorite = favorites.some(
			favorite => favorite.id === productId
		);

		const favoriteButton = product.querySelector('.favorite');
		const favoriteActiveButton =
			product.querySelector('#added-favorite');
		const favoriteRegularIcon = product.querySelector(
			'#favorite-regular'
		);
		favoriteButton.classList.toggle('favorite-active', isFavorite);
		favoriteRegularIcon.classList.toggle('active', isFavorite);
		favoriteActiveButton.classList.toggle('active', isFavorite);
	});

	// Actualizar la lista de favoritos y el contador
	updateFavoriteMenu();
};

// Añadir eventos a los botones de favorito
btnsFavorite.forEach(button => {
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
});

// Controlar apertura y cierre del menú de favoritos
const btnClose = document.querySelector('#btn-close');
const buttonHeaderFavorite = document.querySelector(
	'#button-header-favorite'
);

buttonHeaderFavorite.addEventListener('click', () => {
	containerListFavorites.classList.toggle('show');
});

btnClose.addEventListener('click', () => {
	containerListFavorites.classList.remove('show');
});

// Cargar favoritos al iniciar la página
loadFavoritesFromLocalStorage();
updateFavoriteMenu();

