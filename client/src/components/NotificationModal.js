import React, { useState } from 'react';
import { store, initialState, hideNotification } from '../reducer/reducer.js';
import {Modal, Button} from 'react-bootstrap';

const NotificationModal = () => {

    const [notificationState, setNotificationState] = useState(initialState.notification);

    store.subscribe(() => {
        setNotificationState(store.getState().notification);
    })

    const hide = () => {
        store.dispatch(hideNotification());
    }

    return (
        <Modal show={notificationState.visible} onHide={hide}>
            <Modal.Header closeButton>
                <Modal.Title>{notificationState.title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>{notificationState.message}</Modal.Body>
            <Modal.Footer>
                <Button variant="primary" onClick={hide}>
                    OK
                </Button>
            </Modal.Footer>
        </Modal>
    );
}

export default NotificationModal;