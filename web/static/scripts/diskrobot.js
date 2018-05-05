<<<<<<< HEAD
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

=======
var ws;
$(document).ready(function() {
	$('.btn-command').on('click', btnCommandClicked);
	$('.btn-slot').on('click', btnSlotClicked);
	
	ws_openSocket();

	setTimeout(getInfo, 500)
>>>>>>> 4eef35c125ae8a425e3e7efebb31d7f979c3f462
});


function btnSlotClicked()
{
	var slotNo = $(this).data("slotno");
	motorCommand('Elevator', 'slot', slotNo);
}
<<<<<<< HEAD

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
=======
function btnCommandClicked()
{
	console.log("btnCommandClicked", $(this).data("motor"), $(this).data("command"))
	motorCommand($(this).data("motor"), $(this).data("command"));
}

function getInfo()
{
	motorCommand('Elevator', 'info');
	motorCommand('Connector', 'info');
>>>>>>> 4eef35c125ae8a425e3e7efebb31d7f979c3f462
}

function motorCommand(motorName, command, slotNo)
{
<<<<<<< HEAD
=======
	if (ws.readyState != 1) ws_openSocket();
	//console.log("ws", ws)
>>>>>>> 4eef35c125ae8a425e3e7efebb31d7f979c3f462
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
<<<<<<< HEAD
	infoOut += '<p>Sleep time:' + data.sleeptime + '</p>';
	$('#elevatorInfo').html(infoOut);
}

//***************************************************************************
=======
	//infoOut += '<p>Sleep time:' + data.sleeptime + '</p>';
	if (data.name == "Elevator")
		$('#elevatorInfo').html(infoOut);
	else
		$('#connectorInfo').html(infoOut);
}
// set slot info
function setSlotInfo(command, data)
{
	var slotBtn = $("#btnSlot" + data.SlotNo);
	console.log("setSlotInfo", command, slotBtn.length, data)
	if (command == "connecttoslot")
	{
		$('.btn-slot').each(function (index, value) { 
		  $(this).prop("disabled", true); 
		});
		console.log("setSlotInfo connecttoslot")
		slotBtn.addClass("connectToSlot");
		slotBtn.text("Slot " + data.SlotNo + ", connect...")
	}
	if (command == "connecteddisk")
	{
		if (data.Device.Type == "disk")
		{
			slotBtn.removeClass("connectToSlot");
			slotBtn.addClass("connectedToSlot");
			slotBtn.text("Slot " + data.SlotNo + ", " + data.Device.Serial)
			slotBtn.attr("title", "");
		}
		if (data.Device.Type == "partition")
		{
			slotBtn.attr("title", slotBtn.attr("title") + (slotBtn.attr("title") != "" ? ", " : "") + data.Device.Node);
		}
	}
	if (command == "disconnecteddisk")
	{
		slotBtn.removeClass("connectToSlot");
		slotBtn.removeClass("connectedToSlot");
		slotBtn.text("Slot " + data.SlotNo);
		slotBtn.attr("title", "");
		$(".btn-slot").each(function (index, value) { 
		  $(this).prop("disabled", false); 
		});
	}
}


//***************************************************************************
	function ws_openSocket()
	{
		var host = window.location.host;
		ws = new WebSocket('ws://' + host + '/ws');

		ws.onopen = ws_onOpen;
		ws.onmessage = ws_onMessage;
		ws.onclose = ws_onClose;
		ws.onerror = ws_onError;	
	}
>>>>>>> 4eef35c125ae8a425e3e7efebb31d7f979c3f462
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
<<<<<<< HEAD
	  if (jsonData.command == "motorinfo")
=======
	  if (jsonData.command == "statusinfo")
	  {
		//addWebSocketMessage(jsonData.command, JSON.stringify(jsonData.data));		  
		showInfo(jsonData.data)
	  }
	  else if (jsonData.command == "motorinfo")
>>>>>>> 4eef35c125ae8a425e3e7efebb31d7f979c3f462
	  {
		addWebSocketMessage(jsonData.command, JSON.stringify(jsonData.data));		  
		showInfo(jsonData.data)
	  }
<<<<<<< HEAD
=======
	  else if (jsonData.command == "connecttoslot" || jsonData.command == "connecteddisk" || jsonData.command == "disconnecteddisk")
	  {
		addWebSocketMessage(jsonData.command, JSON.stringify(jsonData.data));		  
		setSlotInfo(jsonData.command, jsonData.data)
	  }
>>>>>>> 4eef35c125ae8a425e3e7efebb31d7f979c3f462
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