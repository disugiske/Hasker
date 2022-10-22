function vote_post_up(comment_id) {
  jQuery.ajax({
		url: '/vote_post',
		method: 'POST',
		dataType: 'json',
	  	// headers: {'X-CSRFToken': csrftoken},
	  	data: {"up": 1, "comment_id": comment_id},
	    success: setTimeout(function(){ location.reload(); }, 200),
	});
}

function vote_post_down(comment_id) {
  	$.ajax({
		url: '/vote_comment',
		method: 'POST',
		dataType: 'json',
	  	// headers: {'X-CSRFToken': csrftoken},
	  	data: {"down": 1, "comment_id": comment_id},
		success: setTimeout(function(){ location.reload(); }, 200),
	});
}