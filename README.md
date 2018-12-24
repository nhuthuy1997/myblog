* Myblog: Trang web thu thấp tin tức từ các trang
  - Viblo
  - Techblog
  - JamViet
  - ITviec

* 3rd application:
 - redis-server
 - mysql

* Step by step to run:
  - . env/bin/active
  - python manage.py makemigrate
  - python manage.py migration
  - redis-server
  - python manage.py rqworker default

* Seed data:
  - SourceInfo....
