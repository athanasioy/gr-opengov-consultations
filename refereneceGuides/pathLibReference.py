from pathlib import Path

# get Current Working Directory

print("CWD: ",Path.cwd())

# get Home Directiory

print("Home: ", Path.home())

# Create a new Path Object by passing path as string

pathObj = Path(r"C:\Users\aneme\vscode\publicConsulationScrap")

print("myPath: ", pathObj)

# Check if path Exists

print("does myPath exist? ", pathObj.exists())

# path object is NOT case sensitive !

pathObj = Path(r"c:\Users\aneme\vscode\publicconsulationScrap")

print("does myPath exist now ? ", pathObj.exists())

# this is allowed

pathObj = Path("someJunkPath")

print("Junk Path: ",pathObj)



# create path objects with "/"

pathObj = Path.cwd() / "main.py"

print("Path.cwd() / 'main.py ==> ",pathObj)

# Check for file, directory

print(f"is File? {pathObj} ",pathObj.is_file())

print(f"is directory? {pathObj} ",pathObj.is_dir())

# Relative vs Absolute

pathObj = Path("main.py")

print("Path('main.py') ==>", pathObj, "|Does it Exists? ", pathObj.exists(), "|is Relative Path? ", not pathObj.is_absolute())
pathObj = pathObj.absolute()  # pathObj.absolute happens in place!
print("pathObj.absolute() ==>", pathObj, " | is Absolute? ", pathObj.is_absolute())

pathObj = Path("main.py")
print("pathObj.resolve() ==>", pathObj.resolve())

# read files with Path

pathObj = Path("config.ini")
print("Path Objects can be used in context managers ==> they return a file")
print("e.g. with pathObj.open() as file:...")

with pathObj.open() as file:
    print(file.read())
print()

# delete file with Path.unlink

# Shorter version
print("Shorter Version:  pathObj.read_text() ==>...")
print(pathObj.read_text())
print()

# useful properties

print("Parent of a relative path : pathObj.parent ==>", pathObj.parent)  # is relative

pathObj_resolved = pathObj.resolve()

print("Parent of a resolved path : pathObj_resolved.parent ==>", pathObj_resolved.parent)  # is absolute 
print("Parent Returns a Path...")
print("So this is possible Path.parent.parent... ==> ", pathObj_resolved.parent.parent)


print("pathObj.name ==> ",pathObj.name)

print("pathObj.stem ==> ", pathObj.stem)

print("pathObj.suffix ==> ", pathObj.suffix)

# Create files, write and delete files

pathObj = Path.cwd() / "new_file.txt"

print("Create a file file: pathObj.touch()")
pathObj.touch()
print()
print("Write text with pathObj.write_text()")
pathObj.write_text("hi")
print()

print("Delete file with pathObj.unlink()")
pathObj.unlink()


# Create a directory

print("Create a directory with pathObj.mkdir()")
pathObj = Path("newDir")
# pathObj.mkdir()

# librarries suppor PathLib

from os import chdir

pathObj = Path("scripts")
print("CWD: ", Path.cwd())
chdir(pathObj)
print("after os.chdir(pathObj)... ", pathObj.cwd())
