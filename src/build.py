import os


class Param:
    
    def __init__(self, root: str):

        self.root = root

        self.texPath = self.root + "/src/tex/"      # repository relative path of tex files
        self.mdPath = self.root + "/src/md/"        # repository relative path of markdown files
        self.dstPath = self.root + "/documents/"    # repository relative output path
        self.alwaysFail = True
        self.clean = True
        self.srcBuild = True # unfortunately we need this for some old (latest) ubuntu packages 


def main(p: Param):

    # create destination path
    if not os.path.exists(p.dstPath):
        os.mkdir(p.dstPath)

    pdfs = compileDir(p.texPath, ".tex", p)
    pdfs += compileDir(p.mdPath, ".md", p)

    print(str(len(pdfs)) + " documents created")

    if p.clean:
        cleanup(p.dstPath)

    if p.srcBuild:
        copypdfs(pdfs, p.dstPath)

def copypdfs(pdfs: list, dst: str):
    from shutil import copyfile
    
    for p in pdfs:
        fn = os.path.basename(p)
        copyfile(p, dst + fn)

def cleanup(path: str):

    files = os.listdir(path)
    delfiles = [f for f in files if not f.endswith(".pdf")]

    for fn in delfiles:
        os.remove(path + fn)

def compileDir(srcPath: str, ext: str, p: Param):

    files = os.listdir(srcPath)
    tf = [f for f in files if f.endswith(ext)]

    pdfs = []
    dstPath = p.dstPath if not p.srcBuild else srcPath

    # compile tex files of this directory
    for fn in tf:
        fnc = str.replace(fn, ext, "")
        pdf = dstPath + fnc + ".pdf"

        print("compiling: " + fn + " -> " + pdf)

        if ext == ".tex":
            if not compileTex(srcPath, fnc, dstPath) and p.alwaysFail:
                raise Exception("Could not compile " + srcPath + fn)
        elif ext == ".md":
            if not compileMarkDown(srcPath, fnc, dstPath) and p.alwaysFail:
                raise Exception("Could not compile " + srcPath + fn)
        else:
            print("Unknown extension: " + ext)
            if p.alwaysFail:
                raise Exception("Could not compile " + srcPath + fn)

        pdfs.append(pdf)

    return pdfs

def compileTex(srcPath: str, filename: str, dstPath: str):

    attr = " -interaction=nonstopmode"
    oDir = " -output-directory=\"" + dstPath + "\""
    iDir = " -include-directory=\"" + srcPath + "\""

    cbp = dstPath + filename + ".aux" 
    cbb = cbp if srcPath != dstPath else filename + ".aux"
    ctp = srcPath + filename + ".tex"

    # texlive = "python3 " + os.path.dirname(os.path.abspath(__file__)) + "/texliveonfly.py \"" + ctp + "\""
    pdflatex = "pdflatex" + attr + iDir + oDir + " \"" + ctp + "\""
    bibtex = "bibtex \"" + cbb + "\""

    # pdflatex
    if not run(pdflatex, srcPath):
        return False

    # run bibtex
    if usesBibTex(cbp):
        if not run(bibtex, srcPath):
            return False

    # run pdflatex again
    if not run(pdflatex, srcPath):
        return False

    # and again
    if not run(pdflatex, srcPath):
        return False
        
    return True

def compileMarkDown(srcPath: str, filename: str, dstPath: str):

    md = srcPath + filename + ".md"
    pdf = dstPath + filename + ".pdf"
    # rp = " --resource-path=" + srcPath

    cmd = "pandoc \"" + md + "\" -o \"" + pdf + "\""

    return run(cmd, srcPath)

def usesBibTex(src: str):

    with open(src, 'rb', 0) as file:
        
        for l in file.readlines():
            if b'\\citation{' in l:
                return True
        
    return False

def run(cmd: str, workingDir: str = ""):
    import subprocess

    # print("running: " + cmd)
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd= workingDir)

    out, err = sp.communicate()
    # cmdprint(out) # uncomment when debugging compiling
    
    if sp.returncode != 0:

        if out:
            cmdprint(out)

        if err:
            cmdprint(err)

        print("\n\nERROR running: " + cmd)

        print("return value: " + str(sp.returncode))
        return False

    return True

# use this function for debugging since it directly prints to std out
def runp(cmd: str, workingDir: str = ""):

    if os.system(cmd) != 0:
        print("\n\nERROR running: " + cmd)
        return False

    return True

def cmdprint(output):

    for line in output.decode('utf-8').split('\n'):
        print(line)

if __name__ == "__main__":
    
    import argparse
    import sys

    # argument parser
    parser = argparse.ArgumentParser(
        description='Compiles all tex and markdown files and copies the pdfs')

    parser.add_argument('dir', nargs='?', default=os.getcwd(), type=str,
                        help='path to your repository')

    parser.add_argument('--tex-src', dest="texpath", type=str,
                        help='folder path to all tex source files')

    parser.add_argument('--md-src', dest="mdpath", type=str,
                        help='folder path to all markdown source files')

    # get args and make a dict from the namespace
    args = vars(parser.parse_args())

    rp = os.path.abspath(args['dir'])
    p = Param(rp)

    if args['texpath']:
        p.texPath = args['texpath']
    if args['mdpath']:
        p.mdPath = args['mdpath']

    main(p)
