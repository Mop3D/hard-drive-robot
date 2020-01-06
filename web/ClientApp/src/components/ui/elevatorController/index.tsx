import * as React from 'react';
import axios from 'axios';
import { robopiApi } from "../../misc/function";
import MessageBox from '../../ui/messageBox';
import { stringify } from 'querystring';

interface IOwnProps {
}

interface IOwnState {
    status: string
    outMessage: string
    hasError: boolean
}

export default class ElevatorController extends React.Component<IOwnProps, {}> {
    // state
    state = {
        status: "empty",
        outMessage: "",
        hasError: false
    }
    // component did mount
    componentDidMount() {
    }

    button_Click(type: string)
    {
        console.log("button_Click", type)
        if (type == "ping")
            this.sendCommand(type);
    }
    //
    // send command: ping
    //
    sendCommand = async (command: string) => {
        const APIENDPOINT = robopiApi(command);

        /* get dropdown data */
        const res = await axios.get(APIENDPOINT);
        const { data } = await res;
        try {
            console.log("sendCommand", command, data)
            if (data) {
                this.setState({
                    outMessage: "returnData: " + stringify(data),
                    hasError: false
                });
            } else {
                console.error("sendCommand - no valid data", data);
                this.setState({ hasError: true });
            }
        } catch (e) {
            console.error("sendCommand - error data", e);
            this.setState({ hasError: true });
        }
    }
    // render
    
    render() {
        const pageContent = <div className="elevatorcontroller">
            <div className="row">
                <div className="col-12 center">
                    <button onClick={() => this.button_Click("up")}>up</button>
                </div>
            </div>
            <div className="row">
                <div className="col-1"></div>
                <div className="col-5 center">
                <button onClick={() => this.button_Click("in")}>in</button>
                </div>
                <div className="col-5 center">
                <button onClick={() => this.button_Click("out")}>out</button>
                </div>
                <div className="col-1"></div>
            </div>
            <div className="row">
                <div className="col-12 center">
                    <button onClick={() => this.button_Click("down")}>down</button>
                </div>
            </div>
            <hr/>
            <div className="row">
                <div className="col-12 center">
                    <button onClick={() => this.button_Click("calibration")}>calibrate</button>
                </div>
            </div>
            <hr/>
            <div className="row">
                <div className="col-12 center">
                    <button onClick={() => this.button_Click("ping")}>ping</button>
                </div>
            </div>
        </div>
        return (
            <>
            {/* content */}
            {pageContent}
            <MessageBox msg={this.state.outMessage} className={this.state.hasError ? "error" : "warning"} />
            </>
        )
    }
}