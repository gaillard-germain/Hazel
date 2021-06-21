function dropDown() {
  document.getElementById("account").classList.toggle("show");
}


window.onclick = function(event) {
  if (!event.target.matches('.dropbtn, .dropbtn i, .dropbtn span')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}


function responsiveMenu() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}


window.onscroll = function() {stickyHeader()};

var header = document.getElementById("home-header");

var sticky = header.offsetTop;


function stickyHeader() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
}


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


function toggleAgenda(item) {
  var all = document.getElementsByClassName("container");
  for (i = 0; i < all.length; i++) {
    if (all[i].classList.contains(item.innerHTML)) {
      all[i].classList.toggle("hidden");
    } else {
      all[i].classList.add("hidden");
    }
  }
}
