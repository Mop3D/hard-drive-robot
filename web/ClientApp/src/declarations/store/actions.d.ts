//import { IDiskState } from "../model/disk";

// Disk Action
interface RequestDiskInfoAction  {
    type: "REQUEST_DISK_INFO";
}
interface ReceiveDiskInfoAction  {
    type: "RECEIVE_DISK_INFO";
    disk: IDiskState;
}
interface ReceiveDiskConnectAction  {
    type: "RECEIVE_DISK_CONNECT";
    disk: IDiskState;
}
interface ReceiveDiskDisconnectAction  {
    type: "RECEIVE_DISK_DISCONNECT";
    disk: IDiskState;
}
