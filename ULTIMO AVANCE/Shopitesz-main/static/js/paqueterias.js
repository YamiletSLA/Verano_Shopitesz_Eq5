
function validar(form){
    var cad=validarPassword(form.tel.value);
    cad+=validarTelefono(form.tel.value);
    var div=document.getElementById("notificaciones");
    if(cad!=''){
        div.innerHTML='<p>'+cad+'</p>';
        return false;
    }
    else{
        return true;
    }

}
function validarTelefono(form){
    var patron=/\d{3}-\d{3}-\d{4}/;
    if(patron.test(cadena)==true){
        return '';
    }
    else{
        return 'El número de telefo debe tener el siguiente formato: ###-###-####';
    }
}