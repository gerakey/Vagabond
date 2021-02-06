import { Form, Button, Alert } from 'react-bootstrap';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { Link } from 'react-router-dom';
import { username as usernameRegex, actor as actorRegex } from '../../util/regex.js';
import axios from 'axios';
import { handleError, store } from '../../reducer/reducer.js';
import {useHistory} from 'react-router-dom';

const SignUp = () => {

    const history = useHistory();

    const initialValues = {
        username: '',
        password: '',
        passwordConfirm: '',
        actorName: ''
    }

    const validationSchema = Yup.object().shape({
        username: Yup.string()
            .required('Required')
            .max(32)
            .matches(usernameRegex, 'Usernames can only contain letters, numbers, hypens, and underscores.'),

        password: Yup.string()
            .required('Required')
            .min(12)
            .max(255),

        passwordConfirm: Yup.string()
            .required('Required')
            .min(12)
            .max(255)
            .oneOf([Yup.ref('password')], 'Passwords don\'t match!'),

        actorName: Yup.string()
            .required('Required')
            .max(32, 'Display name must be at most 32 characters')
            .matches(actorRegex, 'Display names can only contain letters, numbers, hypens, and underscores.')
    });

    const onSubmit = () => {
        axios.post('/api/v1/signup', formik.values)
            .then((res) => {
                store.dispatch({type: 'SET_SESSION', session: {...store.getState().session, signedIn: true, actors: res.data.actors}});
                history.push('/');
            })
            .catch(handleError);
    }

    const formik = useFormik({
        initialValues: initialValues,
        validationSchema: validationSchema,
        onSubmit: onSubmit
    });

    return (

        <>
            <h1>Sign Up</h1>
            <hr />
            <Alert variant="danger">
                <p>
                    <b>Vagabond accounts can only be used to sign in to the instance they were created on</b>.
                    You will not be able to use this account to log in to another Vagabond instance.
                    An instance claiming this is possible is likely trying to steal your information.
                </p>
            </Alert>
            <hr />
            <Form onSubmit={formik.handleSubmit}>
                <Form.Group>
                    <Form.Label htmlFor="username">Username</Form.Label>
                    <Form.Control onBlur={formik.handleBlur} id="username" name="username" placeholder="SteamTrainMaury" onChange={formik.handleChange} />
                    <Form.Text className="text-danger">{formik.getFieldMeta('username').touched && formik.errors.username}</Form.Text>
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="password">Password</Form.Label>
                    <Form.Control onBlur={formik.handleBlur} id="password" name="password" type="password" onChange={formik.handleChange} />
                    <Form.Text className="text-danger">{formik.getFieldMeta('password').touched && formik.errors.password}</Form.Text>
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="passwordConfirm">Confirm password</Form.Label>
                    <Form.Control onBlur={formik.handleBlur} id="passwordConfirm" name="passwordConfirm" type="password" onChange={formik.handleChange} />
                    <Form.Text className="text-danger">{formik.getFieldMeta('passwordConfirm').touched && formik.errors.passwordConfirm}</Form.Text>
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="actorName">Display name</Form.Label>
                    <Form.Control onBlur={formik.handleBlur} id="actorName" name="actorName" onChange={formik.handleChange} />
                    <Form.Text className="text-danger">{formik.getFieldMeta('actorName').touched && formik.errors.actorName}</Form.Text>
                </Form.Group>
                <Form.Text>Already have an account? Sign in <Link to="">here</Link>.</Form.Text>
                <br />
                <br />
                <Button type="submit" disabled={Object.keys(formik.errors).length > 0}>Sign up</Button>
            </Form>
        </>
    );

}

export default SignUp;