#!/bin/bash

exec pyinstaller -F -n nowplaying --add-data "page.html:page.html" --add-data "code.js:code.js" --add-data "styles.css:styles.css" main.py 