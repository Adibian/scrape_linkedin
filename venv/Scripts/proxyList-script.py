#!G:\programming\Pycharm\Projects\PythonProject\scrape_linkedin\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'http-request-randomizer==1.2.3','console_scripts','proxyList'
__requires__ = 'http-request-randomizer==1.2.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('http-request-randomizer==1.2.3', 'console_scripts', 'proxyList')()
    )
