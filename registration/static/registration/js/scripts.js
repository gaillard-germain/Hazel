let csrfToken = $("[name=csrfmiddlewaretoken]").val();


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


function deleteThis(item) {
  var thisId = $(item).val();
  if ($(item).hasClass('child')) {
    var thisKind = 'child'
  } else {
    var thisKind = 'adult'
  }
  if (confirm("êtes-vous sûrs de vouloir supprimer cet personne?")) {
    $.ajax({
      url: '/registration/delete_this',
      headers: {
             'X-CSRFToken': csrfToken
           },
      data: {
        this_id: thisId,
        this_kind: thisKind
      },
      type: 'POST'
    })
    .done(function(response) {
      location.reload();
    });
  }
}
