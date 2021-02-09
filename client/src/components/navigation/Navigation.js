
import { ReactComponent as LogoHome } from '../../icon/home.svg'
import { ReactComponent as LogoUsers } from '../../icon/users.svg'
import { ReactComponent as SignIn } from '../../icon/sign-in.svg'
import { ReactComponent as SignOut } from '../../icon/sign-out.svg'
import { ReactComponent as Info } from '../../icon/info.svg'
import { ReactComponent as Feather } from '../../icon/feather.svg'
import { ReactComponent as Globe } from '../../icon/globe.svg'

import { initialState, store, handleError } from '../../reducer/reducer.js';

import { useState, useEffect } from 'react';

import { Link, useHistory } from 'react-router-dom';

import axios from 'axios';

const Navigation = () => {

    const [session, setSession] = useState(initialState.session);

    const history = useHistory();

    useEffect(() => {
        store.subscribe(() => {
            setSession(store.getState().session);
        });
    }, []);

    const signOut = () => {
        axios.post('/api/v1/signout')
            .then((res) => {
                store.dispatch({ type: 'SET_SESSION', session: initialState.session });
                history.push('/');
            })
            .catch(handleError)
    }

    return (
        <div className="vagabond-navbar">
            <Link to="/" title="Home">
                <LogoHome />
            </Link>
            {
                !session.signedIn &&
                <Link to="/signin" title="Sign in">
                    <SignIn />
                </Link>
            }
            {
                session.signedIn &&
                <Link onClick={signOut} to="#" title="Sign out">
                    <SignOut />
                </Link>
            }
            {
                session.signedIn &&
                <Link to="/actors" title="All actors">
                    <LogoUsers />
                </Link>
            }

            {
                session.signedIn && 
                <Link to="/compose" title="Compose Note">
                    <Feather />
                </Link>
            }

            <Link to="/about" title="About">
                <Info />
            </Link>

            <Link to="/feed" title="Feed">
                <Globe />
            </Link>

        </div>
    );

}

export default Navigation;