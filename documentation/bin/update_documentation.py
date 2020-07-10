import os
import shutil
import subprocess
from pathlib import Path

PACKAGE_LIST_PATH = Path('/root/documentation/documentation/package_list.txt')
TMP_PATH = Path('/root/documentation/tmp')
DOCS_PATH = Path('/root/documentation/docs/source')


def main():
    with PACKAGE_LIST_PATH.open('r') as f:
        lines = f.read().splitlines()
    TMP_PATH.mkdir(parents=True, exist_ok=True)
    os.chdir(TMP_PATH)
    for repository_path in lines:
        repository_name = repository_path.rsplit('/', 1)[1]
        print(repository_name)
        # git clone
        subprocess.run(['git', 'clone', repository_path])
        # update documents
        subprocess.run(['sphinx-apidoc', '-f', '-o', DOCS_PATH, str(TMP_PATH / repository_name)])
        subprocess.run(['sphinx-build', '-b', 'singlehtml', DOCS_PATH, str(TMP_PATH / repository_name)])
    os.chdir('../')
    shutil.rmtree(TMP_PATH)


if __name__ == '__main__':
    main()
