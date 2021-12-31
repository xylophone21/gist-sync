# gist-sync
- Sync selected markdown files to gist in github.
- Share part of pages to gist when you want to using github private repo as notes.

## How to setup
1. Make a private Github repo for your note.
2. Add this repo as submodule

```
git submodule add git@github.com:xylophone21/gist-sync.git gist-sync
```
3. Copy .github/workflows/test.yaml to your repo and change the envs
    - Generate a new GitHub Token https://github.com/settings/tokens here

## How to use
1. New a Gist at https://gist.github.com/
2. Add the Gist to your markdown file to share it
```
[gist-sync-url]:https://gist.github.com/{your_account}/{gist_id}/
```
