
import Routes from './components/navigation/Routes.js';
import Navigation from './components/navigation/Navigation.js';
import { BrowserRouter as Router } from 'react-router-dom';
import NotificationModal from './components/NotificationModal.js';
import './css/App.css';
import { store } from './reducer/reducer.js';
import { useEffect } from 'react';
import axios from 'axios';

import { Container } from 'react-bootstrap';

const App = () => {

  useEffect(() => {
    axios.get('/api/v1/session')
      .then((res) => {
        store.dispatch({ type: 'SET_SESSION', session: { ...store.getState().session, ...res.data } });
      })
      .catch((err) => { });
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

            <Container>
              <Routes />
            </Container>


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
