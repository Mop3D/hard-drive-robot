import './assets/styles/site.scss';
import React from 'react'
import ReactDOM from 'react-dom'
import { Route, BrowserRouter as Router, Switch } from 'react-router-dom'
import Overview from './components/pages/overview'
import RestCall from './components/pages/restcall'
import Notfound from './components/pages/NotFound'


const routing = (
  <Router>
      <Switch>
        <Route exact path="/" component={Overview} />
        <Route exact path="/restcall" component={RestCall} />
        <Route component={Notfound} />
      </Switch>
  </Router>
)
ReactDOM.render(routing, document.getElementById('root'))