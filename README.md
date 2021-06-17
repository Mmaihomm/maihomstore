## Project setup
- `cd maihomproject` 
- `python3 -m venv env`
- `source env/bin/activate`
- `pip install -r requirements.txt`

## Start Develop
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver 0.0.0.0:8000`
## init data
- `python manage.py loaddata jsondata/maihomstore.categories.json`
- `python manage.py loaddata jsondata/maihomstore.product.json`
- `python manage.py loaddata jsondata/maihomstore.cantact.json`
- `python manage.py loaddata jsondata/maihomstore.productimage.json`