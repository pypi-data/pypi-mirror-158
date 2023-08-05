### Overview

The django-cloudflare-restrictor package provides a convient way to restrict access to your application server, such that it will only respond to requests that come via cloudflare's network.

### Installation

Install the package from pypi

```
pip install django-cloudflare-restrictor
```

Add to `INSTALLED APPS` in your settings file 

```
INSTALLED_APPS = [
    'django_cloudflare_restrictor',
    ...
```

And add to `MIDDLEWARE` in your settings file

```
MIDDLEWARE = [
    'django_cloudflare_restrictor.middleware.CloudflareRestrictorMiddleware',
    ...
 ]
```

Set the additional settings as desired

```
CLOUDFLARE_RESTRICTOR_ENABLED = True
CLOUDFLARE_RESTRICTOR_ADDITIONAL_NETWORKS = ["127.0.0.0/8"]
```

If you want to confirm that the IP blocks stored in the django-cloudflare-restrictor package are up to date you can use the `check_cloudflare_ips` command. This will log a warning if the IP addresses are out of date.

```
python manage.py check_cloudflare_ips
```

Based on historical evidence, it appears that Cloudflare gives around 1 month's advance notice of IP address changes, by publishing the new addresses in advance on their site. Updates to these lists are very infrequent (approx once per every 2 years)
