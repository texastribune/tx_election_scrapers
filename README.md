Hi. This is just me fooling around trying to come up a better way to scrape
election results.

The idea is to split the process up into multiple logical steps that other
people might find useful:

1. Ingest results: Typically either with `curl` or `cat` or anything that pipes
   output to stdout.
2. Serialize the output html as JSON: Does not attempt to extract information.
   Just separates data from the html. This is the hard part that scrapers have
   trouble with.
3. Interpret the serialized output: Turns the raw serialized data into
   something you might expect to see from a nice API.

This is born from our internal elections scrapers, which attempted to do all
three of those at once and caused much pain.
