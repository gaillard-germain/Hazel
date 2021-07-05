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
      console.log(response['msg']);
    }
  });
}


$('.day').on('click', function(event) {
  var slot = $(this)
  var day = $(this).val();
  var command = $('input[name="day-option"]:checked').val();

  if (command === undefined) {
    alert('Sélectionnez Journée ou Demi-journée pour réserver une date. Ou Annuler pour annuler une réservation')
  } else {
    $.fn.bookaDay(command, day, slot);
  }
});

$('.calendar h2').on('click', function(event) {
  var month = $(this).parent().find('.month');
  month.toggle('slow')
});
