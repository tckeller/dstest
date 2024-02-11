DSTest
======

I have an idea for a data science productivity framework based on unit testing. 
This is a Work in progress. Let's see where it goes. 

Roadmap
-------
These are the features I currently want to implement

- [X] Tests
  - [X] Basic scan and execution of tests
  - [X] Make it possible to run all tests in directory
  - [X] Make it possible to run individual test in module
- [X] Fixtures
  - [X] Basic dependency injection for fixtures
  - [X] Caching
  - [ ] Fixture Testing
- Experiment Results
  - [X] Result Registry
  - [X] Log Metrics
  - [X] Log Parameters
  - [ ] Log Plots (MPL & Plotly)
- [ ] Output & Presentation
  - [X] Progress Bar
  - [X] Present Results in console
  - [X] Output Result in CSV File
  - [X] Output results into readable file (Markdown)
    - [X] Parse Docstrings
    - [ ] Parse Code
  - [ ] Output results as Html
- [ ] Advanced Features
  - [ ] Make it possible to not rerun experiments and still see the results
  - [ ] Interactive CLI interface which shows you which module were found and allows you tu run them individually. 
  - [ ] Pycharm Plugin
- [ ] Documentation & Examples