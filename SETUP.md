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

## 5. Capture UI templates

```powershell
python tools/capture_template.py
```

Required names are:

- `reel_marker.png`
- `comment_button.png`
- `comment_input.png`
- `close_comment.png`

After capturing templates, validate them:

```powershell
python tools/validate_templates.py
```

Templates should be tightly cropped and must not contain credentials, private messages, or other sensitive information.

## 6. Probe a template

Once a real template exists, test screen detection without performing a workflow action:

```powershell
python tools/probe_template.py comment_button.png
```

A successful probe reports the detected position, size, center, and confidence.

## Resolution and DPI notes

The detector uses multi-scale template matching rather than a single fixed coordinate. For best results, capture templates on the Windows display/scaling configuration where the project will run.

If the display scaling changes significantly, recapture the small UI templates rather than using a large screenshot of the entire interface.


## 7. Calibrate a template on the current screen

Calibration only captures the current screen and measures template matching. It does not click, scroll, type, or submit anything.

```powershell
python tools/calibrate_template.py comment_button.png
```

The report shows the best detected scale, confidence, position, and match size.
