# Have I Been Pwned password check (Django password validator)
This is a custom Django password validator that can be integrated within your Django app to prevent users from using Pwned passwords. 

## Why?

* Pwned Passwords are more than half a billion passwords which have previously been exposed in data breaches. 

* Strong password policies aren't prevalent these days.

* Credential stuffing is a real concern and this helps prevent users from using compromised passwords.

* No need to store or maintain a database of compromised passwords.

* Always Query against the latest list of compromised passwords.

## Is this safe?

Recently (05 MARCH 2020), Have I Been Pwned increased its anonymity for checking Pwned passwords on top of their K-anonymity model.
The new anonymity implementation helps consumers of the service to hit the API without worrying about possible inference of queries to hashes via Man-in-the-middle attack or encrypted traffic observation.
This is achieved by padding of response data returned from HIBP as now the response would always consist random number of records between 800 and 1,000.
Thus, API calls to validate pwned passwords is pretty safe and attackers sniffing traffic cannot reasonably determine which hash prefix was searched for by observing the response size.



## How to implement ?

To integrate this within your Django app, simply add the contents of django-validator.py into your validator.py. 
If your project doesn't have a validator.py you can create one within your primary Django project directory. 
Next, add your recently added validator within your Django settings.py like this:

```
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': '<project_path>.validator.HIBPCheck',
    },
]
```

In the above example, replace `<project_path>`  with your path of the validator.py within your Django app.


More on Pwned password check can be found at: https://haveibeenpwned.com/API/v3#PwnedPasswords