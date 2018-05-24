$(document).ready(function() {
	var	$identificador;
	var $valor;
	var $token;
	$("button").click(function(event) {
		$identificador =  $(this).parents('tr');
		$valor = $(this).val();
		$token = $("input").val();
		console.log($token);
		//libros
			if ($valor == 'showBook') {
				$("#showModalBook").modal();
				showBook($identificador, $token);
			}

			
			if ($valor == 'deleteBook') {
				$('#myModal').modal()
				deleteBook($identificador, $token);
			}

			if ($valor == 'editBook') {
				$.ajax({
				url: '/admin/edit_book/' + $identificador.attr('data-book'),
				type: 'GET',
				beforeSend: function(xhr) {
								xhr.setRequestHeader("X-CSRFToken", $token );
						}
				})
					.done(function() {
						console.log("success");
						location.href = '/admin/edit_book/' + $identificador.attr('data-book');
					})
					.fail(function() {
						console.log("error");
					})
					.always(function() {
						console.log("complete");
					});
			}


// usuarios
			if ($valor == 'deleteUser') {
				$('#myModal').modal();
				deleteUser($identificador, $token);
			}

			if ($valor == 'showUser') {
				$('#showModalUser').modal();
				showUser($identificador, $token);
			}

		});
});

function deleteUser($identificador, $token){
	$("#confirmar").click(function(event){
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
				$('#myModal').modal("hide")
			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});
		});
}

function deleteBook($identificador, $token){
	$("#confirmar").click(function(event){
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
				$('#myModal').modal("hide")
			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});
		});
}

function showUser($identificador, $token){
	$.ajax({
		url: '/admin/show_users/' + $identificador.attr('data-usuario'),
		dataType: 'json',
		type: 'GET',
		beforeSend: function(xhr) {
				xhr.setRequestHeader("X-CSRFToken", $token );
			}
		})
			.done(function(data) {
				console.log("success");
				$("#username").text(data.User.username);
				$("#email").text(data.User.email);
				
			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});
}
function showBook($identificador, $token){
	$.ajax({
		url: '/admin/show_book/' + $identificador.attr('data-book'),
		dataType: 'json',
		type: 'GET',
		beforeSend: function(xhr) {
						xhr.setRequestHeader("X-CSRFToken", $token );
				}
		})
			.done(function(data) {
				console.log("success");
				$("#portada").attr("src","/static/"+data.Book.portada);
				$("#titulo").text("Titulo del libro: " + data.Book.titulo);
				$("#editorial").text("Editorial del libro: " + data.Book.editorial);
				$("#numeroPaginas").text("Numero de paǵinas: " +data.Book.numeroPaginas);
				$("#autor").text("Autor del libro: " +data.Book.autor);
				$("#precio").text("Precio del libro: " +data.Book.precio);
				
			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});
}