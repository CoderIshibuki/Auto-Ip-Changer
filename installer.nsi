Unicode true
Name "Auto IP Changer"
OutFile "AutoIPChanger_Setup.exe"
InstallDir "$PROGRAMFILES\AutoIPChanger"
RequestExecutionLevel admin

!include "MUI2.nsh"

!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "header.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "welcome.bmp"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Vietnamese"

Section "Main"
    SetOutPath "$INSTDIR"
    
    ; File chính
    File "temp_build\AutoIPChanger.exe"
    File "icon.ico"
    File "temp_build\uninstall.bat"
    
    ; Tạo shortcut
    CreateDirectory "$SMPROGRAMS\Auto IP Changer"
    CreateShortCut "$SMPROGRAMS\Auto IP Changer\Auto IP Changer.lnk" "$INSTDIR\AutoIPChanger.exe" "" "$INSTDIR\icon.ico"
    CreateShortCut "$DESKTOP\Auto IP Changer.lnk" "$INSTDIR\AutoIPChanger.exe" "" "$INSTDIR\icon.ico"
    
    ; Tạo uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoIPChanger" \
        "DisplayName" "Auto IP Changer"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoIPChanger" \
        "UninstallString" '"$INSTDIR\Uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoIPChanger" \
        "DisplayIcon" "$INSTDIR\icon.ico"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoIPChanger" \
        "Publisher" "Auto IP Changer Team"
    
SectionEnd

Section "Uninstall"
    ; Xóa file
    Delete "$INSTDIR\AutoIPChanger.exe"
    Delete "$INSTDIR\icon.ico"
    Delete "$INSTDIR\uninstall.bat"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Xóa shortcut
    Delete "$DESKTOP\Auto IP Changer.lnk"
    Delete "$SMPROGRAMS\Auto IP Changer\Auto IP Changer.lnk"
    RMDir "$SMPROGRAMS\Auto IP Changer"
    
    ; Xóa registry
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AutoIPChanger"
    
    ; Xóa thư mục
    RMDir "$INSTDIR"
    
SectionEnd
