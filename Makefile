SRC_DIR := ./src

current-version:
	@echo "Current version is `cat ${SRC_DIR}/__init__.py | awk -F '("|")' '{ print($$2)}'`"

git-release:
	git add ${SRC_DIR}/__init__.py
	git commit -m "New version `cat ${SRC_DIR}/__init__.py | awk -F '\"' '{print($$2)}' | awk -F . '{OFS=\".\";print($$1,$$2,$$3)}'`"
	INPUT_VERSION=`cat ${SRC_DIR}/__init__.py | awk -F '\"' '{print($$2)}'` \
	&& git tag "$$INPUT_VERSION" \
	&& git push origin "$$INPUT_VERSION" \
	&& git push origin -u "$(shell git rev-parse --abbrev-ref HEAD)"

_update_changelog:
	@echo "`gitchangelog`" > ./CHANGELOG.rst

_release-patch:
	@echo "version = \"`cat ${SRC_DIR}/__init__.py | awk -F '\"' '{print($$2)}' | awk -F . '{OFS=\".\";print($$1,$$2,$$(NF) + 1)}' | sed 's/ /./g' `\"" > ${SRC_DIR}/__init__.py
release-patch: _release-patch git-release _update_changelog current-version

_release-minor:
	@echo "version = \"`cat ${SRC_DIR}/__init__.py | awk -F '\"' '{print($$2)}' | awk -F . '{OFS=\".\";print($$1,$$(NF-1) + 1,0)}' | sed 's/ /./g' `\"" > ${SRC_DIR}/__init__.py
release-minor: _release-minor git-release _update_changelog current-version

_release-major:
	@echo "version = \"`cat ${SRC_DIR}/__init__.py | awk -F '\"' '{print($$2)}' | awk -F . '{OFS=\".\";print($$(NF-2) + 1,0,0)}' | sed 's/ /./g' `\"" > ${SRC_DIR}/__init__.py
release-major: _release-major git-release _update_changelog current-version

release: release-patch
