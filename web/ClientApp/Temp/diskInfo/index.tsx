// new with hooks
// Sampel HP MobileFind

import * as React from 'react';
import { useEffect, useState } from "react";

import { useDispatch, useSelector } from "react-redux";

import { selectDisk } from "../../../store/selectors";
import { setDiskInfo } from "../../../store/actions/disk";

import { IDiskInfo } from "../../../declarations/model/disk";

const DiskInfo = () => {
    // getter, setter           // default wert
    //const [status, setStatus] = useState("empty");
    const [status2, setStatus2] = useState("empty2");
    const dispatch = useDispatch();
    const diskSelect: IDiskInfo = useSelector(selectDisk);

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


    const button_Click = () =>
    {
        const diskInfo: IDiskInfo =
        {
                diskid: "abcde",
                mountpoints: []
        } 
        console.log("button_Click", diskInfo)
        dispatch(setDiskInfo(diskInfo));
        setStatus2("neuer Status");
    }

    const pageContent = <div className="diskinfo row">
        <div className="col-12 inactive">Disk Info: { diskSelect.diskid}</div>
        <div className="col-12 inactive">Status: { status2 }</div>

        <button onClick={() => button_Click()}>set DiskInfo</button>

    </div>

    //  Render component
    return (
            <>
            {/* content */}
            {pageContent}
            </>
        )
}

export default DiskInfo;
  