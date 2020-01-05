import * as React from 'react';

interface IOwnProps {
    msg: string,
    className: string
}
export default class MessageBox extends React.Component<IOwnProps, {}> {
    render() {
        const setClassName = this.props.className === "error"  ? "alert-danger" : this.props.className === "warning"  ? "alert-warning" : "";
        return <div className={ setClassName }>
            {this.props.msg}
        </div>
        {/*}
        return <div className={ this.props.className('MessageBox alert', {'alert-danger': this.props.className === 'error', 'alert-warning': this.props.className === 'warning'}) }>
            { this.props.msg }
        </div>
    */}
    }
}
