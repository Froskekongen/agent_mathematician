BUMP ?= patch

.PHONY: release test

test:
	python3 -m unittest discover -s mathematician/tests -p 'test_*.py'

release:
	@if [ -n "$(VERSION)" ]; then \
		python3 scripts/release.py --version "$(VERSION)"; \
	else \
		python3 scripts/release.py --bump "$(BUMP)"; \
	fi
