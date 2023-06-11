# gist-sync
- Share part of pages to gist when you want to using github/gitlab private repo as notebook.
- Support images and plantuml in markdown, see test/*.md as examples.
- Gitlab gets better experience as it supports plantuml images in the repo website

## How to setup
1. Make a private Github/gitlab repo for your notebook.
2. Add this repo as submodule

```
git submodule add git@github.com:xylophone21/gist-sync.git .gist-sync
```
3. Copy .github/workflows/test.yaml or .gitlab-ci.yml to your repo and change the envs
    - Generate a new GitHub Token https://github.com/settings/tokens here

## How to use
1. New a Gist at https://gist.github.com/
2. Add the Gist to your markdown file to share it
```
[gist-sync-url]:https://gist.github.com/{your_account}/{gist_id}/
```
## features
1. Sync some pages to gist
2. plantuml diagram in markdown like Markdown Preview Enhanced

## Note
Do not add you token to your public repo. That's why actions failed in this repo.