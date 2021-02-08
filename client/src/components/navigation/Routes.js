import React from 'react';
import { Switch, Route } from 'react-router-dom';
import Error404 from '../static/Error404.js';
import About from '../static/About.js';
import SignIn from '../session/SignIn.js';
import Home from '../static/Home/Home.js'

const Routes = () => {

    const Test = () => {
        return <p>Test</p>
    }

   

    return (
        <Switch>
            <Route exact path="/" render={() => <Home />} />
            <Route exact path="/test" render={() => <Test />} />
            <Route exact path="/about" render={() => <About />} />
            <Route exact path="/signin" render={() => <SignIn />} />
            <Route render={() => <Error404 />} />
        </Switch>
    );

}

export default Routes;