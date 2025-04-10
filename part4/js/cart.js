document.addEventListener('DOMContentLoaded', function () {
    const cartItemsList = document.getElementById('cart-list');
    const cartCount = document.getElementById('cart-count');
    const cartTotal = document.getElementById('cart-total');
    let cart = [];

    function getUserIdFromSession() {
        return localStorage.getItem('user_id');
    }

    function loadCartFromStorage() {
        const userId = getUserIdFromSession();
        if (!userId) {
            cartItemsList.innerHTML = '<p>Vous devez être connecté pour voir votre panier.</p>';
            return;
        }

        const storedCart = localStorage.getItem(`cart_${userId}`);
        if (storedCart) {
            cart = JSON.parse(storedCart);
            updateCartDisplay();
        } else {
            cartItemsList.innerHTML = '<p>Votre panier est vide.</p>';
        }
    }

    function updateCartDisplay() {
        cartItemsList.innerHTML = '';
        let total = 0;

        cart.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `${item.title} - $${item.price}`;
            cartItemsList.appendChild(li);
            total += item.price;
        });

        cartCount.textContent = cart.length;
        cartTotal.textContent = `$${total}`;
    }

    loadCartFromStorage();
});
function updateCartDisplay() {
    cartItemsList.innerHTML = '';
    let total = 0;

    cart.forEach(item => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            <div>
                <h6 class="my-0">${item.title}</h6>
                <small class="text-muted">${item.description || 'Aucun détail'}</small>
            </div>
            <span class="text-primary fw-bold">$${item.price}</span>
        `;
        cartItemsList.appendChild(li);
        total += item.price;
    });

    cartCount.textContent = cart.length;
    cartTotal.textContent = `$${total}`;
}
