document.addEventListener('DOMContentLoaded', function () {
    const placesList = document.getElementById('places-list');
    let cart = [];

    function getUserIdFromSession() {
        return localStorage.getItem('user_id');
    }

    function loadCartFromStorage() {
        const userId = getUserIdFromSession();
        if (!userId) return;

        const storedCart = localStorage.getItem(`cart_${userId}`);
        if (storedCart) {
            cart = JSON.parse(storedCart);
        }
    }

    function getDynamicImage(index) {
        // Tableau d'URLs d'images (modifiez selon vos besoins)
        const imageUrls = [
            'base_fil/images/maison.jpg',
            'base_fil/images/vila.avif',
            'base_fil/images/maison.jpg',
            'base_fil/images/place4.jpg',
            'base_fil/images/place5.jpg'
        ];
        // Retourne une image basée sur l'index
        return imageUrls[index % imageUrls.length];
    }

    function fetchPlaces() {
        fetch('http://127.0.0.1:5000/api/v1/places/')
            .then(response => response.json())
            .then(places => {
                placesList.innerHTML = ''; // Vider le contenu de la liste avant de charger les nouveaux lieux

                places.forEach((place, index) => {
                    const card = document.createElement('div');
                    card.className = 'col-sm';

                    const cardContainer = document.createElement('div');
                    cardContainer.className = `card custom-card card-${place.id}`;
                    card.appendChild(cardContainer);

                    // Créer le couvert de la carte avec une image dynamique
                    const cardCover = document.createElement('div');
                    cardCover.className = 'card-cover';
                    cardCover.style.backgroundImage = `url('${getDynamicImage(index)}')`;
                    cardContainer.appendChild(cardCover);

                    const title = document.createElement('h5');
                    title.className = 'card-title';
                    title.textContent = place.title;
                    cardContainer.appendChild(title);

                    const price = document.createElement('p');
                    price.className = 'card-text';
                    price.textContent = `Prix par nuit : $${place.price}`;
                    cardContainer.appendChild(price);

                    const desc = document.createElement('p');
                    desc.className = 'card-text';
                    desc.textContent = `Description : ${place.description}`;
                    cardContainer.appendChild(desc);

                    const button = document.createElement('button');
                    button.className = 'choose-button';
                    button.textContent = 'Voir les details';
                    button.addEventListener('click', () => addToCart(place));
                    cardContainer.appendChild(button);

                    const placeLink = document.createElement('a');
                    placeLink.href = `place.html?placeId=${place.id}`;
                    placeLink.className = 'place-link';
                    placeLink.appendChild(cardContainer);

                    placesList.appendChild(placeLink);
                });
            })
            .catch(err => {
                console.error('Erreur lors du chargement des lieux :', err);
                placesList.innerHTML = '<p>Erreur lors du chargement.</p>';
            });
    }

    loadCartFromStorage();
    fetchPlaces();
});