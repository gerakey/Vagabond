import React from 'react';
import { useFormik } from 'formik';

import { Button, Form } from 'react-bootstrap';

const SignIn = () => {

    const formik = useFormik({
        initialValues: {
            username: '',
            password: ''
        },
        onSubmit: (values) => {
            //TODO: Actually... you know, sign in.
            console.log(values);
        }
    });

    return (
        <>
            <h1>Sign in</h1>
            <hr />
            <Form onSubmit={formik.handleSubmit}>
                <Form.Group>
                    <Form.Label htmlFor="username">Username</Form.Label>
                    <Form.Control name="username" id="username" onChange={formik.handleChange} />
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="password">Password</Form.Label>
                    <Form.Control type="password" name="password" id="password" onChange={formik.handleChange} />
                </Form.Group>
                <Button variant="primary" type="submit">Sign in</Button>
    
            </Form>
        </>
    );

}

export default SignIn;