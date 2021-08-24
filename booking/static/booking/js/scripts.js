let csrfToken = $("[name=csrfmiddlewaretoken]").val();


$.fn.bookaDay = function(command, day, slot) {
  $.ajax({
    url: '/booking/modify',
    headers: {
           'X-CSRFToken': csrfToken
         },
    data: {
      child_id: childId,
      command: command,
      day: day
    },
    type: 'POST'
  })
  .done(function(response) {
    if (command === "full-day") {
      $(slot).removeClass("half-day");
      $(slot).addClass("full-day");
    } else if (command === "half-day") {
      $(slot).removeClass("full-day");
      $(slot).addClass("half-day");
    } else if (command === "cancel") {
      $(slot).removeClass("half-day full-day");
    }
    if (response['msg']) {
      $('#booking-msg').text(response['msg'])
      if ($('#booking-msg').hasClass('hidden')) {
        $('#booking-msg').toggleClass('hidden')
      }
      console.log(response['msg']);
    }
  });
}


$('.day').on('click', function(event) {
  var slot = $(this)
  var day = $(this).val();
  var command = $('input[name="day-option"]:checked').val();

  if (command === undefined) {
    alert("Dans l'onglet de gauche, sélectionnez Journée ou Demi-journée \
pour réserver une date. Ou Annuler pour annuler une réservation")
  } else {
    $.fn.bookaDay(command, day, slot);
  }
});


$('.calendar h2').on('click', function(event) {
  var month = $(this).parent().find('.month');
  month.toggle('slow')
});


$('.arrow').on('click', function(event) {
  $('.option').toggle('medium', function() {
    if ($('.option').is(":hidden")) {
      $('.arrow').html('<i class="fas fa-chevron-right fa-2x"></i>');
    } else {
      $('.arrow').html('<i class="fas fa-chevron-left fa-2x"></i>');
    }
  });
});
