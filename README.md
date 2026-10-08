# Reel UI Automation

Screen-based Reel UI workflow automation using Python, OpenCV, and PyAutoGUI.

## Scope

- Detect the active Reel interface with multi-scale template matching
- Scroll to the next Reel
- Detect and open the comment interface
- Locate the comment input area
- Enter predefined text, including Hindi and emoji
- Close the comment interface
- Repeat with recovery handling and emergency controls

The implementation is designed for a Windows desktop with common display resolutions and DPI scaling. It uses screen recognition rather than fixed coordinates.

## Safety boundary

The live workflow intentionally stops at a **manual-post checkpoint** after preparing comment text. There is no automatic comment-submit/post action.

The offline mock workflow exercises the complete safe state flow without touching a real website.

## Controls

- **F8** — pause/resume the live workflow
- **F9** — stop the workflow

## Tech Stack

- Python
- OpenCV
- PyAutoGUI
- Pillow
- NumPy
- Pyperclip
- Keyboard

## Current status

The project has a tested workflow foundation with:

- location-aware multi-scale template matching
- Unicode clipboard typing with clipboard restoration
- recovery handling and F8/F9 controls
- Windows DPI-awareness setup
- template validation and calibration/probe tools
- offline mock integration coverage
- GitHub Actions CI with the existing test suite

Real UI templates are intentionally kept separate from the code and must be captured on the Windows machine where the workflow will run.

## Quick start

From the repository root in Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python tools/check_setup.py
python tools/diagnose.py
python tools/dry_run.py
```

Run the offline workflow without posting anything:

```powershell
python run.py --mock --comment "Demo comment"
```

Capture and validate real UI templates:

```powershell
python tools/capture_template.py reel_marker.png
python tools/validate_templates.py
python tools/probe_template.py reel_marker.png
python tools/calibrate_template.py reel_marker.png
```

For the live workflow, use explicit predefined text and keep the manual-post checkpoint:

```powershell
python run.py --live --once --comment "Your comment"
```

Do not run the live workflow until the target UI templates have been captured and validated.
