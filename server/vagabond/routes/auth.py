from flask import make_response, request, session

import bcrypt

from vagabond.__main__ import app, db, limiter
from vagabond.models import User, Actor
from vagabond.routes import error
from vagabond.routes import require_args_json, require_signin

@app.route('/api/v1/signup', methods=['POST'])
#@limiter.limit('2 per day')
@require_args_json(['username', 'password', 'passwordConfirm', 'actorName'])
def route_signup():
    json = request.get_json()
    username = str(json.get('username')).lower()
    password = str(json.get('password'))
    password_confirm = str(json.get('passwordConfirm'))
    actor_name = str(json.get('actorName'))

    existing_user = db.session.query(User).filter(db.func.lower(User.username) == db.func.lower(username)).first()
    if existing_user != None:
        return error('That username is not available.', 400)

    existing_actor = db.session.query(Actor).filter(db.func.lower(Actor.username) == db.func.lower(actor_name)).first()
    if existing_actor != None:
        return error('That actor name is not available.', 400)

    if password != password_confirm:
        return error('Passwords don\'t match.', 400)

    new_user = User(username, password)
    db.session.add(new_user)
    db.session.flush()

    new_actor = Actor(actor_name, user_id=new_user.id)
    db.session.add(new_actor)

    db.session.commit()

    session['uid'] = new_user.id

    return make_response('', 201)



@app.route('/api/v1/signin', methods=['POST'])
#@limiter.limit('2 per minute')
@require_args_json(['username', 'password'])
def route_signin():
    json = request.get_json()
    username = str(json.get('username'))
    password = str(json.get('password'))

    if 'uid' in session:
        return error('You are currently signed in. Please sign out before trying to sign in.')

    err_msg = 'Invalid username or password.'

    user = db.session.query(User).filter(db.func.lower(User.username) == db.func.lower(username)).first()

    if user is None:
        return error(err_msg)
    
    if not bcrypt.checkpw(bytes(password, 'utf-8'), bytes(user.password_hash, 'utf-8')):
        return error(err_msg)

    session['uid'] = user.id

    return make_response('', 200)



@app.route('/api/v1/signout', methods=['POST'])
#@limiter.limit('2 per minute')
@require_signin
def route_signout(user):
    session.clear()
    return make_response('', 200)



@app.route('/api/v1/session')
@require_signin
def route_session(user):
    return make_response('', 200)