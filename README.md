# h17-raspberry-pi

## Team working on this
- Jean-Pierre Bertrand Dorion
- Thierry Cheutin
- Kenzyme Le
- Nicolas Nadeau
- Alain Zakkour
- Raphaël Zumer

## How to start
1. `pip install -r requirements.txt`

2. Read the [framework reference](http://www.django-rest-framework.org/)

3. Contribute :)

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
`python gti525/manage.py runserver 0.0.0.0:8000 --noreload`
- Clear all data from the database:
`python gti525/manage.py flush`
