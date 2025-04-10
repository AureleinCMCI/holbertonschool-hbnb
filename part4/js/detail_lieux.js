document.addEventListener('DOMContentLoaded', function () {
    const placeDetailsContainer = document.getElementById('place-details');
    const reviewsContainer = document.getElementById('reviews');
    const placeId = new URLSearchParams(window.location.search).get('placeId'); // Récupérer l'ID du lieu depuis l'URL

    if (!placeId) {
        placeDetailsContainer.innerHTML = '<p>Le lieu n\'a pas été trouvé.</p>';
        return;
    }

    // Fonction pour récupérer les détails du lieu
    function fetchPlaceDetails() {
        fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`)
            .then(response => response.json())
            .then(place => {
                displayPlaceDetails(place);
                fetchReviews(placeId);  // Récupérer les avis du lieu
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des détails du lieu:', error);
                placeDetailsContainer.innerHTML = '<p>Erreur lors du chargement des détails.</p>';
            });
    }

    // Fonction pour afficher les détails du lieu
    function displayPlaceDetails(place) {
        // Afficher les détails du lieu dans la page
        const title = document.createElement('h1');
        title.textContent = place.title;

        const description = document.createElement('p');
        description.textContent = `Description: ${place.description}`;

        const price = document.createElement('p');
        price.textContent = `Prix par nuit: $${place.price}`;

        const amenities = document.createElement('p');
        
        // Vérifier si 'amenities' existe et est un tableau
        if (Array.isArray(place.amenities) && place.amenities.length > 0) {
            amenities.textContent = `Amenities: ${place.amenities.join(', ')}`;
        } else {
            amenities.textContent = 'Amenities: Non spécifiées';
        }

        // Ajouter tous les éléments au conteneur des détails du lieu
        placeDetailsContainer.appendChild(title);
        placeDetailsContainer.appendChild(description);
        placeDetailsContainer.appendChild(price);
        placeDetailsContainer.appendChild(amenities);
    }

    // Fonction pour récupérer et afficher les avis du lieu
    function fetchReviews(placeId) {
        fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`)
            .then(response => response.json())
            .then(reviews => {
                displayReviews(reviews);
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des avis:', error);
                reviewsContainer.innerHTML = '<p>not avis </p>';
            });
    }

    // Fonction pour afficher les avis du lieu
    function displayReviews(reviews) {
        reviewsContainer.innerHTML = ''; // Réinitialiser la section des avis
        if (reviews.length === 0) {
            reviewsContainer.innerHTML = '<p>Aucun avis pour ce lieu.</p>';
            return;
        }

        reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';

            const reviewText = document.createElement('p');
            reviewText.textContent = review.text;

            const rating = document.createElement('p');
            rating.textContent = `Note: ${review.rating}`;

            reviewCard.appendChild(reviewText);
            reviewCard.appendChild(rating);
            reviewsContainer.appendChild(reviewCard);
        });
    }

    // Appeler la fonction pour récupérer les détails du lieu
    fetchPlaceDetails();
});
