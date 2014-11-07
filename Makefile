test:
	@$(foreach file, $(wildcard test_*.py), \
	  python $(file) && ) true
