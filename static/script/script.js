const btn = document.querySelector('.button');
const cardLetter = document.querySelectorAll('.car_card').length;
let items = 5;

btn.addEventListener('click', () => {
    items += 5;
    const array = Array.from(document.querySelector('cards_car').children);
    const visItems = array.slice(0, items);

    visItems.forEach(el => el.classList.add('active'));

    if (visItems.length === cardLetter) {
        btn.style.display == 'none';
    }
});