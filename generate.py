#!/usr/bin/env python3

import json
import re
from functools import partial


TWEET_MARKER = re.compile('^\s*\d+/(?:\d+|End)?\s*$').match


def main():
    threads = list(publishable_threads())
    for thread in threads:
        publish_thread(thread)


def stories():
    with open('tweets/tweets.json') as f:
        yield from json.load(f)


def publishable_threads():
    return filter(is_publishable, stories())


def is_publishable(thread):
    return bool(thread.get('title'))


def publish_thread(thread):
    id = thread['id']
    description = generate_description(thread)
    with open(f'tweets/{id}.md', 'w') as f:
        emit = partial(print, file=f)
        emit('---')
        emit('layout: thread')
        emit(f'title: {thread["title"]}')
        emit(f'description: {description}')
        emit(f'date: {thread["published"]}')
        emit(f'twid: {id}')
        emit('tags:')
        for tag in thread['tags']:
            emit(f'  - {tag}')
        emit('links:')
        for link in thread['links']:
            if link["id"]:
                emit(f'  - name: "{link["name"]}"')
                emit(f'    id: "{link["id"]}"')
        emit('---')
        emit('<article class="thread">')
        for tweet in thread["tweets"][:-1]:
            emit('<section class="tweet">')
            for para in paragraphs(tweet['full_text']):
                if TWEET_MARKER(para):
                    continue
                emit('<p>', end='')
                emit(para, end='')
                emit('</p>')
            emit('</section>')
            emit('<hr class="tweet_sep">')
        emit('<section class="tweet">')
        for para in paragraphs(thread['tweets'][-1]['full_text']):
            if TWEET_MARKER(para):
                continue
            emit('<p>', end='')
            emit(para, end='')
            emit('</p>')
        emit('</section>')
        emit('</article>')


def generate_description(thread):
    text = thread["tweets"][0]["full_text"]
    return paragraphs(text)[0]


def paragraphs(text):
    return list(filter(bool, text.split('\n')))


if __name__ == '__main__':
    main()
