Texas Elections Scrapers
========================

.. image:: https://travis-ci.org/texastribune/tx_election_scrapers.svg
    :target: https://travis-ci.org/texastribune/tx_election_scrapers

Hi. This is just me fooling around trying to come up a better way to scrape
election results. The tricky logic has been refined in other Texas Tribune
projects, but they were deeply tied to other logic.

The idea is to split the process up into multiple logical steps that other
people might find useful:

1. Ingest results: Typically either with `curl` or `cat` or anything that pipes
   output to stdout.
2. Serialize the output html as JSON: Does not attempt to extract information.
   Just separates data from the html. This is the hard part that scrapers have
   trouble with.
3. Interpret the serialized output: Turns the raw serialized data into
   something you might expect to see from a nice API.

In a Extract, transform, load (ETL) process, this just covers the extractions,
with support for minor transforming.
