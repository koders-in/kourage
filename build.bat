
set TOKEN=ODQ5NTY2Mzk1NjM3MTcwMTc2.YLdCXA.Jq-76rr3NpcSZcDfzGMfy13Bl2o
set ADMIN_CHANNEL_ID=849583285645475850

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

docker run -e TOKEN=%TOKEN% -e ADMIN_CHANNEL_ID=%ADMIN_CHANNEL_ID% %GITBRANCH%
if errorlevel 1 echo Failed at running the container
