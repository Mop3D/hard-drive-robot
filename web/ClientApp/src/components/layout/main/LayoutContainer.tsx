import * as React from 'react';
import * as Redux from 'redux';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { actionCreators } from '../../../store/actions';
import { ApplicationState }  from '../../../store';
import Layout from './Layout';
import { string } from 'prop-types';

interface IStateProps {
}
     
interface IDispatchProps {
}

interface IOwnProps {
    showHeaderFooter?: boolean;
}

// Selects which state properties are merged into the component's props
const mapStateToProps = (state: ApplicationState): IStateProps => {
    return {
    };
}

// Selects which state store actions are merged into the component's dispatch
const mapDispatchToProps = (dispatch: Redux.Dispatch<any>): IDispatchProps => {
    const storeActions = bindActionCreators<any, any>(actionCreators, dispatch);
    return storeActions;
}
  
export default connect<IStateProps, IDispatchProps, IOwnProps>
  (mapStateToProps, mapDispatchToProps)(Layout) 
