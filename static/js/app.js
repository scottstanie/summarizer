$(document).ready(function() {
  $('#submit-summary').on('click', function() {
    var url = $('#input-url').val();
    var summarizer = $('#summarizer').val();
    console.log(summarizer);
    console.log(url);
    $.ajax({
      type: 'POST',
      url: '/summarize',
      data: JSON.stringify({
        url: url,
        summarizer: summarizer
      }),
      contentType: 'application/json',
      dataType: 'json',
      success: function(data) {
        console.log(data);
        $('#summary').empty();
        var summaryText = 'hey';
        for (var i=0; i < data.length; i++) {
          $('#summary').append('<p>' + data[i] + '</p>');
        };
      },
      error: function(data) {
        console.log('Error');
        console.log(data);
      },
  });

  })
})
