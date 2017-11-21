from bottle import route, run, template, request, response, static_file
import requests
import urllib2
import re
import json

DECIDE_CALL = '{ %s(id: %s) { id cached_votes_up comments_count confidence_score description hot_score public_author { id username } public_created_at tags(first: 10) { edges { node { id name } } } comments(first: 50, after: "%s") { pageInfo { hasNextPage endCursor } edges { node { public_author { id username } cached_votes_up cached_votes_down public_created_at id body ancestry } } } title } }'

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')


@route('/fonts/<filename>')
def server_static(filename):
    return static_file(filename, root='./fonts')

@route('/thread/')
def index():

    type = request.query.type
    id = request.query.id

    endCursor = ''
    r = requests.post('https://decide.madrid.es/graphql', data = {'query': DECIDE_CALL % (type, id, endCursor)})
    thread_json = json.loads(str(r.content))['data'][type]
    thread_json['depth'] = 0
    thread_json['body'] = thread_json['description']
    thread_json.pop('summary', None)
    if not 'cached_votes_down' in thread_json:
        thread_json['cached_votes_down'] = 0
    thread_json['children'] = []

   
    hasNextPage = True
    while hasNextPage:
        comments = json.loads(str(r.content))['data'][type]['comments']['edges']
        for comment in comments:
            node = comment['node']
            node['children'] = []
            node_id = str(node['id'])
            del node['id']
            node['id'] = node_id
            ancestry = node['ancestry']
 
            if ancestry is None:
                node['depth'] = 1
                found = False
                for child in thread_json['children']:
                    if str(child['id']) == str(node['id']):
                        found = True
                        for key in node:
                            if key != 'children':
                                child[key] = node[key]
                if not found:                    
                    thread_json['children'].append(node)
            
            else:
                parent = thread_json['children']
                ancestors = ancestry.split('/')
                node['depth'] = 1+len(ancestors)
                for ancestor in ancestors:
                    found = False
                    for candidate_parent in parent:
                        if int(candidate_parent['id']) == int(ancestor):
                            parent = candidate_parent['children']
                            found = True
                    if not found:
                        temp = {}
                        temp['id'] = int(ancestor)
                        temp['children'] = []
                        parent.append(temp)
                        parent = temp['children']
                found = False
                for child in parent:
                    if str(node['id']) == str(child['id']):
                        found = True
                        for key in node:
                            if key != 'children':
                                child[key] = node[key]
                if not found:
                    parent.append(node)

        thread_json.pop('comments', None)
        r = requests.post('https://decide.madrid.es/graphql', data = {'query': DECIDE_CALL % (type, id, endCursor)})
        endCursor =  json.loads(str(r.content))['data'][type]['comments']['pageInfo']['endCursor']
        hasNextPage = json.loads(str(r.content))['data'][type]['comments']['pageInfo']['hasNextPage']

    # Dump data into data.json
    f=open('./static/data.json','w')
    f.write(json.dumps(thread_json , sort_keys=False, indent=4, separators=(',', ': ')) )
    f.close()

    # Return index.html
    f = open('./static/index.html')
    a = f.read()
    f.close()
    return template(a)

run(host='localhost', server='tornado', port=8080, debug=True)
