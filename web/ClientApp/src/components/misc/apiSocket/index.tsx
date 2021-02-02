// new with hooks
// Sampel HP MobileFind

import * as React from 'react';
import { useEffect } from "react";
import { useDispatch } from "react-redux";

import Websocket from 'react-websocket';

import { setDiskInfo } from "../../../store/actions/disk";

import { IDiskInfo } from "../../../declarations/model/disk";

const ApiSocket = () => {
    // getter, setter           // default wert
    //const [status, setStatus] = useState("empty");
    const dispatch = useDispatch();

    // component did mount
    useEffect(() => {
        //didmount
        // ...
        //  will unmount
        return () => {
            // ...
        };
      }, []);
      //-> [] hier kommen die Properties rein.

    const Websocket_onMessage = (data: any) => {
        if (data.substring(0,1) !== "{")
        {
            console.log("no json data - abbort");
            return;
        }
        const jsonData = JSON.parse(data);
        console.log("ApiSocket Websocket_onMessage", jsonData);
        // is command jsonrpc
        if (!jsonData.command || jsonData.command !== "jsonrpc") {
            console.log("no jsonrpc command - abbort");
            return;
        }
        // is method
        if (!jsonData.data || !jsonData.data.method || jsonData.data.method === "") {
            console.log("no jsonrpc Method command - abbort");
            return;
        }
        const callMethod = jsonData.data.method;
        console.log("jsonprc Method", callMethod);
        if (callMethod == "OnConnect")
        {
            const diskInfo: IDiskInfo =
            {
                    diskid: jsonData.data.result.diskid,
                    mountpoints: jsonData.data.result.mounted
            } 
            dispatch(setDiskInfo(diskInfo));
        }
        else if (callMethod == "OnDisconnect")
        {
            dispatch(setDiskInfo(undefined));
        }

    }
    const Websocket_onOpen = () => {
        console.log("ApiSocket Websocket_onOpen");
    }
    const Websocket_onClose = () => {
        console.log("ApiSocket Websocket_onClose");
    }


    //  Render component
    return (
        <Websocket url="ws://hdrobo:8888/ws"
            onMessage={(data: any) => Websocket_onMessage(data) }
            onOpen={() => Websocket_onOpen() }
            onClose={() => Websocket_onClose() }
            debug={true}
        />
)
}

export default ApiSocket;