document.addEventListener('DOMContentLoaded', function() {
    const expandButton = document.querySelector('.icon-button.expand');
    const collapseSection = document.querySelector('.collapse');

    expandButton.addEventListener('click', function() {
        const expanded = expandButton.getAttribute('aria-expanded') === 'true' || false;
        expandButton.setAttribute('aria-expanded', !expanded);
        collapseSection.classList.toggle('show');
    });
});
