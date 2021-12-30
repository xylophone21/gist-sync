# -*- coding: utf-8 -*-
import click
from click.types import STRING

@click.group()
@click.pass_context
def main(context):
    context.obj = {"debug": False}

@main.command()
@click.option(
    '--root',
    default=".",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help='Root directory to sync.')
@click.option(
    '--user',
    default=None,
    type=STRING,
    help='Default gist user.')
@click.argument('token')
@click.pass_context
def build(context,root,token,user):
    click.echo('build:' + str(context))
    click.echo('build:' + str(root))
    click.echo('build:' + str(token))
    click.echo('build:' + str(user))

if __name__ == '__main__':
    main()