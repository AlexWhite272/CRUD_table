
let globalWorkloads = {}
let globalGenders   = {}
let globalSubjects  = {}
let globalBackupRow 

//Создание объекта XMLHttpRequest
function createRequest(){
    let request = false;

    if (window.XMLHttpRequest){
        //Gecko-совместимые браузеры, Safari, Konqueror
        request = new XMLHttpRequest();
    }else if (window.ActiveXObject){
        //Internet explorer
        try{
            request = new ActiveXObject("Microsoft.XMLHTTP");
        }    
        catch (CatchException){
            request = new ActiveXObject("Msxml2.XMLHTTP");
        }
    }
 
    if (!request){
        alert("Невозможно создать XMLHttpRequest");
    }
    
    return request;
} 

// Создание запроса 
//
//httpMetthod   - строка - метод HTTP запроса (GET или POST)
//url           - строка - url хапроса
//jsonData      - объект - объект, который будет преобразован в JSON
function httpRequest(httpMethod, url, jsonData = undefined){
    return new Promise((resolve, reject)=>{
        let xhr = createRequest()
        xhr.open(httpMethod, url, true)

        xhr.onload = function() {

            if(this.status >= 400) {
                jsonData = JSON.parse(this.responseText)
                let error = new Error()
                error.code = this.status 
                error.message = jsonData.result
                console.log("Ошибка " + this.status)
                reject(error)

            } else {
                console.log("успех " + this.status)
                strJson = this.responseText
                resultObject = JSON.parse(strJson);
                resolve(resultObject)
            }
        };

        xhr.onerror = function() {
            reject(new Error("Network Error"));
        };

        if(httpMethod == 'GET'){
            xhr.send()
        }

        if(httpMethod == 'POST'){

            if(jsonData == undefined){
                return {
                    code: 400,
                    error: "No body request!"
                }
            }
            jsonData = JSON.stringify(jsonData)
            xhr.setRequestHeader("Content-type", "application/json");
            xhr.send(jsonData)
        }
    })
}

let arrayButton = document.body.getElementsByClassName("link_table_elem"); 
createListenElem(arrayButton, showDataTable)

// Вешает событие на переданный элемент

//   event   - string - событие
//   arrElem - array - массив элементов
//   action  - EventListenerOrEventListenerObject - функция, вызываемая при срабатывании события
function createListenElem(arrElem, action, event = "click"){
    for(item of arrElem){
        item.addEventListener(event, action);
    };
}

// Событие. Отправляет запрос на получение данных с сервера
// для заполнения таблицы
function showDataTable(event){
    if(event.srcElement.id === "nav_teachers"){
        httpRequest('GET', "http://127.0.0.1:5000/api/teachers")
            .then(
                response => createContentTable(response.result, "teachers"),
                error    => console.log(error)
            )
        
    }

    if(event.srcElement.id === "nav_students"){
        jsonData = httpRequest('GET', "http://127.0.0.1:5000/api/students")
        .then(
            response => createContentTable(response.result, "students"),
            error    => console.log(error)
        )
    }

    if(event.srcElement.id === "nav_classes"){
        jsonData = httpRequest('GET', "http://127.0.0.1:5000/api/classes")
        .then(
            response => createContentTable(response.result, "classes"),
            error    => console.log(error)
        )
    }

    httpRequest('GET', "http://127.0.0.1:5000/api/workloads")
        .then(
            response => globalWorkloads = structuredClone(response.result),
            error    => console.log(error)
        )
    httpRequest('GET', "http://127.0.0.1:5000/api/genders")
    .then(
        response => globalGenders = structuredClone(response.result),
        error    => console.log(error)
    )
    httpRequest('GET', "http://127.0.0.1:5000/api/subjects")
    .then(
        response => globalSubjects = structuredClone(response.result),
        error    => console.log(error)
    )
}

// Создает строку для редактирования данных
function editRowButton(event){
    globalBackupRow = event.target.parentElement.parentElement.cloneNode(true)
    let rowChildren = event.target.parentElement.parentElement.children 

    for (let element of rowChildren){
        if(element.className == "table_row_button" & element.firstChild.className == "table_button_edit"){
            element.innerHTML = ""

            let buttonConfirm = '<input class="table_button_confirm" type="image" src="source/confirm.ico" title="Сохранить" alt="Confitm"></input>'
            element.insertAdjacentHTML('beforeend', buttonConfirm)
            createListenElem([element.firstChild], confirmEditRow)
        }else if(element.className == "table_row_button" & element.firstChild.className == "table_button_delete"){
            element.innerHTML = ""

            let buttonCancel = '<input class="table_button_cancel" type="image" src="source/back.ico" title="Отменить" alt="Cancel"></input>'
            element.insertAdjacentHTML('beforeend', buttonCancel)
            // createListenElem([element.firstChild], (event)=>{backUpdateRow(event.target)}))
            element.firstChild.addEventListener("click", (event)=>{backUpdateRow(event.target.parentElement.parentElement.rowIndex)} )
        }
        if(element.className == "table_row_td"){
                editCell(element)
        }
        
    }


}

//Функция редактирования ячейки таблицы

//  target - object - ячейка таблицы
function editCell(target){
    let cellIndex = target.cellIndex
    let arrayHeaders = document.getElementsByClassName('table_header_td')
    let typeData = undefined
    
    for (let element of arrayHeaders){
        if(element.cellIndex == cellIndex){
            typeData = element.id
        }
    }

    if(typeData == "workloads"){
        let selectCell = document.createElement("select")
        selectCell.name = "workloads"
        
        for(let key in globalWorkloads){
            let optionSelect = document.createElement("option")
            optionSelect.value = key
            optionSelect.innerHTML = globalWorkloads[key]
            
            if(target.innerHTML == globalWorkloads[key]){
                optionSelect.selected = true
            }
            selectCell.append(optionSelect)
        }
        target.innerHTML = "";

        target.append(selectCell)

    }else if(typeData == "gender"){
        let selectCell = document.createElement("select")
        selectCell.name = "genders"
        
        for(let key in globalGenders){
            let optionSelect = document.createElement("option")
            optionSelect.value = key
            optionSelect.innerHTML = globalGenders[key]
            
            if(target.innerHTML == globalGenders[key]){
                optionSelect.selected = true
            }
            selectCell.append(optionSelect)
        }
        
        target.innerHTML = "";

        target.append(selectCell)

    }else if(typeData == "subject"){
        let selectCell = document.createElement("select")
        selectCell.name = "subjects"
        
        for(let key in globalSubjects){
            let optionSelect = document.createElement("option")
            optionSelect.value = key
            optionSelect.innerHTML = globalSubjects[key]
            
            if(target.innerHTML == globalSubjects[key]){
                optionSelect.selected = true
            }
            selectCell.append(optionSelect)
        }
        
        target.innerHTML = "";

        target.append(selectCell)

    }else if(typeData == "id" || typeData == "initials"){
        console.log("Колонку " + typeData + " редактировать запрещено")
    }else{
        let valueCell       = target.innerHTML;
        let inputCell       = document.createElement("input");
        inputCell.type      = "text";
        inputCell.value     = valueCell;
        inputCell.className = "input_cell_table";

        target.innerHTML = "";

        target.append(inputCell);

    }
    
    
}

// Собирает объект для передачи на сервера
function collectDataForCreate(row){
    let data_object     = {}
    let array_object    = []
    let dataServer      = { 
        "data_object": array_object
    }

    let arrayCell = row.children

    for(let cell of arrayCell){
        
        if(cell.className == "table_row_td"){
            let idHeader = getIdHeader(cell.cellIndex)
            if(idHeader == "id"){
                continue
            }else{
                if(cell.childElementCount == 0){
                    data_object[idHeader] = cell.innerHTML
                    continue
                }
                if(cell.firstElementChild.tagName == "SELECT"){
                    let value = cell.firstElementChild.selectedOptions[0].innerText
                    data_object[idHeader] = value
                }
                if(cell.firstElementChild.tagName == "INPUT"){
                    
                    data_object[idHeader] = cell.firstElementChild.value
                }
            }
        }        
    }

    array_object.push(data_object)
    
    return dataServer
}

// Собирает объект для передачи на сервера
function collectDataForUpdate(row){
    let new_values = {}
    let dataServer = { 
        "new_values": new_values
    }

    let arrayCell = row.children

    for(let cell of arrayCell){
        if(cell.className == "table_row_td"){
            let idHeader = getIdHeader(cell.cellIndex)
            if(idHeader == "id"){
                dataServer[idHeader] = cell.innerHTML
            }else{
                if(cell.childElementCount == 0){
                    new_values[idHeader] = cell.innerHTML
                    continue
                }
                if(cell.firstElementChild.tagName == "SELECT"){
                    let value = cell.firstElementChild.selectedOptions[0].innerText
                    new_values[idHeader] = value
                }
                if(cell.firstElementChild.tagName == "INPUT"){
                    
                    new_values[idHeader] = cell.firstElementChild.value
                }
            }
        }        
    }

    return dataServer
}

// Подтверждение обновление строки
// Отправляет запрос на сервер
function confirmEditRow(event){
    
    let url
    let row = event.target.parentElement.parentElement
    let countRow = row.rowIndex
    let dataServer
    
    if(row.id == "new_row"){
        url = "http://127.0.0.1:5000/api/" + document.getElementsByClassName("table")[0].id
        dataServer = collectDataForCreate(row)
    }else{
        url = "http://127.0.0.1:5000/api/update/" + document.getElementsByClassName("table")[0].id
        dataServer = collectDataForUpdate(row)
    }
    
    httpRequest('POST', url, dataServer)
        .then(
            response => updateRowTable(response.result, countRow),
            error    => backUpdateRow(countRow, error)
        )
}

// Отмена обновления строки
function backUpdateRow(countRow, error = undefined){
    let table     = document.body.getElementsByClassName("table")[0];

    if(table.rows[countRow].id == "new_row"){
        table.deleteRow(countRow)
        return
    }

    table.deleteRow(countRow)
    let row = table.rows[countRow -1]
    row.after(globalBackupRow)

    row = table.rows[countRow]

    let buttonEdit = row.getElementsByClassName("table_button_edit")
    createListenElem(buttonEdit, editRowButton)
    
    let buttonDelete = row.getElementsByClassName("table_button_delete")
    createListenElem(buttonDelete, deleteRowButton)

    if(error != undefined){
        alert(error.message)
    }
}

// Получить id колонки для ячейки
function getIdHeader(countCell){
    let arrayHeaders = document.getElementsByClassName('table_header_td')
    
    for (let element of arrayHeaders){
        if(element.cellIndex == countCell){
            return element.id
        }
    }
}

// Заполняет данными строку после ее обовления пользователем
function updateRowTable(data, countRow){
    let table     = document.body.getElementsByClassName("table")[0];
    table.deleteRow(countRow)

    data.forEach(objectData => {
        addRowTable(objectData, false, countRow)
    })
}

// Создает строку в таблице
function createNewRowTable(event){
    arrayCell       = []
    let table       = document.body.getElementsByClassName("table")[0]
    let row         = table.insertRow()
    row.id          = "new_row"
    row.className   = "table_body"

    let quantityCell = table.getElementsByClassName("table_header_td").length

    let buttonConfirm = '<td class="table_row_button"><input class="table_button_confirm" type="image" src="source/confirm.ico" title="Сохранить" alt="Confitm"></input></td>'
    row.insertAdjacentHTML('afterbegin', buttonConfirm)
    createListenElem([row.firstChild], confirmEditRow)

    for(let i=0; i < quantityCell; i++){
        let cell = row.insertCell()
        cell.className = "table_row_td"
        arrayCell.push(cell)
    }

    let buttonCancel = '<td class="table_row_button"><input class="table_button_cancel" type="image" src="source/back.ico" title="Отменить" alt="Cancel"></input></td>'
    row.insertAdjacentHTML('beforeend', buttonCancel)
    row.lastChild.addEventListener("click", (event)=>{backUpdateRow(event.target.parentElement.parentElement.rowIndex)} )
   
    arrayCell.forEach(cell => {editCell(cell)})
}

//Создает новую строку в текущей таблице
function addRowTable(data, newRow = false, countRow = undefined){
    let table = document.body.getElementsByClassName("table")[0]
    let row
    
    if(countRow != undefined){
        row   = table.insertRow()
    }else{
        row   = table.insertRow(countRow)
    }
     
    if(newRow){
        row.id = 'new_row'
    }else{
        row.id   = data.id
    }

    row.className   = "table_body"
    

    let buttonEdit  = '<td class="table_row_button"><input class="table_button_edit" type="image" src="source/edit.ico" title="Редактировать строку" alt="Delete"></td>'

    row.insertAdjacentHTML('beforeend', buttonEdit);
    createListenElem([row.firstChild.children[0]], editRowButton)
    
    for(let key in data){
        if(typeof(data[key]) != 'object' ){
            let cell = row.insertCell()
            cell.className = "table_row_td"
            cell.innerHTML = data[key]
        }
    }
   
    let textHTML  = '<td class="table_row_button"><input class="table_button_delete" type="image" src="source/delete.ico" title="Удалить строку" alt="Delete"></td>'

    row.insertAdjacentHTML('beforeend', textHTML)
    table.appendChild(row)
  
    createListenElem([row.lastChild.children[0]], deleteRowButton)
}

//Удаляет текущую строку в таблице

//  event - object - текущий объект с которым взаимодействовал пользователь
function deleteRowButton(event){
    let answer = confirm("Вы действительно хотите удалить данную строку?");
    if (answer){
        rowIndex = event.target.parentElement.parentElement.rowIndex
        let table       = document.body.getElementsByClassName("table")[0];
        table.deleteRow(rowIndex);
        
    }
}

//Создает таблицу
function createContentTable(data, id_table){
    
    let table = document.body.getElementsByClassName("table")[0];
    table.id = id_table
    table.innerHTML = ""
    createHeaderTable(data[0], table)
    


    data.forEach(objectData => {
        addRowTable(objectData)
    });
}

// Создает шапку таблицы
function createHeaderTable(data, table){

    let row = table.insertRow()
    row.className = "table_header"
    row.insertCell()

    for(let key in data){
        if(typeof(data[key]) != 'object' ){
            let cell = row.insertCell()
            cell.className = 'table_header_td'
            cell.innerHTML = key;
            cell.id = key;
            let textHTML  = '<input class="table_button_sort asc" type="image" title="Сортировать" src="source/sort.ico" alt="Sort"></input>'
            cell.insertAdjacentHTML('afterbegin', textHTML); 
            createListenElem([cell.firstChild], sortTable)
        }
    }

    let textHTML  = '<td class="table_row_button"><input class="table_button_create_row" type="image" title="Создать строку" src="source/add.ico" alt="Create"></td>'
    row.insertAdjacentHTML('beforeend', textHTML); 
    createListenElem([row.lastChild], createNewRowTable)
}

// Сортировка (убыв/возр) данных в таблице
function sortTable(event){
    let table       = document.body.getElementsByClassName("table")[0];
    let rows        = Array.from(table.rows)
    let arrayRows   = rows.slice(1)
    let index       = event.target.parentElement.cellIndex
    let order       = event.target.className.split(" ")[1]
    
    if(order == "desc"){
        //возрастание
        arrayRows.sort((rowA, rowB) => rowA.cells[index].innerHTML > rowB.cells[index].innerHTML ? 1 : -1);
        event.target.className = "table_button_sort asc"
    }

    if(order == "asc"){
        //убывание
        arrayRows.sort((rowA, rowB) => rowA.cells[index].innerHTML < rowB.cells[index].innerHTML ? 1 : -1);
        event.target.className = "table_button_sort desc"
    }
    
    table.tBodies[0].append(...arrayRows);
}