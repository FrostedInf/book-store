$(document).ready(function(){
	var $idLibro;
	var $token;
	$(".btnGuardar").click(function(event){
		$idLibro=$(this).parent('div');
		console.log($idLibro);
		$token=$("#idtoken").val();
		agregarCarrito($idLibro,$token);
	})

	$(".eliminarLibro").click(function(event){
		$idLibro=$(this).parent('div');
		console.log($idLibro);
		$token=$("#idtoken").val();
		eliminarCarrito($idLibro,$token);
	})

	$(".btnFinalizar").click(function(event){
		$idLibro=$(this).parent('div');
		console.log($idLibro);
		$token=$("#idtoken").val();
		finalizarCompra($idLibro,$token);
	})
});

function agregarCarrito($idLibro,$token){
	var datos = $idLibro.attr('data-book');
	console.log(datos);
	var datasend = {'idLibro': datos }
	$.ajax({
		url: '/agregarCarrito',
		type: 'POST',
		dataType: 'json',
		contentType:'application/json',
		data: JSON.stringify(datasend),
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken",$token);
		}
	})
	.done(function() {
		console.log("success");
		$("#agregadoCarrito").modal();
	})
	.fail(function(xhr, status, error) {
		console.log("error");
		console.log(error);
	})
	.always(function() {
		console.log("complete");
	});
}

function eliminarCarrito($identificador,$token){
	var data = $identificador.attr('data-book');
	console.log(data);

	$.ajax({
		url: '/eliminarCarrito/' + data,
		type: 'GET',
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken",$token);
		}
	})
	.done(function() {
		console.log("success");
		$identificador.remove();
		location.href = '/carrito';
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});
}

function finalizarCompra($idLibro,$token){
	var total = $("#total").text(); 
	var datasend = {"total": total }
	$.ajax({
		url: '/finalizarCompra',
		type: 'POST',
		dataType: 'json',
		contentType:'application/json',
		data: JSON.stringify(datasend),
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken",$token);
		}
	})
	.done(function() {
		console.log("success");
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});
}