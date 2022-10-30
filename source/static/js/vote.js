function vote(vote_id, direct, from) {
  const csrftoken = Cookies.get('csrftoken');
  jQuery.ajax({
		url: '/vote',
		method: 'POST',
		dataType: 'json',
	  	headers: {'X-CSRFToken': csrftoken},
	  	data: {
			[direct]: 1,
			"vote_id": vote_id,
			"method": from,
		},
	  	success: function (rating) {
		if (rating.rating === "err"){
			alert("No-no-no")
			return;
		}
		let count = document.querySelector('#vote'+vote_id+from);
		count.textContent = rating.rating;
  		},
	  	error: function (){
			alert("Server error")
		}
	  }
  );

}

function best(comment_id) {
	const csrftoken = Cookies.get('csrftoken');
	jQuery.ajax({
		url: '/best/',
		method: 'POST',
		dataType: 'json',
		headers: {'X-CSRFToken': csrftoken},
		data: {"comment_id": comment_id},
		success: function (request){
			if(request.best_old === 0){
				return
			}
			let bestold = document.querySelector('#best'+request.best_old);
			bestold.style.color = 'gray';
			bestold.style.fontSize = '35px';
			let best = document.querySelector('#best'+comment_id);
			best.style.color = 'green';
			best.style.fontSize = '45px';
		},
		error: function (){
			let best = document.querySelector('#best'+comment_id);
			best.style.color = 'gray';
			alert('Server error')
		}
	})
}