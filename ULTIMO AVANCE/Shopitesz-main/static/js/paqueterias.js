function imprimirMsg(){
    alert('Se hizo click');
}

function validar(form){
    var cad=validarPassword(form.password.value);
    cad+=passwordRobusto(form.password.value,form.password.value);
    cad+=validarPasswords(form.password.value,form.passwordConfirmacion.value)
    cad+=validarTelefono(form.telefono.value);
    var div=document.getElementById("notificaciones");
    if(cad!=''){
        div.innerHTML='<p>'+cad+'</p>';
        return false;
    }
    else{
        return true;
    }

}
function validarTelefono(cadena){
    var patron=/\d{3}-\d{3}-\d{4}/;
    if(patron.test(cadena)==true){
        return '';
    }
    else{
        return 'El número de telefo debe tener el siguiente formato: ###-###-####';
    }
}