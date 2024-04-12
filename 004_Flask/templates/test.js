//alert("hello World LK!")
//alert("dfdfdfd")

//window.online =  function() {

//получает ссылку на элемент с id "zmina",
////используя метод document.getElementById(),
////и сохраняет его в переменную qqq.
////    qqq = document.getElementById("zmina");
//    qqq = document.getElementById("zmina");
//
////console.log() - это метод JavaScript, который используется для вывода информации
////в консоль разработчика вашего браузера. Он принимает аргументы,
////которые вы хотите вывести в консоль.
//    console.log(qqq);
//
////выражение qqq.innerHTML = "<h1> Hello world! </h1>";
////устанавливает HTML-содержимое элемента с id "zmina"
////равным "<h1> Hello world! </h1>", что приводит к появлению заголовка
////"Hello world!" внутри этого элемента при рендеринге страницы.
//    qqq.innerHTML = "<h1> Hello world! </h1>";
//}
window.onload = function() {
    let qqq = document.getElementById("zmina");
    let age = prompt("Сколько  тебе лет?");
    let years = age * 2;
    let result = "Число: "  + years;
    qqq.innerHTML = result;
}
