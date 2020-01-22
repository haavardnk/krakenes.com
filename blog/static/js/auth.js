/* Signup Form AJAX */
$('#signupForm').submit(function(e){
	var formId = $(this).attr('id');
	var submitBtn = $(this).find('input[type=submit]');
	$('#user-email-exists-error').css('display','none');
	submitBtn.prop('disabled', true);
	e.preventDefault();
	$.ajax({
		url: "/accounts/signup", // the file to call
		type: "POST", // GET or POST
		data: $(this).serialize(), // get the form data
		success: function(data){
			var signup_response = jQuery.parseJSON(data);
			if (signup_response.register == "success") {
				$('#signupModal').modal('hide');
                window.location.href = signup_response.url;
            }
            else if (signup_response.register == "email") {
                $('.signup-user-error').css('display', 'none');
                $('.signup-password-error').css('display', 'none');
				$('.signup-email-error').css('display', 'block');
				submitBtn.prop('disabled', false);
            }
            else if (signup_response.register == "user") {
                $('.signup-password-error').css('display', 'none');
				$('.signup-email-error').css('display', 'none');
				$('.signup-user-error').css('display', 'block');
                submitBtn.prop('disabled', false);
            }
            else if (signup_response.register == "password") {
                $('.signup-email-error').css('display', 'none');
				$('.signup-user-error').css('display', 'none');
				$('.signup-password-error').css('display', 'block');
				submitBtn.prop('disabled', false);
            }
			else {
                $('#signupModal').modal('hide');
                submitBtn.prop('disabled', false)
                $('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
			}
		},/* end of Success */
		error: function(data) {
			$('#signupModal').modal('hide');
			$('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
		}/*  end of error */
	});/*./ajax*/
});
/* End of Signup Form */

/* Login form AJAX */
$('#loginForm').submit(function(e){
	var formId = $(this).attr('id');
	var submitBtn = $(this).find('input[type=submit]');
	submitBtn.prop('disabled', true);
	e.preventDefault();
	$.ajax({
		url: "/accounts/login", // the file to call
		type: "POST", // GET or POST
		data: $(this).serialize(), // get the form data
		success: function(data){
			var login_response = jQuery.parseJSON(data);
			console.log(login_response);
			if (login_response.login == "success"){
                $('#login-modal').modal('hide');
                window.location.href = login_response.url;
			}
			else if (login_response.login == "password") {
                $('.login-user-error').css('display', 'none');
				$('.login-password-error').css('display', 'block');
				submitBtn.prop('disabled', false);
            } 
            else if (login_response.login == "nouser") {
                $('.login-password-error').css('display', 'none');
				$('.login-user-error').css('display', 'block');
				submitBtn.prop('disabled', false);
            } 
			else {
                $('#loginModal').modal('hide');
                submitBtn.prop('disabled', false)
                $('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
			}/*./else*/
		},/* end of Success */
		error: function(data) {
			$('#loginModal').modal('hide');
			$('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
		}/*  end of error */
	});/*./ajax*/
});
/*End of loin form AJAX */

/* Fixing modal scrolling upon second modal opening */
$(document).on('hidden.bs.modal', '.modal', function () {
    $('.modal:visible').length && $(document.body).addClass('modal-open');
});