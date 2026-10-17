# Contributing to Port of Entry

First off, thank you for considering contributing to Port of Entry! It's people like you that make Port of Entry such a great tool.

## Where do I go from here?

If you've noticed a bug or have a feature request, make one! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.

## Fork & create a branch

If this is something you think you can fix, then fork Port of Entry and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```sh
git checkout -b 325-add-pdf-support
```

## Get the test suite running

Make sure you're using Python 3.8+ and install any necessary dependencies. Currently, the system uses standard library dependencies.

## Make your changes

Make sure you follow our style guide:
- Python code should be formatted with `black`.
- Run `flake8` to ensure there are no linting errors.

## Commit your changes

Commit your changes with a descriptive commit message.

```sh
git commit -m "Add PDF document support"
```

## Submit a pull request

Push your branch to your fork and submit a pull request!
