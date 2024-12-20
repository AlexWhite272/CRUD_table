//xhr.open('GET', 'http//localhost:8001/api/teachers', true)

// function createRequest(){
//     let request = false;

//     if (window.XMLHttpRequest){
//         //Gecko-совместимые браузеры, Safari, Konqueror
//         request = new XMLHttpRequest();
//     }else if (window.ActiveXObject){
//         //Internet explorer
//         try{
//             request = new ActiveXObject("Microsoft.XMLHTTP");
//         }    
//         catch (CatchException){
//             request = new ActiveXObject("Msxml2.XMLHTTP");
//         }
//     }
 
//     if (!request){
//         alert("Невозможно создать XMLHttpRequest");
//     }
    
//     return request;
// } 

// function httpRequest(httpMethod, url, jsonData){
//     let xhr = createRequest()
//     xhr.open(httpMethod, url, true)
//     // xhr.setRequestHeader("Access-Control-Allow-Origin", "*")
    
//     if(httpMethod == 'GET'){
//         xhr.send()
//     }
//     if(httpMethod == 'POST'){
//         xhr.setRequestHeader("Content-type", "application/json");
//         xhr.send(jsonData)
//     }
    
//     xhr.onreadystatechange = function() {
//         // Проверяем, был ли запрос успешным
//         if(this.readyState === 4) {
//             // Вставляем ответ от сервера в HTML-элемент
//             strJson = this.responseText
//             return JSON.parse(strJson);
//         }
//     };

    
// }



