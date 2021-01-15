import React from 'react';
import { Switch, Route } from 'react-router-dom';

const Routes = () => {

    const Test = () => {
        return <p>Test</p>
    }

    const Home = () => {
        return <p>Home, sweet home.</p>
    }

    return (
        <Switch>
            <Route exact path="/" render={() =>  <Home/> } />
            <Route exact path="/test" render={() => <Test/>} />
        </Switch>
    );

}

export default Routes;