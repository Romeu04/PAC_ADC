const overlay = document.getElementById('overlay');
const popup = document.getElementById('popup');
const closePopup = document.getElementById('closePopup');
const addMember = document.getElementById('addMember');
const form = document.getElementById('popupForm');

addMember.addEventListener('click', () => openPopup('Adicionar Membro'));
closePopup.addEventListener('click', closePopupFunction);
overlay.addEventListener('click', closePopupFunction);

//Função para abrir o popup
function openPopup(action) {
    overlay.classList.add('active');
    popup.classList.add('active');
    popupTitle.innerText = action;
}

//Função para fechar o popup
function closePopupFunction() {
    overlay.classList.remove('active');
    popup.classList.remove('active');
}

//Função para pegar todos os membros
const get_all_members = () => {
    fetch('/get_all_members')
    .then(response => response.json())
    .then(data => {
        const members = document.getElementById('members');
        members.innerHTML = '';
        data.forEach((member, index) => {
            let editButtonHTML = `<button id="editMember" class="buttons" onclick="edit_member(${member.idMembros})">Editar Membro</button>`; // Ajuste conforme necessário

            const memberHTML = `
                <div class="member" data-id="${member.idMembros}">
                    <div class="photo">
                        <img src="/imagem_membro/${member.idMembros}" alt="Foto do Membro">
                    </div>
                    <div class="description">
                        <p>${member.nomeMembro} ${member.sobrenomeMembro}</p>
                        <p>Data de Nascimento: ${member.dataNascimento}</p>
                        <p>Email: ${member.emailLogin}</p>
                        ${editButtonHTML}
                    </div>
                </div>
            `;
            members.innerHTML += memberHTML;
        });
    });
}

//Função para adicionar um membro
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const memberName = document.getElementById('memberName').value;
        const memberLastName = document.getElementById('memberLastName').value;
        const memberDob = document.getElementById('memberDob').value;
        const memberImage = document.getElementById('memberImage').files[0];
        const memberLogin = document.getElementById('memberLogin').value;
        const memberPassword = document.getElementById('memberPassword').value;

        let formData = new FormData();
        formData.append('memberName', memberName);
        formData.append('memberLastName', memberLastName);
        formData.append('memberDob', memberDob);
        formData.append('memberImage', memberImage);
        formData.append('memberLogin', memberLogin);
        formData.append('memberPassword', memberPassword);

        fetch('/add_member', {
            method: 'POST',
            body: formData
        }).then(() => {
            form.reset();
            get_all_members();
            closePopupFunction();

        }).catch(error => {
            console.error('Erro ao enviar o formulário: ', error);
        });
    });
});

//tentativa de separar as funções
function add_member() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const memberName = document.getElementById('memberName').value;
        const memberLastName = document.getElementById('memberLastName').value;
        const memberDob = document.getElementById('memberDob').value;
        const memberImage = document.getElementById('memberImage').files[0];
        const memberLogin = document.getElementById('memberLogin').value;
        const memberPassword = document.getElementById('memberPassword').value;

        let formData = new FormData();
        formData.append('memberName', memberName);
        formData.append('memberLastName', memberLastName);
        formData.append('memberDob', memberDob);
        formData.append('memberImage', memberImage);
        formData.append('memberLogin', memberLogin);
        formData.append('memberPassword', memberPassword);

        fetch('/add_member', {
            method: 'POST',
            body: formData
        }).then(() => {
            form.reset();
            get_all_members();
            closePopupFunction();

        }).catch(error => {
            console.error('Erro ao enviar o formulário: ', error);
        });
    });

}

//Função para editar um membro
function get_member(idMember) {

    openPopup('Editar Membro');
    
    fetch(`/get_member/${idMember}`, {
        method: 'GET'
    }).then(response => response.json())   
    .then(memberData => {
        
        document.getElementById('memberName').value = memberData.nomeMembro;
        document.getElementById('memberLastName').value = memberData.sobrenomeMembro;
        document.getElementById('memberDob').value = memberData.dataNascimento;
        document.getElementById('memberLogin').value = memberData.emailLogin;
    });
}

function edit_member(idMember) {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const memberName = document.getElementById('memberName').value;
        const memberLastName = document.getElementById('memberLastName').value;
        const memberDob = document.getElementById('memberDob').value;
        const memberImage = document.getElementById('memberImage').files[0];
        const memberLogin = document.getElementById('memberLogin').value;
        const memberPassword = document.getElementById('memberPassword').value;

        let formData = new FormData();
        formData.append('memberName', memberName);
        formData.append('memberLastName', memberLastName);
        formData.append('memberDob', memberDob);
        formData.append('memberImage', memberImage);
        formData.append('memberLogin', memberLogin);
        formData.append('memberPassword', memberPassword);

        fetch('/update_member', {
            method: 'POST',
            body: formData
        }).then(() => {
            form.reset();
            get_all_members();
            closePopupFunction();

        }).catch(error => {
            console.error('Erro ao enviar o formulário: ', error);
        });
    });
}

document.getElementById('popupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    closePopupFunction();
});

get_all_members();