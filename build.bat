

set TOKEN=*****

@echo off
git.exe %*
set GITBRANCH=
for /f %%I in ('git.exe rev-parse --abbrev-ref HEAD 2^> NUL') do set GITBRANCH=%%I

if "%GITBRANCH%" == "" (
  prompt $P$G 
) else (
    echo %GITBRANCH%
)

docker build -t %GITBRANCH% .
if errorlevel 1 echo Unsuccessful built

docker run -e TOKEN=%TOKEN% %GITBRANCH%
if errorlevel 1 echo Failed at running the container
