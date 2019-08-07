# KWC - Build PDFs
This projects builds PDFs from LaTeX or Markdown sources. It is inteded to plug into existing CI's of LaTeX/Markdown repositories.

[![Build Status](https://travis-ci.org/kleineswienercafe/build-pdf.svg?branch=master)](https://travis-ci.org/kleineswienercafe/build-pdf)

## Repository Structure
By default we expect this repository structure:
- `src/tex` folder containing all LaTeX sources
- `src/md` folder containing all Mardkown files

Build PDFs will then create a folder `documents` containing all pdfs.

## Dependencies

Windows:
- Markdown to pdf: [pandoc](https://pandoc.org/installing.html)
- LaTeX to pdf: [miktex](https://miktex.org/)
- Build script: [python](https://www.python.org/)

Linux:
````bash
sudo apt-get install texlive-latex-extra pandoc python3
````

## Building PDFs

You can build all documents in a repository by:
````bash
python src/build.py PATH_TO_YOUR_REPO
````
so to build all documents of this repo, use:
````bash
python src/build.py .
````

Use `python3` rather than `python` on linux.

## Manually Building Markdown

````cmd
pandoc template-md.md -o template-md.pdf
````

## CI Integration
You can easily integrate this script into your [tavis CI](.travis.yml). If you are using gitlab, create a `.gitlab-ci.yml` with this content:
```yml
image: diemmarkus/flowme-tex:latest # load docker with all dependencies needed

stages:
  - build
  - deploy

build-tex:
  stage: build
  artifacts:
    untracked: true
    expire_in: 30 min
  script:
    - git clone https://github.com/kleineswienercafe/build-pdf.git build-pdf
    - python3 build-pdf/src/build.py .
    
# make working copies available on gitlab pages
pages:
    stage: deploy
    dependencies:
      - build-tex
    artifacts:
      paths:
        - public
      expire_in: 2 weeks
    script:
      - mkdir public
      - mv documents/*.pdf public/
```


enjoy!