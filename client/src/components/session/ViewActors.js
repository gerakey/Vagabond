import React from 'react';

const ViewActors = (props) => {

    return (

        <>
            <h1>Your Actors</h1>
            <hr />
            {
                props.actors.map(
                    (actor, index) =>
                        <>
                            <code>{JSON.stringify(actor, null, 2)}</code>
                            <br />
                            <br />
                            <br />
                        </>
                )
            }
        </>
    );
}

export default ViewActors;