
import Routes from './components/navigation/Routes.js';
import Navigation from './components/navigation/Navigation.js';
import { BrowserRouter as Router } from 'react-router-dom';
import NotificationModal from './components/NotificationModal.js';
import './css/App.css';

const App = () => {


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
