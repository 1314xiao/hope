@echo off
chcp 65001 >nul
set "GLUE_DIR=D:\hope\hopeglue"
set "HOPE_ENV_ROOT=D:\hope"
del /q "_env_temp.zip" 2>nul
if "%~2"=="" (
    echo 用法：glue 脚本.hope 输出app.exe
    echo 示例：glue 2.hope app.exe
    pause
    exit /b
)
"%GLUE_DIR%\hopeglue.exe" "%GLUE_DIR%\loader.exe" "%HOPE_ENV_ROOT%" %1 %2
del /q "_env_temp.zip" 2>nul
