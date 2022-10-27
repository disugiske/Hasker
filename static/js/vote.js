function vote(vote_id, direct, from) {
  const csrftoken = Cookies.get('csrftoken');
  jQuery.ajax({
		url: '/vote_comment',
		method: 'POST',
		dataType: 'json',
	  	headers: {'X-CSRFToken': csrftoken},
	  	data: {
			[direct]: 1,
			"vote_id": vote_id,
			"method": from,
		},
	}).done(function (rating) {
		if (rating.rating === "err"){
			alert("No-no-no")
			return;
		}
		if (rating.rating === "500"){
			alert("Server error, try later")
			return;
		}
		let count = document.querySelector('#vote'+vote_id+from);
		count.textContent = rating.rating;
  });

}

