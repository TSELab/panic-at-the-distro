Currently, we run the following analyzers:

## JavaScript Analyzer
python3 javascript_analyzer.py input-path output-path

## Python Analyzer

python3 python3_analyzer.py input-path output-path

## RubyGems Analyzer

python3 ruby_analyer.py input-path output-path

To run all the analyzers, we first need to install the dependencies in the [Pipfile.lock](Pipfile.lock) with [pipenv](https://pipenv.pypa.io/en/latest/).
For the RubyGems analyzer, we have to install the dependencies of packj detailed at [this link](https://github.com/ossillate-inc/packj?tab=readme-ov-file#3-source-repo) I would recommend installing the dependencies at the system level (without using virtual environments). 
