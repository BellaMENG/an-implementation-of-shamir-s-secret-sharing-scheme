function split() {
// TODO: to call the split function
// file: ../split.py
// encrypt_string(secret, intercept, degree, field_base)
    var secret = document.getElementById('secret_string').value;
    var intercept = document.getElementById('intercept').value;
    var degree = document.getElementById('degree_add1').value;
    var field_base = document.getElementById('field_base').value;
    var params = [{"secret":"some thing", "intercept":intercept,"degree":degree, "field_base":field_base}];

    window.onload = function() {
	    document.getElementById("split_btn").onclick = function() {
		    split()
	    };
    }
    function split() {
        $.post( '/split', params, function(){});
        event.preventDefault();
    }
    // TODO: check validity of input values
}