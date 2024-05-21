function isExistEmail(email1, email2) {
    if (email1 == email2) {
        return true;
    }
    return false;
}

function isCorrectPassword(password1, password2) {
    if (password1 == password2) {
        return true;
    }
    return false;
}

function isValidLogin() {
    let email = document.getElementById('email');
    let password = document.getElementById('password');
    // Clear previous error messages
    document.querySelectorAll('.error').forEach(function (error) {
        error.remove();
        canSubmit = true;
    });
    if (isExistEmail(email.value, '123@gmail.com')) {
        if (isCorrectPassword(password.value, '123')) {
            return true;
        }
        password.insertAdjacentHTML('afterend', '<div class="error">密碼錯誤</div>');
        return false;
    }
    email.insertAdjacentHTML('afterend', '<div class="error">email不存在</div>');
    return false;
}

document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();
    if (isValidLogin()) {
        alert("登入成功！");
        this.submit();
    } else {
        return;
    }
});