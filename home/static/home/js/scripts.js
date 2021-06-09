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
