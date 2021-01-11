import * as React from 'react';
import axios from 'axios';
import { SendCommand } from "../../misc/function";
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

    button_Click(type: string, value?: number)
    {
        SendCommand(this, type, value);
    }

    // render
    render() {
        const pageContent = <div className="elevatorcontroller">
            <div className="row">
                <div className="col-12 center">
                    <button onClick={() => this.button_Click("up", 50)}>up</button>
                </div>
            </div>
            <div className="row">
                <div className="col-1"></div>
                <div className="col-5 center">
                <button onClick={() => this.button_Click("forward", 50)}>in 50</button>
                </div>
                <div className="col-5 center">
                <button onClick={() => this.button_Click("backward", 50)}>out 50</button>
                </div>
                <div className="col-1"></div>
            </div>
            <div className="row">
                <div className="col-12 center">
                    <button onClick={() => this.button_Click("down", 50)}>down</button>
                </div>
            </div>
            <hr/>
            <div className="row">
                <div className="col-6">
                    Elevator Status
                </div>
                <div className="col-6">
                    Connector Status
                </div>
            </div>
            <hr/>
            <div className="row">
                <div className="col-12 center">
                    <button onClick={() => this.button_Click("poweroff", undefined)}>power off</button>
                </div>
            </div>
            <hr/>
            <div className="row">
                <div className="col-12 center">
                    <button onClick={() => this.button_Click("calibrate", undefined)}>calibrate</button>
                    <button onClick={() => this.button_Click("reset", undefined)}>reset</button>
                </div>
            </div>
            <hr/>
            <div className="row">
                <div className="col-12 center">
                    <button onClick={() => this.button_Click("connect", undefined)}>Connect HD</button>
                    <button onClick={() => this.button_Click("release", undefined)}>release HD</button>
                </div>
            </div>
            <hr/>
            <div className="row">
                <div className="col-12 center">
                    <button onClick={() => this.button_Click("ping", undefined)}>ping</button>
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
