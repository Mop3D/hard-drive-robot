import * as React from 'react';
import { SendCommand } from "../../misc/function";

interface IOwnProps {
    slotNo: number,
}

interface IOwnState {
    status: string
}

export default class RackSlot extends React.Component<IOwnProps, {}> {
    //constructor(props: IOwnProps) {
    //    super(props);
    //  }
          // state
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
    slot_onClick()
    {
        console.log("slot no", this.props.slotNo)    
        SendCommand(this, "slot", this.props.slotNo);
    }

    render() {
        //const { status } = this.state;

        const pageContent = <div className="rackslot row">
            <div className="col-12 slot inactive" onClick={() => this.slot_onClick()}>
                Slot No: {this.props.slotNo} - {this.state.status}
            </div>
        </div>

        return (
            <>
            {/* content */}
            {pageContent}
            </>
        )
    }
}
