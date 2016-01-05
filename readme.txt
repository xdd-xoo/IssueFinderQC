1, Make sure you have python install
    svn://10.231.212.33/pdt/Tools/Python/python-2.7.3.amd64.msi
2, Install below python lib from below two files
    svn://10.231.212.33/pdt/Tools/Python/xlwt-0.7.5/install.bat
    svn://10.231.212.33/pdt/Tools/Python/xlrd-0.9.3/install.bat
3, Install python lib for MySQL DB access
    svn://10.231.212.33/pdt/Tools/Python/MySQL-python-1.2.3.win-amd64-py2.7.exe   --- For 64 bits python
    svn://10.231.212.33/pdt/Tools/Python/MySQL-python-1.2.4b4.win32-py2.7.exe     --- For 32 bits python
4, Install python lib for JIRA & PRISM
    svn://10.231.212.33/pdt/Tools/Python/suds_requests-0.1.tar.gz
    svn://10.231.212.33/pdt/Tools/Python/python-ntlm-1.0.1.tar.gz
5, Modify parser_config.xml to put the log directory you want to parse
6, Run command
    python HUBBLE_Service.py