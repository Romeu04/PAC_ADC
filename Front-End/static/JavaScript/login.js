document.getElementById("showPassword").addEventListener("change", function() {
    var senhaInput = document.getElementById("senha");
    if (this.checked) {
        senhaInput.type = "text";
    } else {
        senhaInput.type = "password";
    }
});

document.getElementById("loginButton").addEventListener("click", function() {
    window.location.href = "agenda.html";
});