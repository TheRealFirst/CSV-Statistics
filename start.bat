@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ====== Setup logging ======
cd /d "%~dp0" || goto :PAUSE_FAIL
set "LOG=%CD%\run.log"
echo [START %DATE% %TIME%] > "%LOG%"
echo Working dir: %CD%>>"%LOG%"

goto :AFTER_FUNCS
:LOG
>>"%LOG%" echo [%DATE% %TIME%] %*
exit /b 0

:RUN
set "CMD=%*"
>>"%LOG%" echo [%DATE% %TIME%] CMD: !CMD!
%* >>"%LOG%" 2>&1
set "RC=!ERRORLEVEL!"
>>"%LOG%" echo [%DATE% %TIME%] EXIT !RC!
exit /b !RC!

:TRY_WINGET_INSTALL
set "PKG=%~1"
call :LOG Trying winget install: !PKG!
call :RUN "!WINGET!" install --id !PKG! --scope user --accept-source-agreements --accept-package-agreements
exit /b !RC!
:AFTER_FUNCS

REM ====== Ensure winget is available ======
set "WINGET="
for /f "delims=" %%I in ('powershell -NoProfile -Command "(Get-Command winget.exe -EA SilentlyContinue).Source"') do set "WINGET=%%~I"
if not defined WINGET if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\winget.exe" set "WINGET=%LOCALAPPDATA%\Microsoft\WindowsApps\winget.exe"

if not defined WINGET (
    echo( winget not found — installing App Installer...
    call :LOG "winget not found; attempting App Installer registration"
    powershell -NoProfile -Command "Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe" >>"%LOG%" 2>&1
    REM Re-detect
    for /f "delims=" %%I in ('powershell -NoProfile -Command "(Get-Command winget.exe -EA SilentlyContinue).Source"') do set "WINGET=%%~I"
    if not defined WINGET if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\winget.exe" set "WINGET=%LOCALAPPDATA%\Microsoft\WindowsApps\winget.exe"
)

if defined WINGET (
  call :RUN "!WINGET!" -v
  if not "!RC!"=="0" set "WINGET="
)
call :LOG Winget usable: !WINGET!

REM ====== Locate real Python (avoid WindowsApps stub) ======
set "PYEXE="
call :RUN py -V
if "!RC!"=="0" set "PYEXE=py.exe"

if not defined PYEXE (
  for /f "usebackq delims=" %%P in (`where python 2^>NUL`) do (
    echo %%~fP | find /i "\WindowsApps\" >NUL
    if errorlevel 1 (
      set "PYEXE=%%~fP"
      goto :VERIFY_PY
    )
  )
)

if not defined PYEXE (
  for %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*" "%ProgramFiles%\Python3*" "%ProgramFiles(x86)%\Python3*") do (
    for /f "usebackq delims=" %%P in (`dir /b /s "%%~D\python.exe" 2^>NUL`) do (
      set "PYEXE=%%~fP"
      goto :VERIFY_PY
    )
  )
)

:VERIFY_PY
if defined PYEXE (
  call :LOG Candidate PYEXE: !PYEXE!
  call :RUN "!PYEXE!" -V
  if not "!RC!"=="0" set "PYEXE="
)
call :LOG Detected PYEXE: !PYEXE!

REM ====== If missing, install with winget (discover ID dynamically) ======
if not defined PYEXE (
  if not defined WINGET (
    call :LOG ERROR: Python not found and winget unavailable; aborting.
    echo( ERROR: Python not found and winget is unavailable. See run.log
    goto :PAUSE_FAIL
  )

  call :RUN "!WINGET!" source update

  set "FOUND_ID="
  for %%K in (
    Python.Python.3.13
    Python.Python.3.12
    Python.Python.3.11
    Python.Python.3
  ) do (
    if not defined FOUND_ID (
      call :RUN "!WINGET!" show --id %%K --source winget
      if "!RC!"=="0" set "FOUND_ID=%%K"
    )
  )

  if not defined FOUND_ID (
    call :LOG Scanning winget search for Python.Python.*
    for /f "usebackq tokens=1,2,* delims= " %%A in (`"!WINGET!" search python --source winget ^| findstr /r /c:"Python\.Python\.[0-9]"`) do (
      if not defined FOUND_ID set "FOUND_ID=%%B"
    )
  )

  if not defined FOUND_ID (
    call :LOG ERROR: No suitable Python package ID found via winget.
    echo( ERROR: winget couldn't find a Python package in your catalog. See run.log
    goto :PAUSE_FAIL
  )

  call :LOG Installing with ID: !FOUND_ID!
  call :RUN "!WINGET!" install --id !FOUND_ID! --scope user --accept-source-agreements --accept-package-agreements
  if not "!RC!"=="0" (
    call :LOG ERROR: winget install failed.
    goto :PAUSE_FAIL
  )

  REM Re-scan without relying on PATH refresh
  call :RUN py -V
  if "!RC!"=="0" (
    set "PYEXE=py.exe"
  ) else (
    for %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*" "%ProgramFiles%\Python3*" "%ProgramFiles(x86)%\Python3*") do (
      for /f "usebackq delims=" %%P in (`dir /b /s "%%~D\python.exe" 2^>NUL`) do (
        set "PYEXE=%%~fP"
        goto :VERIFY_AFTER_INSTALL
      )
    )
    :VERIFY_AFTER_INSTALL
    if defined PYEXE (
      call :RUN "!PYEXE!" -V
      if not "!RC!"=="0" set "PYEXE="
    )
  )
)

if not defined PYEXE (
  call :LOG ERROR: No working Python after winget install attempts.
  goto :PAUSE_FAIL
)

REM ====== Create venv if needed ======
if not exist ".venv\Scripts\python.exe" (
  if /I "!PYEXE!"=="py.exe" (
    call :RUN py -m venv .venv
  ) else (
    call :RUN "!PYEXE!" -m venv .venv
  )
  if not "!RC!"=="0" goto :PAUSE_FAIL
) else (
  call :LOG .venv already exists
)

REM ====== requirements.txt ======
if not exist "requirements.txt" (
  >requirements.txt echo numpy
  >>requirements.txt echo matplotlib
  call :LOG Created default requirements.txt
) else (
  call :LOG Using existing requirements.txt
)

REM ====== Install deps ======
set "VENV_PY=.venv\Scripts\python.exe"
call :RUN "!VENV_PY!" -m pip install --upgrade pip
if not "!RC!"=="0" goto :PAUSE_FAIL
call :RUN "!VENV_PY!" -m pip install -r requirements.txt
if not "!RC!"=="0" goto :PAUSE_FAIL

REM ====== Run app ======
if not exist "main.py" (
  call :LOG ERROR: main.py missing.
  goto :PAUSE_FAIL
)
call :RUN "!VENV_PY!" main.py
if not "!RC!"=="0" goto :PAUSE_FAIL

goto :PAUSE_OK

:PAUSE_FAIL
echo(
echo === FAILED. See log: "%LOG%" ===
echo(
pause
exit /b 1

:PAUSE_OK
echo(
echo === SUCCESS. See log: "%LOG%" ===
echo(
pause
exit /b 0
