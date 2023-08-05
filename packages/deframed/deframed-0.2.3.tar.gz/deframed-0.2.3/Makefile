#!/usr/bin/make -f

.PHONY: doc test update all tag pypi upload

all: dirs\
	deframed/static/ext/msgpack.min.js  \
	deframed/static/ext/mustache.min.js \
	deframed/static/ext/jquery.min.js   \
	deframed/static/ext/poppler.min.js   \
	deframed/static/ext/bootstrap.min.js   \
	deframed/static/ext/bootstrap.min.css

dirs: deframed/static/ext
deframed/static/ext:
	mkdir $@
deframed/static/ext/msgpack.min.js:
	wget -O $@ "https://github.com/ygoe/msgpack.js/raw/master/msgpack.min.js"

deframed/static/ext/mustache.min.js:
	wget -O $@ "https://github.com/janl/mustache.js/raw/master/mustache.min.js"

deframed/static/ext/jquery.min.js:
	wget -O $@ "https://code.jquery.com/jquery-3.4.1.slim.min.js"

deframed/static/ext/poppler.min.js:
	wget -O $@ "https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"

deframed/static/ext/bootstrap.min.js:
	wget -O $@ "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"


#deframed/static/ext/cash.min.js:
#	wget -O $@ "https://github.com/fabiospampinato/cash/raw/master/dist/cash.min.js"

deframed/static/ext/bootstrap.min.css:
	wget -O $@ "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"


PACKAGE=deframed
ifneq ($(wildcard /usr/share/sourcemgr/make/py),)
	include /usr/share/sourcemgr/make/py
else
	# OK so you really shouldn't do that, but …
	@echo You should install smurfix/sourcemgr.
	@wget -q -o /tmp/mk.$$ https://raw.githubusercontent.com/smurfix/sourcemgr/master/share/make/py
	include /tmp/mk.$$
	@rm /tmp/mk.$$
endif

