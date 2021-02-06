
import Routes from './components/navigation/Routes.js';
import Navigation from './components/navigation/Navigation.js';
import { BrowserRouter as Router } from 'react-router-dom';
import NotificationModal from './components/NotificationModal.js';
import './css/App.css';
import {store, initialState} from './reducer/reducer.js';
import { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {

  const[session, setSession] = useState(initialState.session);
  
  store.subscribe(() => {
    setSession(store.getState().session);
  })

  useEffect(() => {
    axios.get('/api/v1/session')
    .then((res) => {
      store.dispatch({type: 'SET_SESSION', session: {...session, signedIn: true}});
    })
    .catch((err) => {
      //Do nothing
    });
  }, []);


  return (
    <>
      <NotificationModal />
      <Router>
        <Navigation />
        <div id="container-root">
          <div id="sidebar-left">
            Left sidebar (compose new note)
          </div>
          <div id="container-center">
            <Routes />
          </div>
          <div id="sidebar-right">
            Right sidebar (people you follow)
          </div>
        </div>
      </Router>
    </>
  );
}

export default App;
