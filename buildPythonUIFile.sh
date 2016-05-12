echo “This is a simple shell script that is used to update the base UI python file when changes are made in QT Designer”

cd /Users/equipment/Documents/Code/tipLocatorApplication
pyuic5 tipLocatorUIBase.ui > tipLocatorUIBase.py
osascript -e 'tell application "Terminal" to quit'

