exe=bin/*
install:
	install -Dm755 bin/* /usr/bin
uninstall:
	echo NO IMPLEMENTADOOOO!!!!!
togit:
	git add .
	git commit -m "Updated from makefile"
	git push origin

