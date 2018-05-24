$(document).ready(function(){
	var $idLibro;
	var $token;
	$(".btnGuardar").click(function(event){
		$identificador=$(this).parents('div');
		console.log($identificador);
		$token=$("#idtoken").val();
		agregarCarrito($identificador,$token);
	})
});
function agregarCarrito($identificador,$token){
	var data = $identificador.attr('data-book');
	console.log(data);
	var datasend = {'idLibro': data };
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
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});
	
	
}