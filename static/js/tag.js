function tag(value) {
  jQuery.ajax({
      url: '/search/',
      method: 'POST',
      dataType: 'json',
      headers: {'X-CSRFToken': Cookies.get('csrftoken')},
      data: {"tag": value},
      success: function(response) {
          console.log(response)
          const doc = document.getElementById('block');
          doc.innerHTML = response
          }
  })
}
