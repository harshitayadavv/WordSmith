@echo off
copy manifest.json dist\
mkdir dist\icons 2>nul
copy public\icons\*.png dist\icons\ 2>nul
echo Files copied successfully!
