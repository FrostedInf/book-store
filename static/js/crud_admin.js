$(document).ready(function() {
	var	$identificador;
	var $valor;
	var $token;
	$("button").click(function(event) {
		$identificador =  $(this).parents('tr');
		$valor = $(this).val();
		$token = $("input").val();
		console.log($token);

		if ($valor == 'deleteBook') {
			$.ajax({
			url: '/admin/delete_books/' + $identificador.attr('data-book'),
			type: 'POST',
			beforeSend: function(xhr) {
	        		xhr.setRequestHeader("X-CSRFToken", $token);
	    		}
			})
			.done(function() {
				console.log("success");
				$identificador.remove();
			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});

		}


		if ($valor == 'deleteUser') {
			$.ajax({
			url: '/admin/delete_users/' + $identificador.attr('data-usuario'),
			type: 'POST',
			beforeSend: function(xhr) {
	        		xhr.setRequestHeader("X-CSRFToken", $token );
	    		}
			})
			.done(function() {
				console.log("success");
				$identificador.remove();
			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});

		}

		});



	
			
});