function isValidForm() {
    let canSubmit = true;
    let id = document.getElementById('id');
    let email = document.getElementById('email');
    let password = document.getElementById('password');
    let confirm_password = document.getElementById('confirm_password');

    // Clear previous error messages
    document.querySelectorAll('.error').forEach(function(error) {
        error.remove();
        canSubmit = true;
    });

    if (!/^[a-zA-Z0-9]+$/.test(id.value)) {
        id.insertAdjacentHTML('afterend', '<div class="error">只能輸入英文或數字，請重新輸入</div>');
        canSubmit = false;
    }

    if (!/^\S+@\S+\.\S+$/.test(email.value)) {
        email.insertAdjacentHTML('afterend', '<div class="error">格式錯誤，請重新輸入</div>');
        canSubmit = false;
    }

    if (!/[A-Z]/.test(password.value) || !/[a-z]/.test(password.value) || !/\d/.test(password.value) || password.value.length < 6) {
        if (!/[A-Z]/.test(password.value)) password.insertAdjacentHTML('afterend', '<div class="error">請輸入至少一個大寫英文</div>');
        if (!/[a-z]/.test(password.value)) password.insertAdjacentHTML('afterend', '<div class="error">請輸入至少一個小寫英文</div>');
        if (!/\d/.test(password.value)) password.insertAdjacentHTML('afterend', '<div class="error">請輸入至少一個數字</div>');
        if (password.value.length < 6) password.insertAdjacentHTML('afterend', '<div class="error">請輸入大於6個字</div>');
        canSubmit = false;
    }

    if (password.value !== confirm_password.value) {
        confirm_password.insertAdjacentHTML('afterend', '<div class="error">與password不同，請重新確認</div>');
        confirm_password.value = "";
        canSubmit = false;
    }

    return canSubmit;
}
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    if(isValidForm()){
        alert("註冊成功！");
        this.submit();
    }else{
        return;
    }
});