#!/usr/local/bin/python3

# this was modified from an older version of https://tildegit.org/ben/toot

import json
import os
import sys

import click
import emoji
from mastodon import Mastodon

# get config
path = os.getenv('TOOT_JSON_PATH', os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(path, '../misc/toot.json')
with open(config_file) as f:
    config = json.load(f)

# set up connection to mastodon
mastodon = Mastodon(
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    access_token=config['access_token'],
    api_base_url=config['base_url'],
)

def check_valid_files(ctx, param, filenames):
    if filenames:
        if len(filenames) > 4:
            raise click.BadParameter('too many files!')
        for filename in filenames:
            if not os.path.isfile(filename):
                raise click.BadParameter('"{}" is not a valid file'.format(filename))
    return filenames

def post_to_masto(status, media):
    files = []
    for fname in media:
        media_info = mastodon.media_post(fname)
        files.append(media_info)
    if not files:
        files = None
    mastodon.status_post(status, media_ids=files)


@click.command()
@click.argument('status', required=False)
@click.option('--media', '-m', multiple=True, callback=check_valid_files)
def toot(status, media):
    # get status from argument or from stdin
    if not status:
        status = "".join(sys.stdin).strip()

    # replace shortcodes with emoji :thumbsup:
    status = emoji.emojize(status, language='alias')

    # check status length and post status
    if len(status) > 500:
        print("Status is too long, try again")
    elif len(status) == 0:
        print("Did you type a status?")
    else:
        post_to_masto(status, media)



if __name__=='__main__':
    toot()

