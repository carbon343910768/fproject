
function E_chk() {
    var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$");

    var email = document.getElementById("email").value;
    document.getElementById('email_errors').innerHTML = "";
    if(!reg.test(email)){
        document.getElementById('email_errors').innerHTML = "<font color='red'>enter a valid email address.</font>";
        return;
    }
    if(email===""){
        document.getElementById('email_errors').innerHTML = "<font color='red'>enter a valid email address.</font>";
        return;
    }
    document.forms[0].submit();
}

function P_chk() {
    var password1 = document.getElementById("password1").value;
    var password2 = document.getElementById("password2").value;

    document.getElementById('password2_error').innerHTML = "";
    document.getElementById('password1_error').innerHTML = "";

    if(password1!=password2){
        document.getElementById("password2_error").innerHTML = "<font color='red'>password mismatch.</font>";
        return;
    }
    if(password1.length<6){
        document.getElementById("password1_error").innerHTML = "<font color='red'>password too short.</font>";
        return;
    }
    document.forms[0].submit();
}