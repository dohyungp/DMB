$(function(){
	$("login-button").click(function(){
		$('a.modal').modal({
			remote : 'login-modal.html'
		});
	})
})