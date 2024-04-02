# Sau khi git clone về thành công, ta thực hiện các steps như sau:

# Step 1: Tải và cài đặt pipenv

pip install pipenv
pipenv shell

# Step 2: Ngay tại thư mục supersport ngoài cùng, chạy và cài đặt các dependencies

pipenv install

# Step 3: Mở workbench mysql, đăng nhập vào local và tạo đúng tên là supersportdb

# Step 4: Truy cập vào settings.py, tìm đến DATABASES

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql',
'NAME': 'supersportdb',
'USER': '<Điền tên user đăng nhập ở workbench>',
'PASSWORD': '<Điền pass đăng nhập ở workbench>',
'HOST':'localhost',
'PORT':'3306',
}
}

# Step 5: Chạy migrate để update app

python manage.py migrate

# Step 6: Tạo super user cho mình

python manage.py createsuperuser

# Step 7: Chạy migrate phát nữa và khởi chạy server

python manage.py migrate
python manage.py runserver

# Step 8: Truy cập vào trang admin localhost:8000/admin và nhập user, pass như Step 6
