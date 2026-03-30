@echo off
setlocal
set "ROOT=%~dp0"
set "PYTHONPATH=%ROOT%src"
python "%ROOT%run_app.py"
