import ast,sys,os,subprocess,importlib,importlib.util,traceback
from pathlib import Path
ECHO is off.
def get_imports(path):
    try:
        src = Path(path).read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print("Ne mogu procitati", path, ":", e)
        return set()
    try:
        tree = ast.parse(src)
    except Exception as e:
        print("Parse error:", e)
        return set()
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                mods.add(n.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mods.add(node.module.split('.')[0])
    return mods
ECHO is off.
STD_LIB = {
    'sys','os','io','re','json','csv','math','time','shutil','random','string',
    'hashlib','tempfile','datetime','traceback','webbrowser','platform','subprocess',
    'itertools','threading','warnings','secrets','base64','binascii','zlib',
    'pathlib','typing','functools','dataclasses','html','xml','sqlite3','urllib','http','email','ssl','glob'
}
ECHO is off.
def is_local(mod):
    p1 = Path(mod + '.py')
    p2 = Path(mod)
    return p1.exists() or p2.exists()
ECHO is off.
def already_available(mod):
    try:
        spec = importlib.util.find_spec(mod)
        return spec is not None
    except Exception:
        return False
ECHO is off.
def install(mod):
    try:
        print(f"--> Installing: {mod}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', mod])
        return True
    except subprocess.CalledProcessError as e:
        print("Installation failed for", mod, ":", e)
        return False
    except Exception as e:
        print("Unexpected error installing", mod, ":", e)
        return False
ECHO is off.
def main():
    script = 'Luxxer_OS.py'
    if not Path(script).exists():
        print(script, "nije pronadjen u", Path.cwd())
        sys.exit(1)
ECHO is off.
    mods = get_imports(script)
    if not mods:
        print("Nema import linija ili nisu mogle da se procitaju.")
ECHO is off.
    to_install = []
    for m in sorted(mods):
        if not m or m in STD_LIB:
            continue
        if is_local(m):
            print("Preskacem lokalni modul:", m)
            continue
        if already_available(m):
            print("Vec instalirano:", m)
            continue
        to_install.append(m)
ECHO is off.
    # mape/pravila za neke uobicajene razlike izmedju import imena i pip imena
    fallbacks = {'PIL':'Pillow','bs4':'beautifulsoup4'}
ECHO is off.
    for m in to_install:
        name = m
        if m in fallbacks:
            name = fallbacks[m]
        # Ako je import npr. PyQt6.QtCore, m ce biti 'PyQt6' i to je ok
        ok = install(name)
        if not ok:
            # pokusaj malu varijantu (lowercase) ako prvobitna nije radila
            if name.lower() != name:
                install(name.lower())
ECHO is off.
    print("Sve instalacije zavrsene (ili je bilo gresaka). Pokrecem skriptu...")
    try:
        subprocess.check_call([sys.executable, script])
    except subprocess.CalledProcessError as e:
        print("Skripta se zavrsila sa kodom", e.returncode)
    except Exception as e:
        print("Greska pri pokretanju skripte:", e)
ECHO is off.
if __name__ == "__main__":
    main()
