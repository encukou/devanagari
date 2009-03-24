; Devanagari.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "Devanagari"

; The file to write
OutFile "devanagari-install.exe"

; The default installation directory
InstallDir $PROGRAMFILES\Devanagari

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\EnCuKou\Devanagari" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "Devanagari"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put files there
  File "bz2.pyd"
  File "Devanagari.exe"
  File "library.p2e"
  File "MSVCP90.dll"
  File "PyQt4.Qt.pyd"
  File "PyQt4.QtCore.pyd"
  File "PyQt4.QtGui.pyd"
  File "python26.dll"
  File "QtCore4.dll"
  File "QtGui4.dll"
  File "sip.pyd"
  File "transl_table.py"
  File "unicodedata.pyd"
  File "w9xpopen.exe"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM Software\EnCuKou\Devanagari "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Devanagari" "DisplayName" "Devanagari"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Devanagari" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Devanagari" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Devanagari" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\Devanagari"
  CreateShortCut "$SMPROGRAMS\Devanagari\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\Devanagari\Devanagari.lnk" "$INSTDIR\Devanagari.exe" "" "$INSTDIR\Devanagari.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Devanagari"
  DeleteRegKey HKLM Software\EnCuKou\Devanagari

  ; Remove files and uninstaller
  Delete $INSTDIR\Devanagari.exe
  Delete $INSTDIR\uninstall.exe
  Delete $INSTDIR\bz2.pyd
  Delete $INSTDIR\Devanagari.exe
  Delete $INSTDIR\library.p2e
  Delete $INSTDIR\MSVCP90.dll
  Delete $INSTDIR\PyQt4.Qt.pyd
  Delete $INSTDIR\PyQt4.QtCore.pyd
  Delete $INSTDIR\PyQt4.QtGui.pyd
  Delete $INSTDIR\python26.dll
  Delete $INSTDIR\QtCore4.dll
  Delete $INSTDIR\QtGui4.dll
  Delete $INSTDIR\sip.pyd
  Delete $INSTDIR\transl_table.py
  Delete $INSTDIR\unicodedata.pyd
  Delete $INSTDIR\w9xpopen.exe

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\Devanagari\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\Devanagari"
  RMDir "$INSTDIR"

SectionEnd
