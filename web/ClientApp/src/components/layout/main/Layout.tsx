import * as React from 'react';
import Header from '../header';
import Footer from '../footer';
import 'bootstrap/dist/css/bootstrap.min.css';
interface IDispatchProps {

}

 interface IOwnProps {
    showHeaderFooter?: boolean;
} 

type IProps = IDispatchProps & IOwnProps;

export default class Layout extends React.Component<IProps, {}> {
    componentDidMount(){
    }

    public render() {
        return (
        <>
            { this.props.showHeaderFooter && <Header /> }
            <div className="page-container">
                { this.props.children } 
            </div>                    
            { this.props.showHeaderFooter && <Footer /> }
        </>
        ) 
    }
}
