# Local Setup

## 1. Create the environment

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Check dependencies

```powershell
python tools/check_setup.py
```

## 3. Check screen size

```powershell
python tools/diagnose.py
```

## 4. Run the safe workflow simulation

```powershell
python tools/dry_run.py
```

## 5. Capture a UI template

```powershell
python tools/capture_template.py
```

Templates should be tightly cropped and must not contain credentials, private messages, or other sensitive information.
