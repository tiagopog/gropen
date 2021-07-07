# gropen

![PyPI](https://img.shields.io/pypi/v/gropen)
[![Maintainability](https://api.codeclimate.com/v1/badges/513113a78c8843c094a2/maintainability)](https://codeclimate.com/github/tiagopog/gropen/maintainability)

`gropen` (Git Remote Open) is a simple command line application for opening
local files and directories on remote git repositories.

![gropen_example](https://user-images.githubusercontent.com/760933/111877395-f8a0b400-8981-11eb-98c8-ad5f0a21b78d.gif)

## Supported repos

- [x] Bitbucket
- [x] GitHub
- [ ] GitLab

## Supported editors

- [ ] Sublime
- [x] Vim ([gropen.vim](https://github.com/tiagopog/gropen.vim))
- [x] VS Code ([gropen.vscode](https://github.com/tiagopog/gropen-vscode))

# Supported systems

- [ ] Linux
- [x] Macos
- [ ] Windows

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

Open file from an outter directory:

```
cd ~/Dev
gropen python/gropen/gropen/gropen.py:20,30
```

Open file from an inner directory:

```
cd ~/Dev/python/gropen/gropen
gropen gropen.py:20,30
```

# TODO

- [x] Add support for GitHub repositories;
- [x] Add support for Bitbucket repositories;
- [ ] Add support for GitLab repositories;
- [x] Open current directory;
- [x] Open arbitrary directory and files;
- [x] Open in a line or range of lines in the file;
- [ ] Open files in a specific commit;
- [x] Handle relative and absolute paths;
- [ ] Support flag for only displaying the URL instead of opening it on the browser;
- [x] Create Vim plugin;
- [ ] Create VS Code plugin;
- [ ] Create Sublime plugin.

# Contributing

Bug reports and pull requests are welcome on GitHub at [https://github.com/tiagopog/gropen/](https://github.com/tiagopog/gropen/).
This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the
[Contributor Covenant](https://www.contributor-covenant.org/) code of conduct.

# License

This package is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
