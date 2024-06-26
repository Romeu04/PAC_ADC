const overlay = document.getElementById('overlay');
const popup = document.getElementById('popup');
const closePopup = document.getElementById('closePopup');
const popupTitle = document.getElementById('popupTitle');
const addMemberBtn = document.getElementById('addMember');
const removeMemberBtn = document.getElementById('removeMember');
const editMemberBtn = document.getElementById('editMember');

function openPopup(action) {
    overlay.classList.add('active');
    popup.classList.add('active');
    popupTitle.innerText = action;
}

function closePopupFunction() {
    overlay.classList.remove('active');
    popup.classList.remove('active');
}

addMemberBtn.addEventListener('click', () => openPopup('Adicionar novo membro'));
removeMemberBtn.addEventListener('click', () => openPopup('Remover membro'));
editMemberBtn.addEventListener('click', () => openPopup('Editar membro'));
closePopup.addEventListener('click', closePopupFunction);
overlay.addEventListener('click', closePopupFunction);

document.getElementById('popupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    closePopupFunction();
});