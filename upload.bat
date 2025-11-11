@echo off
cls
cd \
xcopy /Y /E pyhog-Engine %userprofile%\pyhog-Engine && cd pyhog-Engine && git add -a && git push