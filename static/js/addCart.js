$(document).ready(function(){
	var $idLibro;
	var $token;
	$(".btnGuardar").click(function(event){
		$identificador=$(this).parents('div');
		$token=$("#idtoken").val();
		agregarCarrito($identificador,$token);
	})
});
function agregarCarrito($identificador,$token){
	$.ajax({
		url: '/agregarCarrito',
		type: 'POST',
		dataType: 'json',
		data: {idLibro: $identificador.attr('data-target') },
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