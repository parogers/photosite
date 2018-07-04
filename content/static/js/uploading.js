function upload_photo()
{
    /*
    var form = document.createElement("form");
    form.action="/upload";
    form.method="post";
    form.enctype="multipart/form-data";
    
    var input = document.createElement("input");
    input.type = "file";
    input.name = "image";
    input.id = "id_image";

    var test = document.createElement("input");
    test.type = "text";
    test.name = "test";
    test.value = "Hello world";

    form.appendChild(input);
    form.appendChild(test);
    form.style.display = "none";
    document.body.appendChild(form);

    console.log(form.submit);
    
    $(input).trigger("click");*/

    $('#image_id').trigger('click');
}

$(document).ready(function() {

    var form = $('#upload-form');
    if (form)
    {
	var input = $('#image_id');
	input.change(function() {
	    var msg = $('#upload-message');
	    msg.html('Uploading image...');
	    msg.addClass('shown');

	    setTimeout(function() {
		form.submit();
	    }, 1);
	});
    }

});
