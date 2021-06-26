let csrfToken = $("[name=csrfmiddlewaretoken]").val();


$.fn.bookaDay = function(dayOption, day, slot) {
  $.ajax({
    url: '/booking/modify',
    headers: {
           'X-CSRFToken': csrfToken
         },
    data: {
      child_id: childId,
      day_option: dayOption,
      day: day
    },
    type: 'POST'
  })
  .done(function(response) {
    if (dayOption === "full-day") {
      $(slot).removeClass("half-day");
      $(slot).addClass("full-day");
    } else if (dayOption === "half-day") {
      $(slot).removeClass("full-day");
      $(slot).addClass("half-day");
    } else if (dayOption === "cancel") {
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
  var dayOption = $('input[name="day-option"]:checked').val();

  if (dayOption === undefined) {
    alert('Sélectionnez Journée ou Demi-journée pour réserver une date. Ou Annuler pour annuler une réservation')
  } else {
    $.fn.bookaDay(dayOption, day, slot);
  }
});

$('.calendar h2').on('click', function(event) {
  var month = $(this).parent().find('.month');
  month.toggle('slow')
});
