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
                displayReservationBox(place); // <--- AJOUT ICI
                fetchReviews(placeId);  // Récupérer les avis du lieu
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des détails du lieu:', error);
                placeDetailsContainer.innerHTML = '<p>Erreur lors du chargement des détails.</p>';
            });
    }

    function displayPlaceDetails(place) {
        const title = document.createElement('h1');
        title.textContent = place.title;
    
        const description = document.createElement('p');
        description.textContent = `Description: ${place.description}`;
    
        const price = document.createElement('p');
        price.textContent = `Prix par nuit: $${place.price}`;
    
        const amenities = document.createElement('p');
        
        if (Array.isArray(place.amenities) && place.amenities.length > 0) {
            amenities.textContent = `Amenities: ${place.amenities.join(', ')}`;
        } else {
            amenities.textContent = 'Amenities: Non spécifiées';
        }
        placeDetailsContainer.appendChild(title);
        placeDetailsContainer.appendChild(description);
        placeDetailsContainer.appendChild(price);
        placeDetailsContainer.appendChild(amenities);
    
    
        const placeImagesMap = {
            '363748f0-48f3-469f-a996-d6ead1414a99': [
                'base_fil/images/vila.avif',
                'base_fil/images/vila1.avif',
                'base_fil/images/vila2.avif',
                'base_fil/images/vila3.avif',
                'base_fil/images/vila4.avif'
            ],
            'autre-id-1234': [
                'base_fil/images/maison.jpg',
                'base_fil/images/place4.jpg'
            ],
            // Ajoute d'autres IDs avec leurs images ici
        };
        const imageUrls = placeImagesMap[place.id] || [];
        const imagesGridContainer = document.createElement('div');
        imagesGridContainer.className = 'images-grid';
        
        if (imageUrls.length > 0) {
            // Grande image à gauche
            const mainImage = document.createElement('img');
            mainImage.src = imageUrls[0];
            mainImage.alt = 'Image principale';
            mainImage.className = 'main-image';
            imagesGridContainer.appendChild(mainImage);
        
            // Container pour les 4 petites images à droite
            const sideImagesContainer = document.createElement('div');
            sideImagesContainer.className = 'side-images';
        
            for (let i = 1; i < 5 && i < imageUrls.length; i++) {
                const sideImg = document.createElement('img');
                sideImg.src = imageUrls[i];
                sideImg.alt = `Image ${i + 1}`;
                sideImg.className = 'side-image';
                sideImagesContainer.appendChild(sideImg);
            }
            imagesGridContainer.appendChild(sideImagesContainer);
        } else {
            const noImagesMsg = document.createElement('p');
            noImagesMsg.textContent = 'Aucune image disponible pour ce lieu.';
            imagesGridContainer.appendChild(noImagesMsg);
        }
        
        placeDetailsContainer.appendChild(imagesGridContainer);
        let modal = document.getElementById('image-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'image-modal';
            modal.innerHTML = `
                <span class="close-modal">&times;</span>
                <img class="modal-content" id="modal-img">
                <button class="modal-prev">&#10094;</button>
                <button class="modal-next">&#10095;</button>
            `;
            document.body.appendChild(modal);
    
            // Fermer la modale
            modal.querySelector('.close-modal').onclick = function() {
                modal.style.display = "none";
            };
        }
    
            const allImages = imagesGridContainer.querySelectorAll('img');
            let currentImgIndex = 0;
    
            allImages.forEach((img, idx) => {
                img.style.cursor = 'pointer';
                img.onclick = function() {
                    showModal(idx);
                };
            });
    
            function showModal(index) {
                currentImgIndex = index;
                modal.style.display = "flex";
                modal.querySelector('#modal-img').src = imageUrls[currentImgIndex];
            }
    
            // 3. Navigation dans la modale
            modal.querySelector('.modal-prev').onclick = function() {
                currentImgIndex = (currentImgIndex === 0) ? imageUrls.length - 1 : currentImgIndex - 1;
                showModal(currentImgIndex);
            };
            modal.querySelector('.modal-next').onclick = function() {
                currentImgIndex = (currentImgIndex === imageUrls.length - 1) ? 0 : currentImgIndex + 1;
                showModal(currentImgIndex);
            };
    
    }

    // AJOUT : Fonction pour afficher la box de réservation
    function displayReservationBox(place) {
        const box = document.getElementById('reservation-box');
        if (!box) return; // Si le div n'existe pas, on ne fait rien

        box.innerHTML = `
            <div class="reservation-card">
                <div class="price-row">
                    <span class="price">${place.price} €</span> <span class="per-night">par nuit</span>
                </div>
                <form id="booking-form">
                    <div class="date-row">
                        <div>
                            <label>Arrivée</label>
                            <input type="date" id="date-arrivee" required>
                        </div>
                        <div>
                            <label>Départ</label>
                            <input type="date" id="date-depart" required>
                        </div>
                    </div>
                    <div>
                        <label>Voyageurs</label>
                        <select id="voyageurs">
                            <option>1 voyageur</option>
                            <option>2 voyageurs</option>
                            <option>3 voyageurs</option>
                            <option>4 voyageurs</option>
                            <option>5 voyageurs</option>
                            <option>6 voyageurs</option>
                            <option>7 voyageurs</option>
                        </select>
                    </div>
                    <button type="button" id="btn-reserver">Réserver</button>
                </form>
                <div id="booking-details" style="display:none;">
                    <div class="row"><span>${place.price} € x <span id="nb-nuits">0</span> nuits</span> <span id="prix-nuits">0 €</span></div>
                    <div class="row"><span>Frais de ménage</span> <span id="frais-menage">100 €</span></div>
                    <div class="row"><span>Frais de service Airbnb</span> <span id="frais-service">311 €</span></div>
                    <div class="row"><span>Taxes</span> <span id="taxes">10 €</span></div>
                    <div class="row total"><span>Total</span> <span id="total">0 €</span></div>
                </div>
            </div>
        `;

        document.getElementById('btn-reserver').onclick = function() {
            const arrivee = document.getElementById('date-arrivee').value;
            const depart = document.getElementById('date-depart').value;
            const voyageurs = document.getElementById('voyageurs').value;
            const prixNuit = place.price;
            const nbNuits = (new Date(depart) - new Date(arrivee)) / (1000 * 60 * 60 * 24);
        
            if (nbNuits > 0) {
                // Calcul du total
                const total = (prixNuit * nbNuits) + 100 + 311 + 10;
        
                // Création de l'objet à ajouter au panier
                const userId = localStorage.getItem('user_id') || 'guest';
                const cartKey = `cart_${userId}`;
                const cartItem = {
                    id: place.id,
                    title: place.title,
                    description: `${arrivee} au ${depart} - ${voyageurs}`,
                    price: total,
                    nights: nbNuits,
                    dateStart: arrivee,
                    dateEnd: depart
                };
        
                // Ajout au panier
                let cart = JSON.parse(localStorage.getItem(cartKey)) || [];
                cart.push(cartItem);
                localStorage.setItem(cartKey, JSON.stringify(cart));
        
                // Redirection vers la page d'avis AVEC l'ID du lieu
                window.location.href = `add_review.html?placeId=${place.id}`;
        
            } else {
                alert("Veuillez sélectionner des dates valides.");
            }
        };
        
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

   
   