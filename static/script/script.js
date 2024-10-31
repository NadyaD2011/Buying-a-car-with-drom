const btn = document.querySelector('.button');
const cardLetter = document.querySelectorAll('.car_card').length;
let items = 5;

if (items >= cardLetter) {
    btn.style.display = 'none';
}

btn.addEventListener('click', () => {
    items += 4;
    const array = Array.from(document.querySelectorAll('.car_card'));
    const visItems = array.slice(0, items);

    visItems.forEach(el => el.classList.add('active'));

    if (visItems.length >= cardLetter) {
        btn.style.display = 'none';
    }
});
