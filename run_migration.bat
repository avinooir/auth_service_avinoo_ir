@echo off
echo Running SSO migration and setup...
python manage.py migrate sso
python scripts/update_sso_clients.py
echo Done!
pause
