document.addEventListener('DOMContentLoaded', function () {
    const btnsFavorite = document.querySelectorAll('.favorite');
    const products = document.querySelectorAll('.card-product');
    const counterFavorites = document.querySelector('.counter-favorite');
    const listFavorites = document.querySelector('.list-favorites');
    const containerListFavorites = document.querySelector('.container-list-favorites');

    let favorites = [];

    const updateFavoritesInLocalStorage = () => {
        localStorage.setItem('favorites', JSON.stringify(favorites));
    };

    const loadFavoritesFromLocalStorage = () => {
        const storedFavorites = localStorage.getItem('favorites');

        if (storedFavorites) {
            favorites = JSON.parse(storedFavorites);
            showHTML();
            updateFavoriteMenu();
        }
    };

    const toggleFavorite = product => {
        const index = favorites.findIndex(favorite => favorite.id === product.id);

        if (index > -1) {
            favorites.splice(index, 1);
        } else {
            favorites.push(product);
        }
        updateFavoritesInLocalStorage();
        updateFavoriteMenu();
    };

    const removeFromFavorites = (productId) => {
        favorites = favorites.filter(fav => fav.id !== productId);
        updateFavoritesInLocalStorage();
        showHTML();
        updateFavoriteMenu();
    };

    const updateFavoriteMenu = () => {
        if (listFavorites) {
            listFavorites.innerHTML = '';

            favorites.forEach(fav => {
                const favoriteCard = document.createElement('div');
                favoriteCard.classList.add('card-favorite');

                const titleElement = document.createElement('p');
                titleElement.classList.add('title');
                titleElement.textContent = fav.title;
                favoriteCard.appendChild(titleElement);

                const priceElement = document.createElement('p');
                priceElement.textContent = fav.price;
                favoriteCard.appendChild(priceElement);

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Borrar';
                deleteButton.classList.add('delete-favorite');
                deleteButton.addEventListener('click', () => {
                    removeFromFavorites(fav.id);
                });
                favoriteCard.appendChild(deleteButton);

                listFavorites.appendChild(favoriteCard);
            });

            counterFavorites.textContent = favorites.length;
        }
    };

    const showHTML = () => {
        btnsFavorite.forEach(button => {
            const card = button.closest('.content-card-product');
            const productId = card.dataset.productId;

            const isFavorite = favorites.some(favorite => favorite.id === productId);

            button.classList.toggle('active', isFavorite);
        });

        updateFavoriteMenu();
    };

    btnsFavorite.forEach(button => {
        if (button) {
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

    loadFavoritesFromLocalStorage();
});

