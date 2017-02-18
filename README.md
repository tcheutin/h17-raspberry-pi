# h17-raspberry-pi

## Team working on this
- Jean-Pierre Bertrand Dorion
- Thierry Cheutin
- Kenzyme Le
- Nicolas Nadeau
- Alain Zakkour
- Raphaël Zumer

## How to start
1. Follow instructions from [HERE](http://www.django-rest-framework.org/#quickstart)

2. Contribute :)

## TODO
- [ ] API
- [x] DB
- [ ] Script
	- [ ] Network
	- [ ] Boot
	- [ ] Nginx
	- [ ] Acces point

## Useful commands
- Create new migration:
`python gti525/manage.py makemigrations`
- Sync the database:
`python gti525/manage.py migrate`
- Create a super user:
`python gti525/manage.py createsuperuser`
- Import fixtures:
`python gti525/manage.py loaddata gti525/api/fixture/*`
- Launch server:
`python gti525/manage.py runserver`
- Curl basic request:
`curl -H 'Accept: application/json; indent=4' -u user:pass http://127.0.0.1:8000/`
