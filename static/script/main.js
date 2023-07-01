function getParameters(){
    let url = new URL((window.location.href).toLowerCase());
    result = {};
    [...url.searchParams.keys()].forEach(key => {
        result[key] = url.searchParams.get(key);
    });
    return result;
}

function renderInto(items, elementName, render, tag="div"){
    const element = document.querySelector(elementName);
    element.innerHTML = '';
    items.forEach(item => {
        const child = document.createElement(tag);
        child.innerHTML = render(item);
        element.appendChild(child);
    });
}

function getMoment(epoch){
    epoch = (Date.now()/1000) - epoch;
    let result = 'Justo ahora';
    const interval = [
        [60, "minuto"],
        [60, "hora"],
        [24, "dia"],
        [7, "semana"],
        [52, "año"]
    ];
    for(let i of interval){
        if(epoch > i[0]){
            epoch = parseInt(epoch / i[0]);
            result = "Hace " + epoch + " " + i[1]
            if (epoch > 1){
                result += "s";
            }
        }else{
            break;
        }
    }
    return result;
}