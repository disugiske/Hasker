function img(value) {
  $.ajax({
      url: '/search/',
      method: 'POST',
      dataType: "json",
      headers: {'X-CSRFToken': Cookies.get('csrftoken')},
      data: {"tag": value},
      success: function(response) {
          window.history.pushState({}, "", '/search/tag/'+value);

          const doc = document.getElementById('block');
          doc.innerHTML = response
            },
      error: function (response) {
          window.location.replace('/auth/?next=/')
      }
  })
}