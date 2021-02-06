
import { ReactComponent as LogoHome } from '../../icon/home.svg'
import { ReactComponent as LogoUser } from '../../icon/user.svg'
import { ReactComponent as LogoUsers } from '../../icon/users.svg'
import { ReactComponent as SignIn } from '../../icon/sign-in.svg'
import { ReactComponent as SignOut } from '../../icon/sign-out.svg'
import { ReactComponent as Info } from '../../icon/info.svg'
import { ReactComponent as Feather } from '../../icon/feather.svg'

import { initialState, store, handleError } from '../../reducer/reducer.js';

import { useState, useEffect } from 'react';

import { Link } from 'react-router-dom';

import axios from 'axios';

const Navigation = () => {

    const [session, setSession] = useState(initialState.session);

    useEffect(() => {
        store.subscribe(() => {
            setSession(store.getState().session);
        });
    }, []);

    const signOut = () => {
        axios.post('/api/v1/signout')
        .then((res) => {
            store.dispatch({type: 'SET_SESSION', session: {...store.getState().session, signedIn: false}});
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
            <Link to="/actors" title="All actors">
                <LogoUsers />
            </Link>
            <Link className="mobile-icon" to="/compose" title="Compose Note">
                <Feather />
            </Link>
            <Link to="/about" title="About">
                <Info />
            </Link>



        </div>
    );

}

export default Navigation;