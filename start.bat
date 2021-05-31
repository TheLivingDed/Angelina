@echo off
TITLE MissAngelina_Bot
rem This next line removes any fban csv files if they exist in root when bot restarts. 
del *.csv
py -3.7 --version
IF "%ERRORLEVEL%" == "0" (
    py -3.7 -m Angelina
) ELSE (
    py -m Angelina
)

pause
