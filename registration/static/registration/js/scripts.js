function validate() {
  var regFamilyBtn = document.getElementById("register-family");
  var agreements = document.getElementsByName("agreement");
  var validated = 0;

  for (i = 0; i < agreements.length; i++) {
    if (agreements[i].checked) {
      validated++;
    }
  }

  if (validated === agreements.length) {
    regFamilyBtn.disabled = false;
  } else {
    regFamilyBtn.disabled = true;
  }
}
