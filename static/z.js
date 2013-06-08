
function addcrush(e) {
	e.preventDefault();
	var crush=$("#ccrush").val();
	var year=$("#cyear").val();
    var chm=$("#chm").prop('checked') ? true : false;
    console.log(chm);
	$.get("/addAjax",{'ccrush':crush,'cyear':year,'chm':chm},
	     function(data) {
		 $("#crushesgohere").empty();
		 $("#crushesgohere").append(data);
		 $("#ccrush").val("");
		 $("#cyear").val("");
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

