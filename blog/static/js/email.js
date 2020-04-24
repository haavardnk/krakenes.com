$('#emailForm').submit(function(e){
	var formId = $(this).attr('id');
	var submitBtn = $(this).find('input[type=submit]');
	submitBtn.prop('disabled', true);
	e.preventDefault();
	$.ajax({
		url: "/about/", // the file to call
		type: "POST", // GET or POST
		data: $(this).serialize(), // get the form data
		success: function(data){
			var email_response = jQuery.parseJSON(data);
			console.log(email_response);
			if (email_response.send == "success"){
                swal.fire({ 
                    title:"Thank you for reaching out!", 
                    text: "I will get back to you shortly!", 
                    type: "success", 
                    buttonsStyling: false, 
                    confirmButtonClass: "btn btn-rose"})
			}
			else {
                swal.fire({ 
                    title:"The contact form has failed...", 
                    text: "Im sorry to say the message will never reach me. Please send an email to krakenesphotography@gmail.com", 
                    type: "error", 
                    buttonsStyling: false, 
                    confirmButtonClass: "btn btn-rose"})
			}/*./else*/
		},/* end of Success */
		error: function(data) {
			swal.fire({ 
                title:"The contact form has failed...", 
                text: "Im sorry to say the message will never reach me. Please send an email to krakenesphotography@gmail.com", 
                type: "error", 
                buttonsStyling: false, 
                confirmButtonClass: "btn btn-rose"})
		}/*  end of error */
	});/*./ajax*/
});