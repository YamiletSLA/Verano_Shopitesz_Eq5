function validarTarjetas(form){
    var cad=validartarjeta(form.numTarjeta.value);
    cad+=validarsaldo(form.saldo.value);
    var div=document.getElementById("notificaciones");
    if(cad!=''){
        div.innerHTML='<p>'+cad+'</p>';
        return false;
    }
    else{
        return true;
    }

}
function validartarjeta(tar){
        tar.length == 16
        if(tar.length==16){
            return '';
        }else{
            return 'El número de tarjeta debe ser de 16 digitos, <br>'
        }
    }


function validarsaldo(tar){
    if(tar<1){
        return 'La tarjeta debe tener un saldo mayor a 0';
    }
    else{
        return '';
    }
}