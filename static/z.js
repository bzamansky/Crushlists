
function addcrush(e) {
    e.preventDefault();
    var crush=$("#ccrush").val();
    var cyear=$("#cyear").val();
    var lyear=$("#lyear").val();
    var chm=$("#chm").prop('checked') ? true : false;
    $.get("/addAjax",{'ccrush':crush,'cyear':cyear,'lyear':lyear,'chm':chm},
	  function(data) {
	      $("#crushesgohere").empty();
	      $("#crushesgohere").append(data);
	      $("#ccrush").val("");
	      $("#cyear").val("");
	      $("#lyear").val("");
	      //$("#chm").attr('checked',false);
	      $("#ccrush").focus();

	  });
}


$(document).ready(function () {
    $("#addcrush").click(addcrush);
    $(document).keypress(function(e){
	if (e.charCode==13) {
	    addcrush(e);
	}
	});
});

