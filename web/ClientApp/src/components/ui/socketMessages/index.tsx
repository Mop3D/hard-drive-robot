import * as React from 'react';
import axios from 'axios';
//import { has } from 'lodash';
import Loading from '../../ui/loading';
import MessageBox from '../../ui/messageBox';
import Websocket from 'react-websocket';
import { stringify } from 'querystring';


interface IOwnProps {
}

interface IOwnState {
    loading: boolean;
    hasError: boolean;
    wsMessages: any;
}

export default class SocketMessages extends React.Component<IOwnProps, {}> {
    //constructor(props: IOwnProps) {
    //    super(props);
    //  }
          // state
    state = {
        loading: true,
        hasError: false,
        wsMessages: []
    }
    // component did mount
    componentDidMount() {
        this.setState({
            loading: false,
            hasError: false
        });

        //this.sendPing();
    }

    Websocket_onMessage(data: any) {
        console.log("Websocket_onMessage", data);
        //this.setState({wsMessages: stringify(data) });
        this.setState({wsMessages: "Websocket_Message: " + data });
        let result = JSON.parse(data);
    }
    Websocket_onOpen()
    {
        console.log("Websocket_onOpen");
    }
    Websocket_onClose()
    {
        console.log("Websocket_onOpen");
    }

    // render
    render() {
        return (
            <>
            <div className="socketMessage row">
                <div className="col-12">
                    {this.state.wsMessages}
                </div>
            </div>
            <Websocket url='ws://hdrobo:8888/ws'
                    onMessage={this.Websocket_onMessage.bind(this)}
                    onOpen={this.Websocket_onOpen.bind(this)}
                    onClose={this.Websocket_onClose.bind(this)}
                    debug={true}
                    />
            </>
        )
    }
}
