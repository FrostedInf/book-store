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

	$(".btnCancelarCompra").click(function(event){
		$token=$("#idtoken").val();
		cancelarCompra($token);
	})
});

function agregarCarrito($idLibro,$token){
	var datos = $idLibro.attr('data-book');
	console.log(datos);
	var datasend = {'idLibro': datos }
	$.ajax({
		url: '/agregarCarrito',
		type: 'POST',
		dataType: 'text',
		contentType:'application/json',
		data:JSON.stringify(datasend),
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken",$token);
		}
	})
	.done(function() {
		console.log("success");
		console.log($("#agregadoCarrito").find())
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
		dataType: 'text',
		contentType:'application/json',
		data: JSON.stringify(datasend),
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken",$token);
		}
	})
	.done(function() {
		console.log("success");
		$("#modalCompraFinalizada").modal();
		location.reload()
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});
}
function cancelarCompra($token){
	$.ajax({
		url: '/cancelarCompra',
		dataType: 'text',
		type: 'GET',
		beforeSend: function(xhr){
			xhr.setRequestHeader("X-CSRFToken",$token);
		}
	})
	.done(function() {
		console.log("success");
		location.reload()
	})
	.fail(function(xhr, status, error) {
		console.log("error");
		console.log(error);
	})
	.always(function() {
		console.log("complete");
	});
}