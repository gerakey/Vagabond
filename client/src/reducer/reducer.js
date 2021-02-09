import { createStore } from 'redux';

const initialState = {
    notification: {
        visible: false,
        title: '',
        message: ''
    },
    session: {
        signedIn: false,
        actors: [],
        currentActor: {}
    },
};

const reducer = (state = initialState, action) => {
    if (action.type === 'CREATE_NOTIFICATION') {
        const newState = { ...state }
        newState.notification = {
            visible: true,
            title: action.title,
            message: action.message
        };
        return newState;
    } else if (action.type === 'HIDE_NOTIFICATION') {
        const newState = { ...state }
        newState.notification = {
            visible: false,
            title: '',
            message: ''
        };
        return newState;
    } else if (action.type === 'SET_SESSION') {
        
        return { ...state, session: action.session}
    } else {
        return state;
    }
};

const store = createStore(reducer, initialState);
store.getState();

const createNotification = (title, message) => {
    return {
        type: 'CREATE_NOTIFICATION',
        title: title,
        message: message
    };
};

const hideNotification = () => {
    return {
        type: 'HIDE_NOTIFICATION'
    };
};

const handleError = (err) => {
    if(err.response) {
        store.dispatch(createNotification(`Error: ${err.response.status}`, err.response.data));
    } else {
        store.dispatch(createNotification('Error', 'Unknown error.'));
        console.log(err);
    }
    
}



export { store, initialState, createNotification, hideNotification, handleError }
