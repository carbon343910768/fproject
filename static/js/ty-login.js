
  function onemail() {
      var re=/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
      var email=document.getElementById("id_email").value;
      var pwd=document.getElementById("id_password").value;
      var pwd2=document.getElementById("id_password_confirmation").value;
      if(re.test(email)!=true && email.length!=0) {
          var obj = document.getElementById("error");
          obj.innerText= "Invalid email!";
          return false;
      }
      else if(pwd.length<6){
          var obj = document.getElementById("error");
          obj.innerText= "Password too short (6 chars. min)";
          return false;
      }
      else if(pwd!=pwd2){
           var obj = document.getElementById("error");
          obj.innerText= "Password mismatach!";
          return false;
      }
  }