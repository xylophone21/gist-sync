# -*- coding: utf-8 -*-
import click
import os
import markdown

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
    type=click.types.STRING,
    help='Default gist user.')
@click.argument('token')
@click.pass_context
def build(context,root,token,user):
    context.root = root
    context.token = token
    context.user = user
    click.echo('build:' + str(context.root) + ':' + str(context.token) + ':' + str(context.user))

    for parent,dirnames,filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith('.md'):
                click.echo("generate for" + os.path.join(parent,filename))
                parser = markdown.MarkdownParser(os.path.join(parent,filename), user, token)
                parser.parse()
                click.echo(":" + parser.url)
                click.echo(":" + parser.gistId)
                click.echo(":" + parser.user)

if __name__ == '__main__':
    main()