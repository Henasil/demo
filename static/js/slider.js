document.addEventListener('DOMContentLoaded', () => {
    const slider = document.querySelector('.slider');
    if (!slider) {
        return;
    }

    const slides = Array.from(slider.querySelectorAll('.slide'));
    const prev = slider.querySelector('.slider-prev');
    const next = slider.querySelector('.slider-next');
    let current = 0;
    let timerId = null;

    function showSlide(index) {
        slides[current].classList.remove('is-active');
        current = (index + slides.length) % slides.length;
        slides[current].classList.add('is-active');
    }
// автоплей
    function restartTimer() {
        clearInterval(timerId);
        timerId = setInterval(() => showSlide(current + 1), 3000);
    }
// кнопки для перелистывания 
    prev.addEventListener('click', () => {
        showSlide(current - 1);
        restartTimer();
    });

    next.addEventListener('click', () => {
        showSlide(current + 1);
        restartTimer();
    });

    restartTimer();
});
