# 1. Setup tools (for Windows)
## 1.1. Install poetry
#### `curl -sSL https://install.python-poetry.org | python` on bash.
#### poetry path is `"$HOME/AppData/Roaming/Python/Scripts/poetry.exe"`.
#### Add this to PATH.

## 1.2. Install pyenv
#### `git clone https://github.com/pyenv-win/pyenv-win.git "$HOME/.pyenv"` on bash.
#### pyenv path is `"$HOME/.pyenv/pyenv-win/bin/pyenv"`.
#### Add this to PATH.

# 1. Setup tools (for Mac or Linux)
## 1.1. Install poetry
#### `curl -sSL https://install.python-poetry.org | python` on bash.
#### poetry path is `"$HOME/.local/bin/poetry"`.
#### Add this to PATH.
#### `echo "PATH=$HOME/.local/bin:\$PATH" >> "$HOME/.bash_profile"` on bash.
#### `source "$HOME/.bash_profile"` on bash.

## 1.2. Install pyenv
#### `git clone https://github.com/pyenv/pyenv.git ~/.pyenv` on bash.
#### pyenv path is `"$HOME/.pyenv/bin/pyenv"`.
#### Add this PATH.
#### `echo "export PYENV_ROOT=$HOME/.pyenv" >> "$HOME/.bash_profile"` on bash.
#### `echo "export PATH=$PYENV_ROOT/shims:\$PATH" >> "$HOME/.bash_profile"` on bash. 
#### `source "$HOME/.bash_profile"` on bash.

## 1.5. Setup creator environment
#### `mkdir src`
#### `cd src`
#### `poetry init`

# 2. Setup use environment
#### `pyenv install 3.10.0`
#### `pyenv rehash`
#### `pyenv local 3.10.0`

