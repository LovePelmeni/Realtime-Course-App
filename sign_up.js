// This is a Sign Up User AJAX Form....
console.log('file is opened...');

$(document).ready(function(){
    var RegisterForm = $('#SignUpForm');

    RegisterForm.submit(function(event){
        var formData = $(this).serialize();
        $.ajaxSetup({
        headers:{ 'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content') }});

        event.preventDefault();
        console.log('started... process');
        //Creating AJAX call.....
        $.ajax({
            data: formData, // data, specified in form.....
            type: "POST", // type of request method.....
            url: "/validate/register/form/", // url to send data for validation.....

            contentType: "application/json; charset=utf-8", // type of the content......
            dataType: "json", // type of data...

            success: function(response){
            // this part executed if AJAX call has been sended successfully......
                if (response.is_valid == false){
                    console.log('invalid data has been received...');

                    RegisterForm.removeClass('is-valid').addClass('is-invalid');
                    RegisterForm.after('<div class="invalid-feedback d-block" id="Error">Invalid Data...</div>');
                     // if valid, logs result into console and just passing through without any issues.....
                }else{
                    console.log('looks like everything is okay...');
                    RegisterForm.removeClass('is-invalid').addClass('is-valid');

                    $('#Error').remove();
                    SendPostRegisterRequest(formData);
                    console.log('POST request has been sended.....');

                    window.location.href = "/";
                }
            },
            error: function(error){ // So obviously this when could not send AJAX request.....
                console.log('error, could not send AJAX call....', error);
            }
        });
       return false;
    });
});

function SendPostRegisterRequest(data){
    var request = new XMLHttpRequest();
    var url = new URL('http://localhost:8000/get/register/page/');

    request.open('POST', url, true);
    request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    request.setRequestHeader('Access-Control-Allow-Origin', '*');

    request.send(data);
}
//            xhrFields: {
//                withCredentials: true
//            },







