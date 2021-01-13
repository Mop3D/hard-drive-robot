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
        console.log("ApiSocket Websocket_onMessage", data);

        const diskInfo: IDiskInfo =
        {
                diskid: "abcde",
                mountpoints: []
        } 
        dispatch(setDiskInfo(diskInfo));
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