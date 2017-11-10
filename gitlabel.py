"""gitlabel - CLI tool for managing GitHub labels"""
import json

import click
import ghlib
import requests

@click.command()
@click.option('-i', '--infile', default='',
              help='infile (.json file or owner/repo)', metavar='<str>')
@click.option('-o', '--output', default='',
              help='output (.json file or owner/repo)', metavar='<str>')

def cli(infile, output):
    """command line interface - main entry point"""
    if not infile:
        click.echo('ERROR: must specify -i or --infile')
        return
    label_set = read(infile)
    # if want to do anything with the label set, here's where to do it
    write(label_set, output)

def read(infile):
    """Read from a .json file or owner/repo."""

    if infile.lower().endswith('.json'):
        return json.loads(open(infile).read()) # read from JSON file

    return read_repo(org_repo=infile) # read from repo

def read_repo(org_repo):
    """Read label definitions from a GitHub owner/repo, return label set."""
    return [{'name': label['name'],
             'color': label['color']}
            for label in ghlib.github_allpages(endpoint=f'/repos/{org_repo}/labels')]

def write(labelset, output):
    """Write to .json file or owner/repo (or console)."""
    if output.lower().endswith('.json'):
        with open(output, 'w') as fhandle:
            fhandle.write(json.dumps(labelset, indent=4))
    elif output:
        return write_repo(labelset, org_repo=output)
    elif labelset:
        click.echo('[\n    ', nl=False)
        click.echo(',\n    '.join([json.dumps(label) for label in labelset]))
        click.echo(']')

def write_repo(labelset, org_repo):
    """Write a label set to a GitHub owner/repo."""

    # create a list of the labels currently defined in this repo
    labels_before = [label['name'] for label in read_repo(org_repo)]

    # create a list of the new labels to be added to the repo
    to_add = [label['name'] for label in labelset if not label['name'] in labels_before]

    click.echo('NEW LABELS TO ADD: ' + ', '.join(to_add))
    prompt = f'{len(to_add)} LABELS WILL BE ADDED TO {org_repo.upper()}. PROCEED?'
    if not click.confirm(prompt, default=False, abort=True):
        return

    # convert labelset into a dictionary of name-color mappings
    colors = {label['name']:label['color'] for label in labelset}

    for label_name in to_add:
        response = requests.post(url=f'https://api.github.com/repos/{org_repo}/labels',
                                 headers={'Accept': 'application/vnd.github.v3+json'},
                                 data=json.dumps({"name": label_name, "color": colors[label_name]}),
                                 auth=ghlib.auth_tuple())
        if response.ok:
            click.echo('Label added: ' + label_name)
        else:
            click.echo(f'ERROR ({response.status_code}) adding label: ' + label_name)
