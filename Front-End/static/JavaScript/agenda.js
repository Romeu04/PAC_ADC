document.getElementById("editButton").addEventListener("click", function() {
    document.getElementById("overlay").classList.add("active");
});

document.getElementById("closePopup").addEventListener("click", function() {
    document.getElementById("overlay").classList.remove("active");
});
