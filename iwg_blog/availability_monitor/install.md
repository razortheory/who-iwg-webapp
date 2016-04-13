1. Add application
=========================

1. Add `availability-monitor` to `INSTALLED_APPS`.
2. Add `availability_monitor.urls` to `ROOT_URLCONF` file.
3. Migrate: `./manage.py migrate availability_monitor`


2. Enable New Relic alerts
================================

1. Go to the `https://newrelic.com` and log in to the account with admin privileges.
2. On the top, open the `SYNTHETICS` tab.
> There you can see the dashboard with all monitors that already working.  

3. Press `Add monitor` button on the right.
4. Set the following settings:
    * Monitor type: `Ping`
    * Monitor name: to project name with specifying environment (Prod/Staging/etc.)
    * Monitor URL: absolute path to API endpoint specified in the `urls.py` (e.g. http://razortheory.com/availability-test/)
    * Validation string: `Passed` (that's the string which monitor would expect to see in the HTTP GET response)
    > Check `Advanced options` - `Verify SSL` if needed.
    * Select monitoring locations
    * Set the schedule (default is 10 minutes)
5. Press `Create my monitor` button.
6. Set notification emails addresses:
    * In the Dashboard select created monitor.
    * In the menu on the left, in Settings group, click on `Alert notifications`.
    * Enter email addresses of users, that should be alerted about problems with availability.


3. Additional Info
====================

* Celery task will run every 10 minutes by default.
* Test will fail, if the last access to database was more than 15 minutes ago.
