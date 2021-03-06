# gropen

`gropen` (Git Remote Open) is a simple command line application for opening
local files and directories on remote git repositories.

Supported remote repos:

- [x] GitHub;
- [x] Bitbucket;
- [ ] GitLab.

# Installation

```
pip install gropen
```

*NOTE:* `gropen` requires Python 3.6 or greater installed on your environment.

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

- [x] Add support for remote repos on GitHub;
- [x] Add support for remote repos on Bitbucket;
- [ ] Add support for remote repos on GitLab;
- [x] Open current directory;
- [x] Open arbitrary directory and files;
- [x] Point out the line(s) of code to be highlighted;
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
