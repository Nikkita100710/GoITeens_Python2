// Отримуємо посилання на кнопку "Login"
let submitButton = document.getElementById("submitButton");

// Додаємо обробник події кліку по кнопці
submitButton.addEventListener("click", function() {
    // Отримуємо значення з полів вводу
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;


    // Вивод введених даних
    alert("Ваше ім'я користувача: " + username + "\nYour password: " + password);
});
