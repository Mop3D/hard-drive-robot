import './assets/styles/site.scss';
import React from 'react'
import ReactDOM from 'react-dom'
import { Route, BrowserRouter as Router, Switch } from 'react-router-dom'
import Overview from './components/pages/overview'
import RestCall from './components/pages/restcall'
import Notfound from './components/pages/NotFound'

import { Provider } from 'react-redux';
import { createBrowserHistory } from "history";
import initialState from "./initialState";
import configureStore from "./configureStore";

// Create browser history to use in the Redux store
const history = createBrowserHistory();

export const store = configureStore(history, initialState);

const providerStore = (
  <Provider store={store}>
    <Router>
        <Switch>
          <Route exact path="/" component={Overview} />
          <Route exact path="/restcall" component={RestCall} />
          <Route component={Notfound} />
        </Switch>
    </Router>
  </Provider>
)
ReactDOM.render(providerStore, document.getElementById('root'))