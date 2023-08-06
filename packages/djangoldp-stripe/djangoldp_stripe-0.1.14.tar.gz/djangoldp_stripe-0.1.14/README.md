# djangoldp-stripe

A DjangoLDP package supporting Stripe payments. Uses dependency [dj-stripe](https://github.com/dj-stripe/dj-stripe) to achieve much of the functionality, a library for handling Stripe payments in Django

# Requirements

* djangoldp 2.1
* Python 3.6.5

* Requires the installation of a [DjangoLDP server](https://docs.startinblox.com/import_documentation/djangoldp_guide/install-djangoldp-server.html)

* You will need to set up a [Stripe client](https://dashboard.stripe.com/test/dashboard)

# Installation

* You will need to set the following settings to your settings.yml:

```yaml
dependencies:
   # ...
   - djangoldp-stripe

ldp_packages:
   # ...
   - djangoldp_stripe

server:
   # ...
   STRIPE_LIVE_MODE: True  # Should be False when testing, True in production
   DJSTRIPE_USE_NATIVE_JSONFIELD: True  # if using SQLite, set this to False
   DJSTRIPE_FOREIGN_KEY_TO_FIELD: "id"
```

* Set `STRIPE_LIVE_SECRET_KEY` and `STRIPE_TEST_SECRET_KEY` in your OS environment variables where the server is run. These settings will then be securely imported when you next configure. Alternatively, you can add them to the settings.yml:

```yaml
server:
    # ...
    STRIPE_LIVE_SECRET_KEY: ""
    STRIPE_TEST_SECRET_KEY: ""
```

You can find these settings via the [Stripe dashboard](https://dashboard.stripe.com/)

* Optionally you can change the setting `LDP_STRIPE_URL_PATH` to change the path where Django Stripe's urls will be accessible. By default it is `"stripe/"`, i.e. `http://localhost:8080/stripe/`. These urls are provided by [DjStripe](https://github.com/dj-stripe/dj-stripe/blob/master/djstripe/urls.py) and implement all of the necessary webhooks to keep your Stripe data sync'ed with your Django data

* In the Stripe dashboard, register a [webhook](https://stripe.com/docs/webhooks) listening to all events (or just those you want to keep up-to-date) and point them to your API url + your webhook endpoint. So if your API was hosted on `https://yoursite.com/` and you didn't change the `LDP_STRIPE_URL_PATH`, then the endpoint would be `https://yoursite.com/stripe/webhooks/`

* In the created webhooks, find your webhook secret, and set this in the OS variable (or server setting) `DJSTRIPE_WEBHOOK_SECRET`. It is a string which will start `whsec_`

* Optionally add `djangoldp_stripe.middleware.StripeSubscriptionRequiredMiddleware` to your `MIDDLEWARE` settings in `settings.yml`. When this middleware is included then it will restrict access to certain requests so that they are only accessible by users with an active subscription. Add a list of all paths which should be restricted to the setting `INCLUDE_FROM_GLOBAL_STRIPE_SUBSCRIPTION_REQ`

```yaml
server:
   # ...
   MIDDLEWARE:
     - "djangoldp_stripe.middleware.StripeSubscriptionRequiredMiddleware"
   INCLUDE_FROM_GLOBAL_STRIPE_SUBSCRIPTION_REQ:
     - '/my-custom-path/'
```

Note that this middleware does not check that an anonymous user is subscribed. To prevent this being a problem, make sure that your server does not give anonymous users permissions that they shouldn't have, so that they must login before accessing the application

* Optionally add the setting `REDIRECT_URL_NO_SUBSCRIPTION` if you plan to use `UserHasValidSubscriptionView` and wish to modify its' behaviour, e.g. `http://localhost:8000/checkout-session/?lookup_key=test-subscription` or `http://localhost:8000/checkout-session/?price_id=price_1KOPEhIK99puQD1xtbSN94fk`

* Run `djangoldp install`

* Run `djangoldp configure`

* Run `python manage.py djstripe_sync_models`. Anytime you run this command your database will be manually synchronised with your Stripe records. If for example your site went down for a time, you should re-run this command

## Migrating existing customers

After configuration, you can do this by running:

```
djangoldp configure
python manage.py djstripe_init_customers
python manage.py djstripe_sync_plans_from_stripe
```

# StripeSubscriptionPermissions

This package can be used to provide custom permissions on your models and views. To do this you can use the permissions class `StripeSubscriptionPermissions` or the utility functions in `permissions.py`

* Set up the required product permissions on your model:

```python
class MyModel(Model):
    # ...

    class Meta(Model.Meta):
       # ...
       PERMS_REQUIRED_STRIPE_SUBSCRIPTIONS = ['prod_xxxx',]
```

When applying either the permission class to a `LDPViewSet` or the utility function, you can now control access based on the products a requesting user is subscribed to

# Views

Making a GET request to `/user-valid-subscriptions/` will return in JSON-LD the serialized products which the authenticated user is subscribed to. It will only return those which are valid subscriptions (e.g. excluding those which have expired)

```json
{
   "@context": [...],
   "@type": "ldp:Container",
   "@id": "http://yourserver/user-valid-subscriptions/",
   "ldp:contains": [
      {
         "name": "My Awesome Product",
         "id": "prod_xxxx"
      }
   ]
}
```
