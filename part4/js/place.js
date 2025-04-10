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

    function addToCart(place) {
        const userId = getUserIdFromSession();
        if (!userId) {
            alert("Veuillez vous connecter pour ajouter au panier.");
            return;
        }

        cart.push(place);
        localStorage.setItem(`cart_${userId}`, JSON.stringify(cart));
        alert(`"${place.title}" a été ajouté à votre panier.`);
    }

    function fetchPlaces() {
        fetch('http://127.0.0.1:5000/api/v1/places/')
            .then(response => response.json())
            .then(places => {
                placesList.innerHTML = '';

                places.forEach(place => {
                    const card = document.createElement('article');
                    card.className = 'place-card';

                    const title = document.createElement('h2');
                    title.textContent = place.title;

                    const price = document.createElement('p');
                    price.textContent = `Prix par nuit : $${place.price}`;

                    const desc = document.createElement('p');
                    desc.textContent = `Description : ${place.description}`;

                    const button = document.createElement('button');
                    button.textContent = 'Ajouter au panier';
                    button.className = 'choose-button';
                    button.addEventListener('click', () => addToCart(place));

                    card.appendChild(title);
                    card.appendChild(price);
                    card.appendChild(desc);
                    card.appendChild(button);

                    placesList.appendChild(card);
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
