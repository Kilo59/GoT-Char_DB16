# GoT-Char_DB16

[![Python package](https://github.com/Kilo59/GoT-Char_DB16/actions/workflows/python-package.yml/badge.svg)](https://github.com/Kilo59/GoT-Char_DB16/actions/workflows/python-package.yml)

Partial (Incomplete) Database of major Characters from the Game of Thrones universe

https://gotdb-api.herokuapp.com/

## Coming soon

REST API with OAuth scopes that protect users from spoilers.

### TODO

- [ ] Models
- [ ] REST API
  - [ ] Locale
  - [ ] Death
  - [ ] Character
  - [x] Houses
  - [ ] Book
- [x] Heroku Deploy
- [ ] Update from data csv
- [ ] Basic OAuth integration
- [ ] Google Based Oauth /login or /token
- [ ] Scopes to protect user from spoilers
- [ ] Enable OAuth code flow from Swagger

## Quick start

### Requires

- [python 3.7 or above](https://realpython.com/installing-python/)
- `pipenv`

### Optional

- [`pipx` for isolated pipenv install](https://pypa.github.io/pipx/)

1. Install `pipenv`
   - `pipx install pipenv` or `pip install pipenv`
2. Create virtual environment and install dependencies.
   - Windows: `pipenv install` (dependencies must be re-resolved for windows)
   - MacOS & Linux: `pipenv sync` (can synchronize with the pre-resolved dependencies)
3. Start the Webserver
   - `pipenv run app`
4. Open your browser
   - http://localhost:8000/
