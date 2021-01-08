# Status Infos from Objects

## StatusObject
send Status Json to the connected client
{
    "Action": action,
    "Object": messageFrom
    /*
    "json": ...
    */ 
}

method StatusInfo
        -> Action: Info
        -> Object: messageFrom
(json)  -> Message: message
        self.WriteStatus(messageFrom, "Info", message, True)


## DeviceConnect
Object: devicemon 

action: connectDisk
json: { "diskid": "disk1234", "mounted": [ "Part1"] }

action: disconnectDisk
json: { "diskid": [ "disk1234"] }