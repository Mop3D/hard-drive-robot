import { connect } from "react-redux";
import { Action, bindActionCreators, Dispatch } from "redux";
import { actionCreators } from '../../../store/actions';
import { ApplicationState  }  from '../../../store';
import {
    selectDisk
  } from "../../../store/selectors";
  
import Layout from './Layout';
import { string } from 'prop-types';
import { IDiskInfo } from "../../../declarations/model/disk";

/* This component is used as main container for all pages.
   It has the responsibility to provide state data to Layout Component.
   LayoutContainer is used on all components inside /pages folder as a wrapper component.
   Layout creates header and footer and renders it's children as page content.
*/
export interface IReduxStateProps {
    disk?: IDiskInfo;
  }
  
export interface IDispatchProps {
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
  
export default connect(mapStateToProps, mapDispatchToProps)(Layout);
  