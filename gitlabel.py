"""gitlabel - CLI tool for managing GitHub labels"""
import json

import click
import githuberino
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
        return json.loads(open(infile).read())
    else:
        return read_repo(org_repo=infile)

def read_repo(org_repo):
    """Read label definitions from a GitHub owner/repo, return label set."""
    return [{'name': label['name'],
             'color': label['color']}
            for label in githuberino.github_allpages(endpoint=f'/repos/{org_repo}/labels')]

def write(labelset, output):
    """Write to .json file or owner/repo (or console)."""
    if output.lower().endswith('.json'):
        with open(output, 'w') as fhandle:
            fhandle.write(json.dumps(labelset, indent=4))
    elif output:
        return write_repo(labelset, org_repo=output)
    else:
        click.echo('[\n    ', nl=False)
        click.echo(',\n    '.join([json.dumps(label) for label in labelset]))
        click.echo(']')

def write_repo(labelset, org_repo):
    """Write a label set to a GitHub owner/repo."""

    labels_before = read_repo(org_repo)

    #/// need a final prompt here:
    #    - show existing labels, how many will be added
    #    - prompt for whether to proceed

    for label in labelset:
        if not label['name'] in labels_before:
            click.echo('Label added: ' + label['name'])
            pass #/// add this label

    print(f'/// write_repo({org_repo})')
