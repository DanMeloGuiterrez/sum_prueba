const passwordInput = document.getElementById('contrasena'),
      togglePassword = document.querySelector('#togglePassword');

togglePassword.addEventListener('click', e=>{
    if (passwordInput.type === "password"){
        passwordInput.type = "text";
        togglePassword.classList.remove('bx-eye');
        togglePassword.classList.add('bx-eye-slash');
    } else {
        passwordInput.type = "password"
        togglePassword.classList.add('bx-eye');
        togglePassword.classList.remove('bx-eye-slash');
    }
})
