# OpenElections Data D.C. [![Build Status](https://github.com/openelections/openelections-data-dc/actions/workflows/format_tests.yml/badge.svg?branch=master)](https://github.com/openelections/openelections-data-dc/actions)

Pre-processed election results for District of Columbia elections

This repository contains pre-processed election results from the District of Columbia, formatted to be ingested into the OpenElections [processing pipeline](http://docs.openelections.net/guide/). It contains mostly CSV files converted from PDF tables. Interested in contributing? We have a bunch of [easy tasks](https://github.com/openelections/openelections-data-dc/labels/easy%20task) for you to tackle.

Use [this header row](https://gist.github.com/dwillis/c93ffe5954df21a0e75c) for precinct-level D.C. results (for ward and city-wide results, just remove the `precinct` column). Each row of a CSV file represents a single result for a single candidate in a race and jurisdiction, even if the original data has multiple candidates in a single row. Vote totals do not contain commas or other formatting. Parties and candidates should appear exactly as they appear in the original file. The names of the CSV files should correspond to our [naming conventions](http://docs.openelections.net/archive-standardization/).

Here are the offices we care about: President, Delegate to the House of Representatives (but not shadow senators or representatives), Mayor, City Council and Board of Education. We do not need ANC results, but if you want to include them, feel free. For at-large offices, put "At Large" in the `district` column.

For extracting text from PDF tables,we recommend [Tabula](http://tabula.technology/), which can be installed and run locally on OSX, Windows or Linux.

If you're familiar with git and Github, clone this repository and get started. If not, you can still help: leave a comment on a task you'd like to work on, or just convert any of the files into CSV and send the result to openelections@gmail.com.
