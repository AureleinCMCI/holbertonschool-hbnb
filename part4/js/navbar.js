$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    console.log("Clicked menu");
    $("#mainListDiv").toggleClass("show_list");
    $("#mainListDiv").fadeIn();

});
// Si tu veux un contrôle JavaScript supplémentaire pour l'animation du texte
$(document).ready(function() {
    const scrollingText = $(".scrolling-text");
    let textContent = scrollingText.text();
    let fullText = textContent + " ";  // Ajoute un espace à la fin pour un effet fluide
    scrollingText.text(fullText);

    function animateText() {
        scrollingText.animate({
            left: '100%'
        }, 10000, 'linear', function() {
            $(this).css("left", "-100%"); // Réinitialise la position pour recommencer l'animation
            animateText(); // Redémarre l'animation
        });
    }

    animateText(); // Démarre l'animation lorsque la page est prête
});
