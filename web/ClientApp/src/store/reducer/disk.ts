import { Action, Reducer } from "redux";
import * as ActionTypes from "../actions/actionTypes";
import initialState from "../../initialState";

// ----------------
// REDUCER - For a given state and action, returns the new state. To support time travel, this must not mutate the old state.
type KnownAction = RequestDiskInfoAction | ReceiveDiskInfoAction | ReceiveDiskConnectAction | ReceiveDiskDisconnectAction;

export const reducer: Reducer<DiskState> = (state: DiskState = initialState.disk, incomingAction: Action) => {
    const action = incomingAction as KnownAction;
    switch (action.type) {
      case ActionTypes.ReduxConstants.REQUEST_DISK_INFO:
        return {
          ...state,
          error: false,
          isLoading: true
        };
        case ActionTypes.ReduxConstants.RECEIVE_DISK_CONNECT:
            return {
              ...state,
              data: action.disk,
              error: false,
              isLoading: false
            };
        default:
    }
          
    return state;
};
