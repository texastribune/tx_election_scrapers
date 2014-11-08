test:
	@$(foreach file, $(wildcard sos/test_*.py), \
	  python $(file) && ) true
