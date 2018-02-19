$(document).ready(function() { $('#outV').html('Version V4'); });
function getJsonData(url, sendData, onSuccess, onError, onAllways) {
	var headers = { 
        "Accept": "text/javascript; charset=utf-8",
		"Content-Type": "text/javascript; charset=utf-8"
    }
	
	var contentType = 'text/javascript';
	return callAjax(url, null, contentType, headers, sendData, onSuccess, onError, onAllways);
}
function callAjax(url, method, contentType, headers, sendData, onSuccess, onError, onAllways) {
	
	return $.ajax({
		url: url,
		method: method || 'get',
		contentType: contentType,
		data: sendData,
		headers: headers
	}).done(function(data) {
		console.log("call done", typeof data, data)
		if (typeof onSuccess != 'undefined') onSuccess(data);
	}).fail(function(jqXHR, textStatus, errorThrown) {
		console.log("call fail", jqXHR, textStatus, errorThrown)
    }).always(function() {
		console.log("call always")
    });
}
