# ITCrowd

Named after a British sitcom `The IT Crowd` because I've similiar job descs as Moss and Roy at the time I wrote this app. Do not expect sleek lines of code since I wrote this when still learning Python and Django.

ITCrowd is a Trello/kanban clone with customized flows to fill my own needs. I didn't remember the `root` and other users password except my own. You can login with username `piko` and `okip` as password to manage other user(s). The db already feeded up with dump data to help you understand how to work with this app.

<img src="https://cloud.githubusercontent.com/assets/2534060/22257731/83778e24-e291-11e6-860e-73655b6b35f6.png">

## Requirements

- Python 2.7.x
- Sqlite3
- See `requirements.txt`

## Run

- `$ pip install -r requirements.txt`
- `$ python manage.py runserver localhost:8000` then open `http://localhost:8000` in your browser.

## Todo

The views for `Orang` and `Kategori` still missing. I was managed them manually through sqlite3 shell. Please send PR.

