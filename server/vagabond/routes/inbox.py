from math import ceil

from flask import request, make_response

from vagabond.routes import error, require_signin
from vagabond.__main__ import app, db
from vagabond.crypto import require_signature
from vagabond.config import config
from vagabond.models import Actor, Following, Follow, APObjectRecipient, Create, Note
from vagabond.util import resolve_ap_object

from dateutil.parser import parse


def modify_follow(actor, activity, obj):
    '''
        Incoming Accept and Reject activites on Follow objects
        have side effects which are handled here
    '''

    following = db.session.query(Following).filter(db.and_(
        Following.follower_id == actor.id,
        Following.leader == activity['actor']),
        Following.approved == 0
    ).first()

    follow_activity = db.session.query(Follow).filter(db.and_(
        Follow.external_object_id == obj['object'],
        Follow.internal_actor_id == actor.id
    )).first()

    if following is None or follow_activity is None:
        return error('Follow request not found.', 404)

    if activity['type'] == 'Accept':
        following.approved = True
        db.session.add(following)
    else:
        db.session.delete(following)

    db.session.delete(follow_activity)
    

    db.session.commit()

    return make_response('', 200)



def new_ob_object(activity, obj, recipient=None):
    '''
        ?recipient: dict
            the actor whose inbox this activity was POSTed to
        activity: dict
            The activity being preformed
        ?obj: dict
            The object the activity is being done on


        Returns: Flask Response object


        To avoid repetition, this function is used to process
        ALL inbound APObjects to an actor's inbox regardless as
        to the type. Special behavior for certain kinds of incoming
        objects is to be handled on a case-by-case basis.

        The newly created objects are added to the database, flushed, and committed.
    '''

    base_activity = None
    base_object = None

    if activity['type'] == 'Create':
        base_activity = Create()
    elif (activity['type'] == 'Accept' or activity['type'] == 'Reject') and obj['type'] == 'Follow' and recipient is not None:
        return modify_follow(recipient, activity, obj)
    else:
        return error('Invalid request. That activity type may not supported by Vagabond.', 400)
          
    if obj is not None:
        if obj['type'] == 'Note':
            base_object = Note()

    #Assign common properties to the generic activity
    db.session.add(base_activity)
    db.session.flush()
    base_activity.external_id = activity['id']
    base_activity.external_actor_id = activity['actor']
    base_activity.published = parse(activity['published'])
    base_activity.add_all_recipients(activity)
    if obj is not None:
        base_activity.external_object_id = obj['id']


    #assign common properties to the generic object
    if base_object is not None:
        db.session.add(base_object)
        db.session.flush()
        base_object.external_id = obj['id']
        base_object.published = parse(obj['published'])
        base_object.attribute_to(obj['attributedTo'])
        base_object.add_all_recipients(obj)
        if 'content' in obj:
            base_object.content = obj['content']

    db.session.commit()
    return make_response('', 200)



@require_signin
def get_inbox(personalized, user=None):

    '''
        if personalized == True:
            the route is /api/v1/actors/<actor_name>/inbox
        if personalized == False:
            the route is /api/v1/inbox

        This is not an arbitrary distinction and the AP spec dictates
        the difference in behavior between the two.
    '''

    actor = user.primary_actor

    api_url = config['api_url']

    # Figure out who the actor is following and put that into a list
    # Do another query for all isntances of APObjectRecipient where the recipiet is contained inside he previously generated list

    leaders = db.session.query(Following).filter(Following.follower_id == actor.id).all()
    followers_urls = []
    for leader in leaders:
        followers_urls.append(leader.followers_collection)

    total_items = db.session.query(APObjectRecipient).filter(APObjectRecipient.recipient.in_(followers_urls)).count()
    items_per_page = 20
    max_page = ceil(total_items / items_per_page)

    root_url = None
    if personalized:
        root_url = f'{api_url}/actors/{actor.username}/inbox'
    else:
        root_url = f'{api_url}/inbox'

    output = {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': f'{root_url}',
        'type': 'OrderedCollection',
        'totalItems': total_items,
        'first': f'{root_url}/1',
        'last': f'{root_url}/{max_page}'
    }

    response = make_response(output)
    response.headers['content-type'] = 'application/activity+json'
    return response



def get_inbox_paginated(actor, page, personalized):

    leaders = db.session.query(Following).filter(Following.follower_id == actor.id).all()
    followers_urls = []
    for leader in leaders:
        followers_urls.append(leader.followers_collection)

    recipient_objects = db.session.query(APObjectRecipient).filter(APObjectRecipient.recipient.in_(followers_urls)).paginate(page, 20).items

    ordered_items = []

    for recipient_object in recipient_objects:
        ordered_items.append(recipient_object.ap_object.to_dict())

    api_url = config['api_url']

    root_url = None
    if personalized:
        root_url = f'{api_url}/actors/{actor.username}/inbox'
    else:
        root_url = f'{api_url}/inbox'

    output = {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': f'{root_url}/{page}',
        'partOf': f'{root_url}/inbox',
        'type': 'OrderedCollectionPage',
        'prev': f'{root_url}/{page-1}',
        'next': f'{root_url}/{page+1}',
        'orderedItems': ordered_items
    }

    response = make_response(output)
    response.headers['content-type'] = 'application/activity+json'
    return response


@require_signin
def get_actor_inbox(actor_name, user=None):

    actor_name = actor_name.lower()

    has_permission = False
    for _actor in user.actors:
        if _actor.username.lower() == actor_name:
            has_permission = True
            break

    if has_permission:
        return get_inbox(personalized=True)
    else:
        #TODO: Non-watseful way of figuring out which notes go to who
        return error('You can only view your own inbox, not someone else\'s!')

    

@require_signature
@app.route('/api/v1/actors/<actor_name>/inbox', methods=['GET', 'POST'])
def route_actor_inbox(actor_name):
    
    if request.method == 'POST':
        activity = request.get_json()
        recipient = db.session.query(Actor).filter_by(username=actor_name.lower()).first()

        if recipient is None:
            return error('The specified actor could not be found.', 404)

        obj = resolve_ap_object(request.get_json().get('object'))

        return new_ob_object(activity, obj, recipient)

    elif request.method == 'GET':
        return get_actor_inbox(actor_name=actor_name)


@app.route('/api/v1/actors/<actor_name>/inbox/<int:page>')
@require_signin
def route_actor_inbox_paginated(user, actor_name, page):

    has_permission = False
    actor = None
    for _actor in user.actors:
        if _actor.username.lower() == actor_name.lower():
            has_permission = True
            actor = _actor
            break

    if not has_permission:
        return error('You can only view your own inbox, not someone else\'s!')

    return get_inbox_paginated(actor, page, personalized=True)


@app.route('/api/v1/inbox', methods=['GET', 'POST'])
def route_shared_inbox():
    if request.method == 'GET':
        return get_inbox(personalized=False)
    elif request.method == 'POST':
        activity = request.get_json()
        obj = resolve_ap_object(activity['object'])

        return new_ob_object(activity, obj)


@app.route('/api/v1/inbox/<int:page>')
@require_signin
def route_shared_inbox_paginated(user, page):

    if request.method == 'GET':
        actor = user.primary_actor
        return get_inbox_paginated(actor, page, personalized=False)