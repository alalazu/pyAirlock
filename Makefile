#
# pyAirlock - Python lybrary for Airlock products REST APIs
#

TOPDIR = `pwd`
NAME=pyAirlock
LATEST_RELEASE = `find releases -type f -name pyAirlock-\* -print | sed -e 's,releases/pyAirlock-\(.*\)\.tar.gz,\1,' | sort -rnt . | head -n 1`
V_PYAIRLOCK	= `grep VERSION src/pyAirlock/const.py | sed -e "s/VERSION[ \t]*=[ \t]*'\([^']*\).*/\1/"`

all:
	@echo "Valid targets are:"
	@echo "	dist            - create distributable tar file in ./releases"
	@echo "	ebuild          - create Gentoo ebuild"
	@echo "	deploy          - deploy Gentoo ebuild"
	@echo "	pushout         - create & deploy Gentoo ebuild, ready for syncing on target systems with 'layman -S'"
	@echo "	clean           - maintainer-clean of all subdirectories"

dist: releases
	(cd src; python ./setup.py sdist)
	mv src/dist/pyAirlock-${V_PYAIRLOCK}.tar.bz2 ./releases/$(NAME)-${V_PYAIRLOCK}.tar.bz2
	-rmdir src/dist

ebuild:
	$(MAKE) -C ebuilds

deploy:
	$(MAKE) -C ebuilds deploy

pushout: cleanManifest dist ebuild deploy

cleanManifest:
	-rm ebuilds/app-admin/$(NAME)/Manifest
	
clean:
	find src -name \*.pyc -delete
	-rm -rf src/dist
	-rm -rf src/build
	-rm src/MANIFEST
	$(MAKE) -C ebuilds clean

releases:
	mkdir releases
