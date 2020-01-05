import * as React from "react";
import { Route, Switch } from "react-router-dom";

import Overview from "./components/pages/overview";

export const routes = (
  <Switch>
    <Route path="/" exact={true} component={Overview} />
{/*
    <Route path="/search" component={Search} />
*/}
    <Route path="/*" component={Overview} />
  </Switch>
);
