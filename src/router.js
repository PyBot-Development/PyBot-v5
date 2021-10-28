import React from 'react';
import { Route, Redirect, BrowserRouter, Switch } from 'react-router-dom';

import NotFound from './sites/404/index';
import Home from './sites/home/index'
import About from './sites/about/index'
import Changelog from './sites/changelog/index'
import Commands from './sites/commands/index'
import HowTo from './sites/add/index'


import Header from './components/header/index'
import Footer from './components/footer/index';

function createRoute(path, component, headerAndFooter = false, headerText = "Not Specified.") {

  return (
    <Route exact path={path} key={path}>
      {headerAndFooter ? <Header text={headerText} /> : ''}
      {component}
      {headerAndFooter ? <Footer /> : ''}
    </Route>
  )
}

const Routes = () => {
  return (
    <>
      <BrowserRouter>
        <Switch>
          {createRoute(["/404"], <NotFound />, false)}
          {createRoute(["/home", "/", ""], <Home />, true, "🏡 Home")}
          {createRoute(["/about", "/", ""], <About />, true, "🤔 About")}
          {createRoute(["/changelog", "/", ""], <Changelog />, true, "🖨️ Changelog")}
          {createRoute(["/commands", "/", ""], <Commands />, true, "💾 Commands")}
          {createRoute(["/add"], <HowTo />, true, "ℹ️ How to?")}
          
          <Redirect to="/404" />
        </Switch>
      </BrowserRouter>
    </>
  );
};

export default Routes;