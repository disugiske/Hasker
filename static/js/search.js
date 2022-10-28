$(document).ready(function() {
  $('#searchform').on('submit', function (e) {
    e.preventDefault();
    const search= $('#search').val()
    if (search.slice(0,4) === 'tag:'){
      var val = search.slice(4)
      var key = 'tag'
    }
    else {
      var key = 'search'
      var val = search
    }
    $.ajax({
      url: '/search/',
      method: 'POST',
      dataType: 'json',
      headers: {'X-CSRFToken': Cookies.get('csrftoken')},
      data: {[key]: val},
      success: function(response) {
          window.history.pushState({}, "", '/search');
          const doc = document.getElementById('block');
          doc.innerHTML = response
          }
    })
  })
});

window.addEventListener('popstate', function(event) {
          window.location.reload()
            }, false);