import os
import re
import shutil
import subprocess
from getpass import getpass
from glob import glob
from pathlib import Path

PACKAGE_LIST_PATH = Path('/root/documentation/documentation/package_list.txt')
TMP_PATH = Path('/root/documentation/tmp')
DOCS_PATH = Path('/root/documentation/docs/source')


def initialize(filename, extension):
    """initialize files

    Args:
        filename (str): initial file name.
        extension (str): extension of initial file.
    """
    with open(f'{DOCS_PATH}/initials/{filename}_initial.{extension}', 'r') as f:
        _ = f.readlines()
    with open(f'{DOCS_PATH}/{filename}.{extension}', 'w') as f:
        f.writelines(_)


def main():
    """update documents"""

    # clear files which are created automatically before.
    existing = glob('/root/documentation/docs/*')
    existing = [_ for _ in existing if _.rsplit('/', 1)[1] not in ('Makefile', 'make.bat', 'source')]
    for _existing in existing:
        if os.path.isfile(_existing):
            os.remove(_existing)
        else:
            shutil.rmtree(_existing)

    with PACKAGE_LIST_PATH.open('r') as f:
        lines = f.read().splitlines()

    initials = glob(f'{DOCS_PATH}/initials/*')
    initials = [_.rsplit('/', 1)[1] for _ in initials]
    initials = [_.split('_initial.') for _ in initials]
    for _initial in initials:
        initialize(_initial[0], _initial[1])
    cfg_index = 18

    TMP_PATH.mkdir(parents=True, exist_ok=True)
    os.chdir(TMP_PATH)

    username = input('Please input Username for "https://github.com":')
    password = getpass(f'Please input Password for "https://{username}@github.com":')
    for _repository in lines:
        if _repository[0] == '[' and _repository[-1] == ']':
            group = _repository[1:-1]
            continue
        elif not all([_ in _repository for _ in ('{', '}')]) or '' == _repository:
            continue
        _repository = [_ for _ in re.split('[{},=" ]', _repository) if _ != '']
        repository_name = _repository[_repository.index('name')+1]
        tag_or_branch = 'tag' if 'tag' in _repository else 'branch' if 'branch' in _repository else None
        tag_or_branch = _repository[_repository.index(tag_or_branch)+1] if tag_or_branch is not None else 'master'
        print(f'>>> {repository_name} / {tag_or_branch}')
        # git clone
        _repository_ = f'https://{username}:{password}@github.com/i-SAS/{repository_name}'
        subprocess.run(['git', 'clone', '-b', tag_or_branch, '--depth', '1', _repository_])

        # add document name to index.rst
        folders = glob(f'{TMP_PATH}/{repository_name}/**/')
        _exceptions = ('docs', 'cfg', 'tests', 'bin', 'test')
        folders = [_.rsplit('/', 2)[1] for _ in folders if _.rsplit('/', 2)[1] not in _exceptions]
        if repository_name == 'i-SAS_iFEM-matlab':
            folders = ['ifem_matlab']
        if len(folders) != 1:
            print(f'Could not specified script folder of {repository_name}.')
            for i in range(100):
                script_folder = input(f'Please input script folder name. The candidates are {folders}.\n>>>')
                if os.path.isdir(f'{TMP_PATH}/{repository_name}/{script_folder}') or script_folder == 'skip':
                    break
                else:
                    print(f'folder named {script_folder} is not exist.')
        else:
            script_folder = folders[0]
        if group != 'Interface':
            with open(f'{DOCS_PATH}/{group}_index.rst', 'a') as f:
                f.write(f'\n   {script_folder}')

        # create .rst file automatically
        # subprocess.run(['sphinx-apidoc', '-f', '-o', DOCS_PATH, str(TMP_PATH / repository_name)])
        # create .rst file manually
        modules = glob(f'{TMP_PATH}/{repository_name}/{script_folder}/*.py')
        modules = [_.rsplit('/', 1)[1][:-3] for _ in modules]
        modules = [_ for _ in modules if '__' not in _]
        with open(f'{DOCS_PATH}/{script_folder}.rst', 'w') as f:
            f.write(f'{"="*50}\n{repository_name}\n{"="*50}\n\n')
            for _module in modules:
                f.write(f'{_module}\n{"-"*50}\n\n')
                f.write(f'.. automodule:: {script_folder}.{_module}\n')
                f.write('   :members:\n   :undoc-members:\n   :show-inheritance:\n\n')

        # add path
        with open(f'{DOCS_PATH}/conf.py', 'r') as f:
            cfg = f.readlines()
        cfg.insert(cfg_index, f"sys.path.insert(0, os.path.abspath('../../tmp/{repository_name}'))\n")
        with open(f'{DOCS_PATH}/conf.py', 'w') as f:
            f.writelines(cfg)
        cfg_index += 1

    os.chdir('../')

    subprocess.run(['sphinx-build', '-b', 'html', DOCS_PATH, '/root/documentation/docs'])
    shutil.rmtree(TMP_PATH)


if __name__ == '__main__':
    main()
