# SQLLMConverter

# Basic Info:
## ec2 instance (mysql & sqlite)
- ssh -i xxx/cs511-key.pem ubuntu@ec2-18-117-190-220.us-east-2.compute.amazonaws.com 
- sudo mysql -u root
- Converter: https://github.com/techouse/sqlite3-to-mysql
- pip3 install sqlite3-to-mysql
- sudo sqlite3mysql -f ~/spider/database/academic/academic.sqlite -d academic -u root
- sudo sqlite3mysql -f ~/spider/database/bike_1/bike_1.sqlite -d bike_1 -u cs511 --mysql-password cs511password
- user: -u root -p 123456 / -u cs511 -p cs511password
- split queries: https://drive.google.com/file/d/1Bc-j40KcviE-NSM-7FRupGlyKa6j_U6c/view?usp=sharing


