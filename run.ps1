$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = Join-Path $root "src"
python (Join-Path $root "run_app.py")
