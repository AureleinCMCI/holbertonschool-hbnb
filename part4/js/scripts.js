/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    /* DO SOMETHING */
  });
  const places = [
    { name: "Cozy Cabin", price: 120 },
    { name: "Modern Loft", price: 150 },
    { name: "Beachside Bungalow", price: 200 },
    { name : "Palace bord de plage" , price : 500},
    { name : "Palace bord de plage" , price : 500},
    { name : "Palace bord de plage" , price : 500},
    { name : "Palace bord de plage" , price : 500},
    
  ];
  
  const placesList = document.getElementById('places-list');
  
  places.forEach(place => {
    const card = document.createElement('article');
    card.className = 'place-card';
  
    const title = document.createElement('h2');
    title.textContent = place.name;
  
    const price = document.createElement('p');
    price.textContent = `Price per night: $${place.price}`;
  
    const button = document.createElement('button');
    button.className = 'details-button';
    button.textContent = 'View Details';
  
    card.appendChild(title);
    card.appendChild(price);
    card.appendChild(button);
  
    placesList.appendChild(card);
  });
  document.addEventListener('DOMContentLoaded', function() {
    const placeDetailsSection = document.getElementById('place-details');
    const reviewsSection = document.getElementById('reviews');
    const addReviewSection = document.getElementById('add-review');
    const reviewForm = document.getElementById('review-form');

    // Dummy data - replace with real data as needed
    const place = {
        title: "Ocean View Villa",
        host: "John Doe",
        price: "$150 per night",
        description: "A beautiful villa with ocean views, perfect for a relaxing vacation.",
        amenities: ["WiFi", "Pool", "Parking", "AC"],
    };

    const reviews = [
        { comment: "Amazing place, had a great time!", username: "JaneDoe", rating: 5 },
        { comment: "Nice place but needs more amenities.", username: "MarkSmith", rating: 3 },
    ];

    // Function to populate place details
    function populatePlaceDetails() {
        placeDetailsSection.innerHTML = `
            <h1>${place.title}</h1>
            <p><strong>Host:</strong> ${place.host}</p>
            <p><strong>Price:</strong> ${place.price}</p>
            <p><strong>Description:</strong> ${place.description}</p>
            <div><strong>Amenities:</strong>
                <ul>
                    ${place.amenities.map(amenity => `<li>${amenity}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    // Function to populate reviews
    function populateReviews() {
        if (reviews.length > 0) {
            reviewsSection.innerHTML += reviews.map(review => `
                <div class="review-card">
                    <p><strong>Comment:</strong> ${review.comment}</p>
                    <p><strong>By:</strong> ${review.username}</p>
                    <p><strong>Rating:</strong> ⭐⭐⭐⭐⭐</p>
                </div>
            `).join('');
        } else {
            reviewsSection.innerHTML += "<p>No reviews yet. Be the first to review this place!</p>";
        }
    }

    // Show or hide add review section based on user login status
    function checkUserLogin() {
        const userLoggedIn = true; // Replace this with actual logic to check user login status
        if (userLoggedIn) {
            addReviewSection.style.display = 'block'; // Show add review form if logged in
        } else {
            addReviewSection.style.display = 'none'; // Hide add review section if not logged in
        }
    }

    // Event listener for submitting a review
    reviewForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const reviewText = document.getElementById('review-text').value;
        const rating = document.getElementById('rating').value;

        // Add the new review to the reviews array (you can also send this to a server)
        reviews.push({ comment: reviewText, username: "LoggedInUser", rating: rating });

        // Re-populate reviews
        populateReviews();

        // Clear form
        reviewForm.reset();
    });

    // Initialize page content
    populatePlaceDetails();
    populateReviews();
    checkUserLogin();
});

document.addEventListener('DOMContentLoaded', function () {
  // Sélection du formulaire par son ID
  const loginForm = document.getElementById('login-form');

  // Ajout de l’écouteur d’événement sur la soumission du formulaire
  loginForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Empêche le rechargement de la page

    // Ici tu pourras ajouter la logique de connexion (requête AJAX, etc.)
    console.log('Formulaire soumis (sans rechargement de page)');
  });
});


// DANS CE CODE ? QUAND L'UTILISATEUR SERA CONNECTER ON VA AFFICHER DECONEXION ET LOGIN QUAND IL SERA CONNECTER //
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }
  document.addEventListener("DOMContentLoaded", () => {
    const loginLink = document.getElementById("login-link"); // lien de connexion
    const token = getCookie("token");
  
    if (token) {
      // Utilisateur authentifié → on cache le lien de connexion
      if (loginLink) loginLink.style.display = "none";
    } else {
      // Pas de token → utilisateur non connecté → on affiche le lien
      if (loginLink) loginLink.style.display = "inline-block";
    }
  });
  //////// Fonction pour récupérer la valeur d'un cookie par son nom , 
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}
//pour masque est affiche le button connexion et deconexion 
document.addEventListener("DOMContentLoaded", () => {
  // Récupérer le token JWT depuis les cookies
  const token = getCookie("token");

  // Vérifier si le token est présent
  if (token) {
      // Si le token existe, l'utilisateur est connecté
      document.getElementById("login-link").style.display = "none"; // Cache le bouton Login
      document.getElementById("logout-link").style.display = "block"; // Affiche le bouton Déconnexion
  } else {
      // Si le token n'existe pas, l'utilisateur n'est pas connecté
      document.getElementById("login-link").style.display = "block";
      document.getElementById("logout-link").style.display = "none";
  }
});

/////////////////////////// GESTION DE LA DECONEXION   ////////////
document.getElementById("logout-link").addEventListener("click", () => {
  document.cookie = 'token=; Max-Age=0; path=/';


  window.location.href = "index.html";
});
