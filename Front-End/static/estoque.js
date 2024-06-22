const overlay = document.getElementById('overlay');
const popup = document.getElementById('popup');
const closePopup = document.getElementById('closePopup');
const editStockBtn = document.getElementById('editStock');

function openPopup() {
    overlay.classList.add('active');
    popup.classList.add('active');
}

function closePopupFunction() {
    overlay.classList.remove('active');
    popup.classList.remove('active');
}

editStockBtn.addEventListener('click', openPopup);
closePopup.addEventListener('click', closePopupFunction);
overlay.addEventListener('click', closePopupFunction);

const form = document.getElementById('popupForm')
const sendForm = () => {
const nomeProduto = document.getElementById('productName').value;
 const precoProduto = document.getElementById('productPrice').value;
 const estoqueProduto = document.getElementById('productQuantity').value;

let formData = new FormData();
formData.append('nomeProduto', nomeProduto);
formData.append('estoqueProduto', estoqueProduto);
formData.append('precoProduto', precoProduto);

fetch('/add_product', {
    method: 'POST',
    body: formData
})

}
form.addEventListener('submit', function(event) {
    event.preventDefault();
    sendForm();
    get_all_products();
    closePopupFunction();
});

const get_all_products = () => {
    fetch('/get_all_products')
    .then(response => response.json())
    .then(data => {
        const products = document.getElementById('products');
        products.innerHTML = '';
        data.forEach(product => {
            products.innerHTML += `
            <div class="product">
                    <div class="photo">
                        <img src="camisa.png" alt="Camisa Atlética Unissex">
                    </div>
                    <div class="description">
                        <p>${product.nomeProduto}</p>
                        <p>${product.precoProduto}</p>
                        <div class="quantity-control">
                            <button class="quantity-button">-</button>
                            <span class="quantity">${product.estoqueProduto}</span>
                            <button class="quantity-button">+</button>
                        </div>
                    </div>
                </div>
            `
        })
    })
}

get_all_products();