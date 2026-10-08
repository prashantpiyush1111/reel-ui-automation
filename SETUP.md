# Local Setup

## Assumptions

- **Windows desktop only** for live screen/UI interaction.
- Run commands from the repository root.
- Instagram/Reels UI templates must be captured from the actual Windows display configuration being used.
- The live workflow does **not** submit/post comments automatically.
- The offline mock may automatically submit comments only inside the local mock UI.

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

This checks OpenCV, PyAutoGUI, Pillow, NumPy, keyboard, and Pyperclip.

## 3. Check screen size and DPI coordinate consistency

```powershell
python tools/diagnose.py
```

The diagnostic prints the screenshot size next to `pyautogui.size()`. If they differ, fix the Windows display/DPI configuration before capturing templates.

The application calls Windows `SetProcessDpiAwareness` once at startup, with `SetProcessDPIAware` as a fallback. The call is skipped on non-Windows systems so CI remains headless-safe.

## 4. Run the safe offline simulation

```powershell
python tools/dry_run.py
```

For the integrated mock workflow:

```powershell
python run.py --mock
```

The mock flow groups comments in batches of four:

1. Detect Reel.
2. Open comments.
3. Automatically submit comment 1 locally.
4. Automatically submit comment 2 locally.
5. Automatically submit comment 3 locally.
6. Automatically submit comment 4 locally.
7. Close comments.
8. Move to the next mock Reel.

With eight comments, comments 1–4 belong to Reel 1 and comments 5–8 belong to Reel 2.

The mock submission is local-only and never touches a real website.

## 5. Capture UI templates

Capture only tightly cropped UI elements:

```powershell
python tools/capture_template.py reel_marker.png
python tools/capture_template.py comment_button.png
python tools/capture_template.py comment_input.png
python tools/capture_template.py close_comment.png
```

Required names are:

- `reel_marker.png`
- `comment_button.png`
- `comment_input.png`
- `close_comment.png`

Templates should not contain credentials, private messages, or other sensitive information.

## 6. Validate templates

```powershell
python tools/validate_templates.py
```

Validation checks that every required template exists, is readable, is large enough to be useful, and is not an unusually large screenshot.

## 7. Probe a template

```powershell
python tools/probe_template.py comment_button.png
```

A successful probe reports the detected position, size, center, and confidence without clicking or changing the UI.

## 8. Calibrate a template

```powershell
python tools/calibrate_template.py comment_button.png
```

Calibration measures the best scale and confidence on the current screen. It does not click, scroll, type, or submit anything.

## 9. Live safe workflow

After templates are validated, a single live cycle can be run with explicit text:

```powershell
python run.py --live --once --comment "Your comment"
```

The live sequence is:

1. Detect the active Reel.
2. Open the comment interface.
3. Locate the comment input.
4. Type the predefined text.
5. **Stop at the manual-post checkpoint.**
6. You decide whether to submit the comment manually.
7. Press Enter in the terminal to continue.
8. Close the comment interface.
9. Scroll to the next Reel.

Unicode text such as Hindi and emoji is entered through the clipboard. The previous clipboard contents are restored when they can be read.

## Emergency controls

- **F8:** pause/resume.
- **F9:** stop the live workflow.

If the detector cannot safely recover from a UI mismatch, the recovery layer fails safe rather than guessing coordinates.

## Resolution and DPI notes

The detector uses multi-scale template matching and location-based ambiguity handling rather than a single fixed coordinate.

For best results:

- capture templates on the Windows display/scaling configuration where the project will run;
- keep templates tightly cropped;
- recapture small UI templates after significant Windows display-scaling changes;
- use `python tools/diagnose.py` to confirm screenshot and PyAutoGUI coordinate sizes match.
