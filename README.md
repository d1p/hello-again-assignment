## Installation
### Requirements:
 - Docker Compose

#### or

   - Python3 (3.6+)
   - Pip3
   - Pipenv
   - Postgresql
   - Redis

### Docker Compose
1. Clone the repository
2. Run `docker-compose up`
3. Run `docker-compose exec web python manage.py migrate`
4. Run `docker-compose exec web python manage.py createsuperuser`

### Manual
1. Clone the repository
2. Create a virtual environment with `pipenv shell`
3. Install the requirements with `pipenv install`
4. Create a postgresql database
5. Create redis instance
6. Edit the `.env` file with your database, redis credentials
7. Run `python manage.py migrate`
8. Run `python manage.py createsuperuser`
9. Run `python manage.py runserver`

### Testing
1. Run `docker-compose exec web python manage.py test`

## Posible improvements
- Add more tests
- Add more documentation
- Create upstert task for updating the data
- Add more fields to the model
- Add more filters to the admin
- Optimize docker image

## License
[MIT](https://choosealicense.com/licenses/mit/)


## Important
This project is created for assignment purposes only. It is not intended for production use.