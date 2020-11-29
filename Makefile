SRC_DIR := ./src

current-version:
	@echo "Current version is `cat ${SRC_DIR}/__init__.py | awk -F '("|")' '{ print($$2)}'`"

git-release:
	git add ${SRC_DIR}/__init__.py
	git commit -m "New version `cat ${SRC_DIR}/__init__.py | awk -F '\"' '{print($$2)}' | awk -F . '{OFS=\".\";print($$1,$$2,$$3)}'`"
	INPUT_VERSION=`cat ${SRC_DIR}/__init__.py | awk -F '\"' '{print($$2)}'` \
	&& git tag "$$INPUT_VERSION" \
	&& echo "`gitchangelog`" > ./CHANGELOG.rst \
	&& git add ./CHANGELOG.rst \
	&& git commit -m "Changelog updated" \
	&& git push origin "$$INPUT_VERSION" \
	&& git push origin -u "$(shell git rev-parse --abbrev-ref HEAD)"

_release-patch:
	@echo "__version__ = \"`cat ${SRC_DIR}/__init__.py | awk -F '\"' '{print($$2)}' | awk -F . '{OFS=\".\";print($$1,$$2,$$(NF) + 1)}' | sed 's/ /./g' `\"" > ${SRC_DIR}/__init__.py
release-patch: _release-patch git-release current-version

_release-minor:
	@echo "__version__ = \"`cat ${SRC_DIR}/__init__.py | awk -F '\"' '{print($$2)}' | awk -F . '{OFS=\".\";print($$1,$$(NF-1) + 1,0)}' | sed 's/ /./g' `\"" > ${SRC_DIR}/__init__.py
release-minor: _release-minor git-release current-version

_release-major:
	@echo "__version__ = \"`cat ${SRC_DIR}/__init__.py | awk -F '\"' '{print($$2)}' | awk -F . '{OFS=\".\";print($$(NF-2) + 1,0,0)}' | sed 's/ /./g' `\"" > ${SRC_DIR}/__init__.py
release-major: _release-major git-release current-version

release: release-patch
