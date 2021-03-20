# gropen
![PyPI](https://img.shields.io/pypi/v/gropen)
[![Maintainability](https://api.codeclimate.com/v1/badges/513113a78c8843c094a2/maintainability)](https://codeclimate.com/github/tiagopog/gropen/maintainability)

`gropen` (Git Remote Open) is a simple command line application for opening
local files and directories on remote git repositories.

![gropen_example](https://user-images.githubusercontent.com/760933/111877395-f8a0b400-8981-11eb-98c8-ad5f0a21b78d.gif)

Current support:

- [x] GitHub;
- [x] Bitbucket;
- [ ] GitLab.

# Installation

```
pip install gropen
```

**NOTE:** `gropen` requires Python 3.6 or greater installed on your local environment.

# Usage

Here are some example of what `gropen` can open on your project's remote repo.

Open current directory:

```
gropen .
```

Open another directory:

```
gropen gropen/
```

Open a file:

```
gropen gropen/gropen.py
```

Open a file pointing out the lines of code to be highlighted:

```
gropen gropen/gropen.py:42
gropen gropen/gropen.py:16,32
```

# TODO

- [x] Add support for GitHub repositories;
- [x] Add support for Bitbucket repositories;
- [ ] Add support for GitLab repositories;
- [x] Open current directory;
- [x] Open arbitrary directory and files;
- [x] Point out the line(s) of code to be highlighted;
- [ ] Open files in a specific commit;
- [ ] Handle relative paths;
- [ ] Create Vim plugin;
- [ ] Create VS Code plugin;
- [ ] Create Sublime plugin.

# Contributing

Bug reports and pull requests are welcome on GitHub at [https://github.com/tiagopog/gropen/](https://github.com/tiagopog/gropen/).
This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the
[Contributor Covenant](https://www.contributor-covenant.org/) code of conduct.

# License

This package is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
