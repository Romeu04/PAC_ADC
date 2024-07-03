const overlay = document.getElementById('overlay');
const popup = document.getElementById('popup');
const closePopup = document.getElementById('closePopup');
const editStockBtn = document.getElementById('editStock');
const form = document.getElementById('popupForm');

editStockBtn.addEventListener('click', openPopup);
closePopup.addEventListener('click', closePopupFunction);
overlay.addEventListener('click', closePopupFunction);

//Função para abrir o popup
function openPopup() {
    overlay.classList.add('active');
    popup.classList.add('active');
}

//Função para fechar o popup
function closePopupFunction() {
    overlay.classList.remove('active');
    popup.classList.remove('active');
}

//Função para pegar todos os produtos
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

            const formattedPrice = product.precoProduto.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

            const productHTML = `
                <div class="product" data-id="${product.idProduto}">
                    <div class="photo">
                        <img src="/imagem_produto/${product.idProduto}" alt="Foto do Produto">
                    </div>
                    <div class="description">
                        <p>${product.nomeProduto}</p>
                        <p>${formattedPrice}</p>
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

//Função para adicionar um produto novo
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const nomeProduto = document.getElementById('productName').value;
        const precoProduto = document.getElementById('productPrice').value;
        const estoqueProduto = document.getElementById('productQuantity').value;
        const imagemProduto = document.getElementById('productImage').files[0];

        let formData = new FormData();
        formData.append('nomeProduto', nomeProduto);
        formData.append('estoqueProduto', estoqueProduto);
        formData.append('precoProduto', precoProduto);
        formData.append('imagemProduto', imagemProduto);

        fetch('/add_product', {
            method: 'POST',
            body: formData
        }).then(() => {
            form.reset();
            get_all_products();

            if (typeof closePopupFunction === 'function') {
                closePopupFunction();
            }
        }).catch(error => {
            console.error('Erro ao enviar o formulário: ', error);
        });
    });
});

//Função para atualizar o estoque
document.addEventListener('DOMContentLoaded', () => {
    const salvarEstoqueBtn = document.querySelector('.salvarEstoque');
    salvarEstoqueBtn.addEventListener('click', () => {
        const produtos = document.querySelectorAll('.product');
        const produtosAtualizados = Array.from(produtos).map(produto => {
            const produtoId = produto.getAttribute('data-id');
            const quantidadeAtualizada = parseInt(produto.querySelector('.quantity').textContent, 10);
            return { id: produtoId, quantidadeAtualizada };
        });

        produtosAtualizados.forEach(({ id, quantidadeAtualizada }) => {
            fetch('/update-stock', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ productId: id, newQuantity: quantidadeAtualizada }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Falha ao atualizar o estoque');
                }
            })
            .then(() => {
                console.log('Estoque atualizado com sucesso!');
                get_all_products();
            })
            .catch(error => {
                console.error('Erro ao atualizar o estoque', error);
            });
        });
    });
});

//Função para deletar um produto
function delete_product(productId) {
    fetch(`/delete-product/${productId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(() => {
        get_all_products();
    });
}

//chamada da função get_all_products para iniciar os produtos na tela
get_all_products();
