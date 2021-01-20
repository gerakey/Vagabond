
import './App.css';
import Routes from './components/navigation/Routes.js';
import Navigation from './components/navigation/Navigation.js';
import { Container } from 'react-bootstrap';
import { BrowserRouter as Router } from 'react-router-dom';
import NotificationModal from './components/NotificationModal.js';

const App = () => {

  const containerStyle = {
    marginTop: '15px'
  };

  return (
    <>
      <NotificationModal/>
      <Router>
        <Navigation />
        <Container style={containerStyle}>
          <Routes />
        </Container>
      </Router>
    </>
  );
}

export default App;
