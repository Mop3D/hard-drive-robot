$(document).ready(function() {
	$('#btnElevForward').on('click', btnElevForwardClicked);
	$('#btnElevBackward').on('click', btnElevBackwardClicked);
	$('#btnElevCalibrate').on('click', btnElevCalibrateClicked);
	$('#btnConnForward').on('click', btnConnForwardClicked);
	$('#btnConnBackward').on('click', btnConnBackwardClicked);

	$('.btn-slot').on('click', btnSlotClicked);
		
    var host = window.location.host;
    var ws = new WebSocket('ws://'+host+'/ws');

    ws.onopen = ws_onOpen;
    ws.onmessage = ws_onMessage;6
    ws.onclose = ws_onClose;
    ws.onerror = ws_onError;	

	setTimeout(getInfo, 500)

});


function btnSlotClicked()
{
	var slotNo = $(this).data("slotno");
	motorCommand('Elevator', 'slot', slotNo);
}

function btnElevCalibrateClicked()
{
	motorCommand('Elevator', 'calibrate');
}
function btnElevForwardClicked()
{
	motorCommand('Elevator', 'forward');
}
function btnElevBackwardClicked()
{
	motorCommand('Elevator', 'backward');
}
function btnConnForwardClicked()
{
	motorCommand('Connector', 'forward');
}
function btnConnBackwardClicked()
{
	motorCommand('Connector', 'backward');
}
function getInfo()
{
	motorCommand('Elevator', 'info');
}

function motorCommand(motorName, command, slotNo)
{
	console.log('motorCommand motor, command', motorName, command)
	var url = '/motor/' + motorName + "/" + command;
	if (slotNo) url += "?slotno=" + slotNo;
	$('#currentCommand').html(url + "...");
	getJsonData(url, null, successStepCall);	
}
function successStepCall(data){
	console.log('successStepCall ', data)
	$('#out2').html('successStepCall ' + data);
}
function showInfo(data)
{
	var infoOut = '<p>Current position:' + data.currentPosition + '</p>';
	infoOut += '<p>Sleep time:' + data.sleeptime + '</p>';
	$('#elevatorInfo').html(infoOut);
}

//***************************************************************************
	function ws_onOpen()
	{
	  console.log("open")
	  addWebSocketMessage("open", "");
	}
	function ws_onClose()
	{
	  console.log("ws close")
	  addWebSocketMessage("closed", "");
	}
	function ws_onError(ev)
	{
	  console.log("ws error", ev)
	  addWebSocketMessage("error", "occurred");
	}
	function ws_onMessage(ev)
	{
	  console.log("ws message", ev)

	  var jsonData = JSON.parse(ev.data);
	  if (jsonData.command == "motorinfo")
	  {
		addWebSocketMessage(jsonData.command, JSON.stringify(jsonData.data));		  
		showInfo(jsonData.data)
	  }
	  else if (jsonData.command == "signalhandler")
	  {
		addWebSocketMessage(jsonData.command, JSON.stringify(jsonData.data));		  
	  }
	  else
	  {
		addWebSocketMessage("message", ev.data);
	  }
	}
	function addWebSocketMessage(command, message)
	{
		//$("#webSocketMessages")[0].options.add( new Option(message), 0  );
		var time = new Date();
		var outTime = time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds() + "," + time.getMilliseconds();
		var trOut = '<tr>';
		trOut += '<td>' + outTime + '</td>';
		trOut += '<td>' + command + '</td>';
		trOut += '<td>' + message + '</td>';
		trOut += '</tr>';
		//$('#webSocketMessagesTable tr:last').after(trOut);
		$('#webSocketMessagesTable tr:first').after(trOut);
	}
	
//***************************************************************************




$(window).keypress(function(evt) {
	evt = (evt) ? evt : (window.event) ? event : null;
	if (!evt)
		return;
    var charCode = (evt.charCode) ? evt.charCode :((evt.keyCode) ? evt.keyCode :((evt.which) ? evt.which : 0));
	console.log("keypress char, charCode", charCode, String.fromCharCode(charCode))
	if (String.fromCharCode(charCode).toLowerCase() == "i") getInfo();
/*
    switch (charCode) {

    case 37:
        //prev();
        break;
    case 39:
        //next();
        break;

    }
*/
});