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
    const imagemProduto = document.getElementById('productImage').files[0]; // Obter o arquivo de imagem

    let formData = new FormData();
    formData.append('nomeProduto', nomeProduto);
    formData.append('estoqueProduto', estoqueProduto);
    formData.append('precoProduto', precoProduto);
    formData.append('imagemProduto', imagemProduto); 

    console.log(imagemProduto);

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
        data.forEach((product, index) => {
            let removeButtonHTML = '';

            if (product.estoqueProduto === 0) {
                removeButtonHTML = `<button class="remove-button" onclick="delete_product(${product.idProduto})">Remover Produto</button>`;
            }
        
            const productHTML = `
                <div class="product" data-id="${product.idProduto}">
                    <div class="photo">
                        <img src="/images/${product.idProduto}" alt="Foto do Produto">
                    </div>
                    <div class="description">
                        <p>${product.nomeProduto}</p>
                        <p>${product.precoProduto}</p>
                        <div class="quantity-control">
                            <button class="quantity-button" id="decrease-${index}">-</button>
                            <span class="quantity" id="quantity-${index}">${product.estoqueProduto}</span>
                            <button class="quantity-button" id="increase-${index}">+</button>
                        </div>
                        ${removeButtonHTML}
                    </div>
                </div>
            `;
            products.innerHTML += productHTML;
        });

        data.forEach((product, index) => {
            document.getElementById(`decrease-${index}`).addEventListener('click', () => {
                const quantitySpan = document.getElementById(`quantity-${index}`);
                let quantity = parseInt(quantitySpan.textContent, 10);
                if (quantity > 0) {
                    quantitySpan.textContent = --quantity;
                }
            });

            document.getElementById(`increase-${index}`).addEventListener('click', () => {
                const quantitySpan = document.getElementById(`quantity-${index}`);
                let quantity = parseInt(quantitySpan.textContent, 10);
                quantitySpan.textContent = ++quantity;
            });
        });
    });
}

get_all_products();

document.addEventListener('DOMContentLoaded', () => {
    const salvarEstoqueBtn = document.querySelector('.salvarEstoque');
    salvarEstoqueBtn.addEventListener('click', () => {
        const produtosAtualizados = coletarDadosAtualizados();

        produtosAtualizados.forEach(produto => {
            update_product_stock(produto.id, produto.quantidadeAtualizada)
            .then(response => {
                console.log('Estoque atualizado com sucesso!', response);
            })
            .catch(error => {
                console.error('Erro ao atualizar o estoque', error);
            });
        });
    });
});

function coletarDadosAtualizados() {
    const produtosAtualizados = [];
    const produtos = document.querySelectorAll('.product');

    produtos.forEach((produto) => {
        const produtoId = produto.getAttribute('data-id');
        const quantidadeAtualizada = parseInt(produto.querySelector('.quantity').textContent, 10);

        produtosAtualizados.push({
            id: produtoId,
            quantidadeAtualizada
        });
    });

    return produtosAtualizados;
}

function update_product_stock(productId, newQuantity) {

    const request = fetch('/update-stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ productId, newQuantity }),
    });
    get_all_products();
    return request
}

function delete_product(productId) {
    fetch(`/delete-product/${productId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    get_all_products();
}