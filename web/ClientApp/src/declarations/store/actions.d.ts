//import { IDiskInfo } from "../model/disk";

// Disk Action
interface RequestDiskInfoAction  {
    type: "REQUEST_DISK_INFO";
}
interface ReceiveDiskInfoAction  {
    type: "RECEIVE_DISK_INFO";
    disk: IDiskInfo;
}
interface ReceiveDiskConnectAction  {
    type: "RECEIVE_DISK_CONNECT";
    disk: IDiskInfo;
}
interface ReceiveDiskDisconnectAction  {
    type: "RECEIVE_DISK_DISCONNECT";
    disk: IDiskInfo;
}
