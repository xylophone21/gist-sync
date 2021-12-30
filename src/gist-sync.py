# -*- coding: utf-8 -*-
import click

@click.group()
@click.pass_context
def main(context):
    context.obj = {"debug": False}

@main.command()
@click.argument(
    'root',
    type=click.Path(file_okay=False, resolve_path=True))
@click.argument(
    'token')
@click.pass_context
def build(context,root,token):
    click.echo('build:' + str(context))
    click.echo('build:' + str(root))
    click.echo('build:' + str(token))

if __name__ == '__main__':
    main()