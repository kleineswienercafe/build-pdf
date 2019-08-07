# KWC - Build PDFs
This projects builds PDFs from LaTeX or Markdown sources. It is inteded to plug into existing CI's of LaTeX/Markdown repositories.

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

enjoy!