import React from 'react';
import { Route, Redirect, BrowserRouter, Switch } from 'react-router-dom';
import App from './sites/home/index'
import Header from './components/header/index'
import Footer from './components/footer/index';
import NotFound from './sites/404/index';
function createRoute(path, component, headerAndFooter=false, headerText="Not Specified.") {

  return (
    <Route exact path={path} key={path}>
      {headerAndFooter ? <Header text={headerText} /> : ''}
      {component}
      {headerAndFooter ? <Footer/> : ''}
    </Route>
  )
}

const Routes = () => {
  return (
    <>
        <BrowserRouter>
                <Switch>
                    {createRoute(["/404"], <NotFound />, false)}
                    {createRoute(["/home", "/", ""], <App />, true, "🏡 Home")}

                    <Redirect to="/404" />
                </Switch>
        </BrowserRouter>
    </>
  );
};

export default Routes;