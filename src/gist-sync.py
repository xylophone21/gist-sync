# -*- coding: utf-8 -*-
import click
import os
import sys
import markdown
import gitopt
import shutil

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
@click.option(
    '--workpath',
    default="/tmp/gist-sync",
    type=click.Path(file_okay=False, resolve_path=True),
    help='Tmp folder to work.')
@click.argument('token')
@click.pass_context
def build(context,root,token,user,workpath):
    context.root = root
    context.token = token
    context.user = user
    # click.echo('build:' + str(context.root) + ':' + str(context.token) + ':' + str(context.user))

    if os.path.exists(workpath):
        shutil.rmtree(workpath)
    os.makedirs(workpath)

    err = 0

    for parent,dirnames,filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith('.md'):
                parser = markdown.MarkdownParser(os.path.join(parent,filename), token ,user)
                ret = parser.parse()
                if not ret:
                    click.echo("Not share:" + os.path.join(parent,filename) )
                    continue

                gitopt.checkoutGist(workpath, parser.user, parser.token, parser.gistId)

                ret = parser.syncTo(workpath)
                if not ret:
                    click.echo("syncTo")
                    err = 1

    sys.exit(err)

if __name__ == '__main__':
    main()