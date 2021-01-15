
import './App.css';
import Routes from './components/navigation/Routes.js';
import Navigation from './components/navigation/Navigation.js';
import {Container} from 'react-bootstrap';
import { BrowserRouter as Router } from 'react-router-dom';

const App = () => {

  const containerStyle = {
    marginTop: '15px'
  };

  return (
    <Router>
      <Navigation />
      <Container style={containerStyle}>
        <Routes />
      </Container>
    </Router>
  );
}

export default App;
