k// JavaScript for form validation
function validateForm() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();

    if (name === '' || email === '' || message === '') {
        alert('All fields are required.');
        return false;
    }

    return true;
}

// JavaScript for newsletter form validation
function validateNewsletterForm() {
    const newsletterEmail = document.getElementById('newsletter-email').value.trim();

    if (newsletterEmail === '') {
        alert('Email is required.');
        return false;
    }

    return true;
}

// JavaScript for back-to-top button
window.onscroll = function () {
    const backToTopButton = document.getElementById('back-to-top');
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        backToTopButton.style.display = 'block';
    } else {
        backToTopButton.style.display = 'none';
    }
};

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// JavaScript for carousel functionality
document.addEventListener('DOMContentLoaded', function () {
    const carouselInner = document.querySelector('.carousel-inner');
    const items = document.querySelectorAll('.carousel-item');
    let index = 0;

    function showNextSlide() {
        index = (index + 1) % items.length;
        updateCarousel();
    }

    function showPrevSlide() {
        index = (index - 1 + items.length) % items.length;
        updateCarousel();
    }

    function updateCarousel() {
        carouselInner.style.transform = `translateX(-${index * 100}%)`;
    }

    document.querySelector('.carousel-control-next').addEventListener('click', showNextSlide);
    document.querySelector('.carousel-control-prev').addEventListener('click', showPrevSlide);

    // Auto-slide every 5 seconds
    setInterval(showNextSlide, 5000);
});
