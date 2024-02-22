function changePicture(url) {

    var img = document.querySelector("#picture-container");
    img.setAttribute('src', url);
}


function reportUser(name) {

    var reportText = 'Você reportou ' + name + ' com sucesso!'
    alert(reportText)
}