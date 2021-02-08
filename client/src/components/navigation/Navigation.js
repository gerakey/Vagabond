
import { ReactComponent as LogoHome } from '../../icon/home.svg'
import { ReactComponent as LogoUser } from '../../icon/user.svg'
import { ReactComponent as LogoUsers } from '../../icon/users.svg'
import { ReactComponent as SignIn } from '../../icon/sign-in.svg'
import { ReactComponent as SignOut } from '../../icon/sign-out.svg'
import { ReactComponent as Info } from '../../icon/info.svg'
import { ReactComponent as Feather } from '../../icon/feather.svg'

import { initialState, store } from '../../reducer/reducer.js';

import { useState, useEffect } from 'react';

import { Link } from 'react-router-dom';

const Navigation = () => {

    const [userData, setUserData] = useState(initialState.userData);

    useEffect(() => {
        store.subscribe(() => {
            setUserData(store.getState().userData);
        })
    }, []);

    return (
        <div class="vagabond-navbar">
            
            <Link to="/" title="Home">
                <div id="vagabondTitle">Vagabond</div>
            </Link>
            
            <div id="iconsBar">
                <Link to="/" title="Home">
                    <LogoHome/>
                </Link>


                {
                   !userData.signedIn &&
                  <Link to="/signin" title="Sign in">
                      <SignIn/>
                  </Link>
               }
                {
                    userData.signedIn &&
                    <Link to="/signout" title="Sign out">
                        <SignOut/>
                    </Link>
                }

                <Link to="/actors" title="All actors">
                    <LogoUsers/>
                </Link>
                <Link to="/compose" title="Compose Note">
                    <Feather/>
                </Link>
                <Link to="/about" title="About">
                    <Info/>
                </Link>
            </div>


        </div>
    );

}

export default Navigation;