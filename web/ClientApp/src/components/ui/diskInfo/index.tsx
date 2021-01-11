import * as React from 'react';
import { SendCommand } from "../../misc/function";

interface IOwnProps {
}

interface IOwnState {
    status: string
}

export default class RackSlot extends React.Component<IOwnProps, {}> {
    state = {
        status: "empty"
    }

    // component did mount
    componentDidMount() {
/*         this.setState({
            loading: false,
            hasError: false
        });
 */ 
    }
    
    render() {
        const { status } = this.state;

        const pageContent = <div className="diskinfo row">
            <div className="col-12 inactive">Disk Info: {this.state.status}</div>
        </div>

        return (
            <>
            {/* content */}
            {pageContent}
            </>
        )
    }
}
