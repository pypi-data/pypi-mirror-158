=======
Commons
=======

Commons is a Django app that includes commonly used
serializer, models, pagination and mixins while developing an
API with DjangoRestFramework .


Quick start
-----------

1. Add "commons" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...
        'commons',

    ]

2. Include the polls URLconf in your project urls.py like this:

    path('commons/', include('commons.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server
