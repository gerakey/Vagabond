import { createStore } from 'redux';

const initialState = {
    notification: {
        visible: false,
        title: '',
        message: ''
    },
    userData: {
        signedIn: false
    }
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
    } else if (action.type === '') {
        //TODO: Log in / log out
    }
};

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

const store = createStore(reducer);

export { store, initialState, createNotification, hideNotification }
