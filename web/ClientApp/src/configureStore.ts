import { connectRouter, routerMiddleware } from "connected-react-router";
import { History } from "history";
import { applyMiddleware, combineReducers, compose, createStore, ReducersMapObject, Store } from "redux";
import thunk from "redux-thunk";

import { ApplicationState, reducers } from "./store";

export default function configureStore(history: History, initialState?: ApplicationState) {
  // Build middleware. These are functions that can process the actions before they reach the store.
  const windowIfDefined = typeof window === "undefined" ? null : (window as any);
  // If devTools is installed, connect to it
  //const devToolsExtension = windowIfDefined && windowIfDefined.__REDUX_DEVTOOLS_EXTENSION__ as () => GenericStoreEnhancer;

  const composeEnhancers = windowIfDefined.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

  const createStoreWithMiddleware = composeEnhancers(applyMiddleware(thunk, routerMiddleware(history)))(createStore);
  // Combine all reducers and instantiate the app-wide store instance
  const allReducers = buildRootReducer(reducers, history);
  const store = createStoreWithMiddleware(allReducers, initialState) as Store<ApplicationState>;

  return store;
}

function buildRootReducer(allReducers: ReducersMapObject, history: History) {
  return combineReducers<ApplicationState>(
    Object.assign({}, allReducers, {
      router: connectRouter(history)
    })
  );
}
