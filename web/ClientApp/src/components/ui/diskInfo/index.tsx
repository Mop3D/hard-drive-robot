import * as React from 'react';

import { connect } from "react-redux";
import { Action, bindActionCreators, Dispatch } from "redux";
import { actionCreators } from '../../../store/actions';
import { ApplicationState  }  from '../../../store';
import { selectDisk } from "../../../store/selectors";
import { setDiskInfo } from "../../../store/actions/disk";

import { IDiskInfo } from "../../../declarations/model/disk";


export interface IReduxStateProps {
    disk: IDiskInfo;
  }
export interface IDispatchProps {
    //setDiskInfo: (key: IDiskInfo) => void;
}

interface IOwnProps {
}

//  Merge all props.
type IProps = IReduxStateProps & IDispatchProps & IOwnProps;


class DiskInfo extends React.Component<IProps, {}> {
    state = {
        status: "empty"
    }

    // component did mount
    componentDidMount() {
    }

    button_Click()
    {
        const diskInfo: IDiskInfo =
        {
                diskid: "abcde",
                mountpoints: []
        } 
        console.log("button_Click", diskInfo)
        setDiskInfo(diskInfo)
    }

    render() {
        //const { status } = this.state;
        const { disk } = this.props;

        const pageContent = <div className="diskinfo row">
            <div className="col-12 inactive">Disk Info: { disk.diskid}</div>
            <div className="col-12 inactive">Status: {this.state.status}</div>

            <button onClick={() => this.button_Click()}>set DiskInfo</button>

        </div>

        return (
            <>
            {/* content */}
            {pageContent}
            </>
        )
    }
}

const mapStateToProps = (state: ApplicationState): IReduxStateProps => {
    return {
      disk: selectDisk(state)
    };
};
// Selects which state store actions are merged into the component's dispatch
const mapDispatchToProps = (dispatch: Dispatch<Action>): IDispatchProps => {
    const storeActions = bindActionCreators<any, any>(actionCreators, dispatch);
    return storeActions;
  };

export default connect(mapStateToProps, mapDispatchToProps)(DiskInfo);
  