echo “This is a simple shell script that is used to update the base UI python file when changes are made in QT Designer”

cd /Users/galenarnold/Documents/Galen/Python/tipLocatorApplication
pyuic4 tipLocatorUIBase.ui > tipLocatorUIBase.py
osascript -e 'tell application "Terminal" to quit'