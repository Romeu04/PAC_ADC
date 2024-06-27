const overlay = document.getElementById('overlay');
const popup = document.getElementById('popup');
const closePopup = document.getElementById('closePopup');
const addMember = document.getElementById('addMember');
const form = document.getElementById('popupForm');
const members = document.getElementById('members');

addMember.addEventListener('click', () => openPopup());
closePopup.addEventListener('click', closePopupFunction);
overlay.addEventListener('click', closePopupFunction);

//Função para botão de editar membro
function buttonEfect() {
    document.getElementById('members').addEventListener('click', function(event) {
        if (event.target && event.target.classList.contains('editMember')) {
            const onclickAttribute = event.target.getAttribute('onclick');
            const memberId = onclickAttribute.match(/\d+/)[0];
            get_member(memberId);   
        }
    });
}

//Função para abrir o popup
function openPopup(id = null) {
    const deleteButton = document.getElementById('deleteButtonMember');
    form.reset();
    if (id && !deleteButton) {
        button = document.createElement('button');
        button.classList.add('buttons');
        button.innerText = 'Excluir Membro';
        button.setAttribute('onclick', `delete_member(${id})`);
        button.setAttribute('id', 'deleteButtonMember');
        form.appendChild(button);
    } else if (!id && deleteButton){
        form.removeChild(deleteButton);
    }
    overlay.classList.add('active');
    popup.classList.add('active');
    popupTitle.innerText = id ? 'Editar Membro' : 'Adicionar Membro';
}

//Função para fechar o popup
function closePopupFunction() {
    overlay.classList.remove('active');
    popup.classList.remove('active');
}

//Função para fechar o popup ao clicar no botão de submit
document.getElementById('popupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    closePopupFunction();
});

//Função para mostrar a senha
document.getElementById("showPassword").addEventListener("change", function() {
    var senhaInput = document.getElementById("memberPassword");
    if (this.checked) {
        senhaInput.type = "text";
    } else {
        senhaInput.type = "password";
    }
});

//Função para pegar todos os membros
const get_all_members = () => {
    fetch('/get_all_members')
    .then(response => response.json())
    .then(data => {
        members.innerHTML = '';
        data.forEach((member, index) => {

            const memberHTML = `
                <div class="member" data-id="${member.idMembros}">
                    <div class="photo">
                        <img src="/imagem_membro/${member.idMembros}" alt="Foto do Membro">
                    </div>
                    <div class="description">
                        <p>${member.nomeMembro} ${member.sobrenomeMembro}</p>
                        <p>Data de Nascimento: ${member.dataNascimento}</p>
                        <p>Email: ${member.emailLogin}</p>
                        <button id="editMember" class="buttons editMember" onclick="edit_member(${member.idMembros})">Editar Membro</button>
                    </div>
                </div>
            `;
            members.innerHTML += memberHTML;
        });
        buttonEfect();
    });
}

//Função para enviar o formulário e verificar se é para adicionar ou editar um membro
form.addEventListener('submit', function(event) {
    event.preventDefault();

    const idMember = form.querySelector('#memberId').value;

    //const idMember = document.getElementById('memberId').value;
    console.log(idMember);

    if (idMember) {
        edit_member(idMember);
    } else {
        add_member();
    }   
});

//Função para adicionar um membro
function add_member() {
    
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
}

//Função para buscar um membro
function get_member(idMember) {

    //Função para formatar a data
    function formatarData(dataISO) {
        const data = new Date(dataISO);
        const dia = data.getDate().toString().padStart(2, '0');
        const mes = (data.getMonth() + 1).toString().padStart(2, '0');
        const ano = data.getFullYear();
        return `${ano}-${mes}-${dia}`;
    }

    openPopup(idMember);
    
    fetch(`/get_member/${idMember}`, {
        method: 'GET'
    }).then(response => response.json())   
    .then(memberData => {

        document.getElementById('memberId').value = memberData.idMembros;
        document.getElementById('memberName').value = memberData.nomeMembro;
        document.getElementById('memberLastName').value = memberData.sobrenomeMembro;
        document.getElementById('memberDob').value = formatarData(memberData.dataNascimento);
        document.getElementById('memberLogin').value = memberData.emailLogin;
        document.getElementById('memberPassword').value = memberData.senhaLogin;
    });
}

//Função para editar um membro
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
        formData.append('idMember', idMember);
        formData.append('memberName', memberName);
        formData.append('memberLastName', memberLastName);
        formData.append('memberDob', memberDob);
        formData.append('memberImage', memberImage);
        formData.append('memberLogin', memberLogin);
        formData.append('memberPassword', memberPassword);

        fetch('/update_member', {
            method: 'PUT',
            body: formData
        }).then(() => {
            form.reset();
            get_all_members();
            document.getElementById('memberId').value = null;
            closePopupFunction();
        }).catch(error => {
            console.error('Erro ao enviar o formulário: ', error);
        });
    });
}

//Função para deletar um membro
function delete_member(idMember) {
    fetch(`/delete_member/${idMember}`, {
        method: 'DELETE'
    }).then(() => {
        closePopupFunction();
        window.location.reload();
    }).catch(error => {
        console.error('Erro ao deletar o membro: ', error);
    });
}

//Chamada da função para pegar todos os membros ao carregar a página
get_all_members();