NAME='openbox-tools'
PREFIX='/usr'
TEMPDIR := $(shell mktemp -u --suffix .$(NAME))

install:
	install -Dm 644 LICENSE $(PREFIX)/share/licenses/$(NAME)/COPYING
	install -Dm 644 README.md $(PREFIX)/share/doc/$(NAME)/README
	install -Dm755 src/openbox-tool-dock.py $(PREFIX)/bin/openbox-tool-dock
	install -Dm755 src/openbox-tool-focus.py $(PREFIX)/bin/openbox-tool-focus
	install -Dm755 src/openbox-tool-placement.py $(PREFIX)/bin/openbox-tool-placement
	install -Dm755 src/openbox-tool-theme.py $(PREFIX)/bin/openbox-tool-theme
	install -Dm755 src/openbox-tool-client-kill.py $(PREFIX)/bin/openbox-tool-client-kill
	install -Dm755 src/openbox-tool-client-renice.py $(PREFIX)/bin/openbox-tool-client-renice
	install -Dm755 src/openbox-tool-client-spawn-new.py $(PREFIX)/bin/openbox-tool-client-spawn-new
	install -Dm755 src/openbox-tool-client-spawn-clone.py $(PREFIX)/bin/openbox-tool-client-spawn-clone
	install -Dm755 src/openbox-tool-version.sh $(PREFIX)/bin/openbox-tool-version
uninstall:
	rm -f $(PREFIX)/share/licenses/$(NAME)/COPYING
	rm -f $(PREFIX)/share/doc/$(NAME)/README
	rm -f $(PREFIX)/bin/openbox-tool-dock
	rm -f $(PREFIX)/bin/openbox-tool-focus
	rm -f $(PREFIX)/bin/openbox-tool-placement
	rm -f $(PREFIX)/bin/openbox-tool-theme
	rm -f $(PREFIX)/bin/openbox-tool-client-kill
	rm -f $(PREFIX)/bin/openbox-tool-client-renice
	rm -f $(PREFIX)/bin/openbox-tool-client-spawn-new
	rm -f $(PREFIX)/bin/openbox-tool-client-spawn-clone
	rm -f $(PREFIX)/bin/openbox-tool-version
togit:
	git add .
	git commit -m "Updated from makefile"
	git push origin

clean:
	rm -f packages/pacman/$(NAME)-*.pkg.tar.xz

pacman:
	mkdir $(TEMPDIR)
	cp packages/pacman/PKGBUILD $(TEMPDIR)/
	cd $(TEMPDIR); makepkg -dr
	cp $(TEMPDIR)/$(NAME)-*.pkg.tar.xz packages/pacman/
	rm -rf $(TEMPDIR)
	@echo Package done!
	@echo Package is in `pwd`/packages/pacman/
