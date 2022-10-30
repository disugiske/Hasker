function tag(value) {
  $.ajax({
      url: '/search/',
      method: 'POST',
      dataType: "json",
      headers: {'X-CSRFToken': Cookies.get('csrftoken')},
      data: {"tag": value},
      success: function(response) {
          window.history.pushState({}, "", '/search');

          const doc = document.getElementById('block');
          doc.innerHTML = response
            }
  })
}

window.addEventListener('popstate', function(event) {
          window.location.reload()
            }, false);