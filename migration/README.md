# [Migration Script](https://www.notion.so/prismaio/IA-migration-script-4e7caef78f8a45dd8f3b0a38a86484af)

This repository contains the source code for the Prisma Docs Migration Script, the supporting API, and the webform.

## How to Run

- set up your run environment
- go to the website to input data
- edit the content directory
- run the script

### Prerequisites

- Python 3.10.x or higher
- git

### Setup

- Copy `migration/script` from [prisma/docs-tools](https://github.com/prisma/docs-tools)
- Clone `staging-data` into `./staging-data` with `git clone --branch staging-data https://github.com/prisma/docs` from [prisma/docs](https://github.com/prisma/docs)
- Clone `staging` into `./staging` with `git clone --branch staging https://github.com/prisma/docs` from [prisma/docs](https://github.com/prisma/docs)

### Run the Script

`python migration.py`

Note: in the above command, you might need to replace `python` with `python3` or `python3.10`, depending on how you installed it.

## How Does It Work?

### Variables:

- 'moves_list': A list of files to be moved and where to move them
- 'deletes_list': A list of files to be deleted and where to redirect them to
- 'surgery_list': A list of files to be cut up and where to redirect them to
- 'stitch_list': A list of new files to be made out of the cut up parts of surgery files
- 'redirects_list': A list of redirects

### Steps:

1. Get data from the database
    * Get 'moves' from the database and add them to 'moves_list'
    * Get 'deletes' from the database and add them to 'deletes_list'
    * Get 'surgeries' from the database and add them to 'surgery_list'
    * Get 'stitches' from the database and add them to 'stitch_list'
2. Add all files that are not references in 'moves_list', 'deletes_list', or 'surgery_list' to 'moves_list' at their current path
3. Move all files in 'moves_list' to their new locations
4. Move all files in 'surgery_list' to a temporary surgery directory
5. Load all surgery files into memory and slice them at predetermined points
6. Use stitch_list to contruct new files from the pieces of the surgery files
7. Generate redirects and add them to 'redirects_list'
    * From the current url to the new url with 'moves_list'
    * From the current url to the redirect if it exists, or the 410 page if it doesnt with 'deletes_list' and 'surgery_list'
8. Add the redirects from 'redirects_list' to 'vercel.json'
9. Use 'redirects_list' to go through all of the files and fix any broken links
