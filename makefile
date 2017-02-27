exe=bin/*
install:
	install -Dm755 src/openbox-tool-dock.py /usr/bin/openbox-tool-dock
	install -Dm755 src/openbox-tool-focus.py /usr/bin/openbox-tool-focus
	install -Dm755 src/openbox-tool-placement.py /usr/bin/openbox-tool-placement
	install -Dm755 src/openbox-tool-theme.py /usr/bin/openbox-tool-theme
	install -Dm755 src/openbox-tool-version.sh /usr/bin/openbox-tool-version
uninstall:
	rm /usr/bin/openbox-tool-dock \
	/usr/bin/openbox-tool-focus \
	/usr/bin/openbox-tool-placement \
	/usr/bin/openbox-tool-theme \
	/usr/bin/openbox-tool-version
togit:
	git add .
	git commit -m "Updated from makefile"
	git push origin

