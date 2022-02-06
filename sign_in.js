console.log('file is opened.....');

$(document).ready(function(){

    var $LoginForm = $('#SignInForm');
    $LoginForm.submit(function(event){
        event.preventDefault();
        // Waiting on form submit event.....
        var formData = $(this).serialize();
         // preparing AJAX call headers
         $.ajaxSetup({
            headers:
            { 'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content') }
        });
        $.ajax({
            // preparing AJAX call.....
            data: formData,
            contentType: "application/json; charset=utf-8",
            type: "POST",

            dataType: "json",
            url: '/validate/login/form/',

            success: function(response){
                if (response.is_valid == false){
                    console.log('data is not valid.....');
                    $LoginForm.removeClass('is-valid').addClass('is-invalid');
                    $LoginForm.after('<div class="invalid-feedback d-block" id="Error">Invalid Data...</div>');
                }else{
                    $LoginForm.removeClass('is-invalid').addClass('is-valid');
                    $('#Error').remove();

                    console.log('data is valid.....');
                    SendPostLoginRequest(formData);

                    console.log('POST request has been sended.....')
                    window.location.href = "/";
                }},
            error: function(error){
               console.log('ERROR, could not send ajax request....', error)
            }
        });
        return false;
    });
});

function SendPostLoginRequest(data){
    var url = new URL('http://localhost:8000/get/login/page/');
    var request = new XMLHttpRequest(url);

    request.setRequestHeader('Content-type', 'application/json');
    request.setRequestHeader('Access-Control-Allow-Origin', 'http://localhost:8000/get/login/page/');

    request.send(data);
}


