#!/usr/bin/python3
import os
import oauth
import json
from json import JSONDecoder, JSONEncoder

decoder = JSONDecoder()
encoder = JSONEncoder()

user_name = ''
client_key = ''
client_secret = ''
URL = 'http://api.egloos.com/{}/post.json?page='.format(user_name)
POST_URL = 'http://api.egloos.com/{}/post/'.format(user_name)

req = oauth.get_request_token(client_key, client_secret)
verifier = oauth.get_oauth_verifier(req['oauth_session'])
acc = oauth.get_access_token(client_key, client_secret, req['oauth_token'],
    req['oauth_token_secret'], verifier)

def is_saved(path):
    try:
        os.stat(path)
        return True
    except FileNotFoundError:
        return False

post_index = []
post_list = []

page_max = 11

try:
    os.stat('post_index.json')
    f = open('post_index.json', encoding='utf-8')
    post_index_json = f.read()
    post_index = decoder.decode(post_index_json)
    print('file opened: post_index.json')
except FileNotFoundError:
    for i in range(1, page_max + 1):
        url = URL + str(i)
        r = oauth.request(client_key, client_secret, acc['oauth_token'],
                            acc['oauth_token_secret'], url)
        py_li = decoder.decode(r.content.decode())
        posts = py_li['post']
        for p in posts:
            post_index.append(p)

print('sorting by date ...')
post_index.sort(key=lambda post: post['post_date_created'])
print('done')

print('get indexes total ' + str(len(post_index)))
act = ''
while act != 'b':
    act = input('action [l: list all / b: begin iterate / s: save]: ')
    if act == 'l':
        for p in post_index:
            print(p['post_title'])
            print(p['post_date_created'])
            print('hidden? ' + str(p['post_hidden']))
            print('---------------------------------------')
        print('')
    elif act == 's':
        post_index_json = encoder.encode(post_index)
        f = open('post_index.json', encoding='utf-8', mode='w')
        f.write(post_index_json)
        f.close()
        print('saved to post_index.json')

for p in post_index:
    fetch = None
    filename = p['post_date_created'].replace(' ', '_')
    act = ''
    while act != 'n':
        print(p['post_title'])
        print(p['post_no'])
        print(p['post_date_created'])
        print('hidden? ' + str(p['post_hidden']))
        act = input('action [p: print / n: next / s: save and next / q: saved?]: ')
        if act == 'p':
            if fetch == None:
                url = POST_URL + p['post_no'] + '.json'
                r = oauth.request(client_key, client_secret,
                        acc['oauth_token'], acc['oauth_token_secret'], url)
                py_li = decoder.decode(r.content.decode())
                try:
                    fetch = py_li['post']
                except KeyError:
                    print(r.content.decode())
            print('')
            print('title: ' + fetch['post_title'])
            print('no: ' + str(fetch['post_no']))
            print('content: ')
            print(fetch['post_content'])
            print('category: ' + fetch['category_name'])
            print('category_no: ' + str(fetch['category_no']))
            print('name: ' + fetch['post_nick'])
            print('comments: ' + str(fetch['comment_count']))
            print('trackbacks: ' + str(fetch['trackback_count']))
            print('hidden? ' + str(fetch['post_hidden']))
            print('commend allowed? ' + str(fetch['comment_enabled']))
            print('trackback allowed? ' + str(fetch['trackback_enabled']))
            print('date: ' + fetch['post_date_created'])
            print('update: ' + fetch['post_date_modified'])
            print('tags: ' + fetch['post_tags'])
            print('-------------------------------------------')
        elif act == 's':
            if fetch == None:
                url = POST_URL + p['post_no'] + '.json'
                r = oauth.request(client_key, client_secret,
                        acc['oauth_token'], acc['oauth_token_secret'], url)
                py_li = decoder.decode(r.content.decode())
                try:
                    fetch = py_li['post']
                except KeyError:
                    print('an error occured! > <')
            post_json = encoder.encode(fetch)
            if is_saved('posts/' + filename) == False:
                f = open('posts/' + filename, encoding='utf-8', mode='w')
                f.write(post_json)
                f.close()
                print('saved to posts/' + filename)
            else:
                print('file already saved at posts/' + filename)
            break
        elif act == 'a':
            # hidden post could not be fetched (bug)
            if str(p['post_hidden']) != '1' and is_saved('posts/' + filename) == False:
                # not implemented
                '''
                if fetch == None:
                    url = POST_URL + p['post_no'] + '.json'
                    r = oauth.request(client_key, client_secret,
                            acc['oauth_token'], acc['oauth_token_secret'], url)
                    py_li = decoder.decode(r.content.decode())
                    fetch = py_li['post']
                post_json = encoder.encode(fetch)
                f = open('posts/' + filename, encoding='utf-8', mode='w')
                f.write(post_json)
                f.close()
                print('saved to posts/' + filename)
                break
                '''
        elif act == 'q':
            if is_saved('posts/' + filename) == True:
                print('yes! :)')
                print('')
            else:
                print('not yet')
                print('')

print('== end ==')
