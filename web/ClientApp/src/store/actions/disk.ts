import { AppThunkAction } from "..";
import * as ActionTypes from "./actionTypes";
import { IDiskInfo } from "../../declarations/model/disk";

type KnownAction = ReceiveDiskInfoAction | ReceiveDiskConnectAction | ReceiveDiskDisconnectAction;

export const setDiskInfo = (disk: IDiskInfo): AppThunkAction<KnownAction> => (dispatch, getState) => {
    return dispatch({ type: ActionTypes.ReduxConstants.RECEIVE_DISK_INFO, disk });
  };

//export const setDiskInfo = (disk: IDiskInfo): AppThunkAction<KnownAction> => dispatch =>
//  dispatch({ type: ActionTypes.ReduxConstants.RECEIVE_DISK_INFO, disk });