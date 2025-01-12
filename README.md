# 1. Setup tools (for Windows)
## 1.1. Install poetry
#### `curl -sSL https://install.python-poetry.org | python` on bash.
#### poetry path is `"$HOME/AppData/Roaming/Python/Scripts/poetry.exe"`.
#### Add this to PATH.
#### `echo "export PATH=$HOME/AppData/Roaming/Python/Scripts:\$PATH" >> "$HOME/.bash_profile"` on bash.
#### `source "$HOME/.bash_profile"` on bash.

## 1.2. Install pyenv
#### `git clone https://github.com/pyenv-win/pyenv-win.git "$HOME/.pyenv"` on bash.
#### pyenv path is `"$HOME/.pyenv/pyenv-win/bin/pyenv"`.
#### Add this to PATH.
#### `echo "export PYENV=$HOME/.pyenv/pyenv-win" >> "$HOME/.bash_profile"` on bash.
#### `echo "export PYENV_ROOT=$HOME/.pyenv/pyenv-win" >> "$HOME/.bash_profile"` on bash.
#### `echo "export PYENV_HOME=$HOME/.pyenv/pyenv-win" >> "$HOME/.bash_profile"` on bash.
#### `source "$HOME/.bash_profile"` on bash.
#### `echo "export PATH=$HOME/.pyenv/pyenv-win/bin:\$PATH" >> "$HOME/.bash_profile"` on bash. 
#### `echo "export PATH=$HOME/.pyenv/pyenv-win/shims:\$PATH" >> "$HOME/.bash_profile"` on bash. 
#### `source "$HOME/.bash_profile"` on bash.

# 1. Setup tools (for Mac or Linux)
## 1.1. Install poetry
#### `curl -sSL https://install.python-poetry.org | python` on bash.
#### poetry path is `"$HOME/.local/bin/poetry"`.
#### Add this to PATH.
#### `echo "export PATH=$HOME/.local/bin:\$PATH" >> "$HOME/.bash_profile"` on bash.
#### `source "$HOME/.bash_profile"` on bash.

## 1.2. Install pyenv
#### `git clone https://github.com/pyenv/pyenv.git ~/.pyenv` on bash.
#### pyenv path is `"$HOME/.pyenv/bin/pyenv"`.
#### Add this PATH.
#### `echo "export PYENV=$HOME/.pyenv" >> "$HOME/.bash_profile"` on bash.
#### `source "$HOME/.bash_profile"` on bash.
#### `echo "export PATH=$PYENV/bin:\$PATH" >> "$HOME/.bash_profile"` on bash. 
#### `echo "export PATH=$PYENV/shims:\$PATH" >> "$HOME/.bash_profile"` on bash. 
#### `source "$HOME/.bash_profile"` on bash.

## 1.5. Setup creator environment
#### `mkdir src`
#### `cd src`
#### `poetry init`

# 2. Setup python local environment.
#### `cd src` on bash.
#### `poetry config virtualenvs.in-project true --local` on bash.
#### Installation environment.
#### `pyenv install 3.10.0` on bash.
#### `pyenv rehash` on bash.
#### `pyenv local 3.10.0` on bash.
#### `poetry install --no-root` on bash.

# 3. Show GUI App.
#### `poetry run python main.py`
