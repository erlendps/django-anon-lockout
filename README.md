# Django Anonymous Lockout

Django anonymous lockout is a simple django module for keeping track of failed loging attemps to an endpoint that is protected by some password, but does not require authentication with an authentication backend.

## Installation

Note: does not work yet.

Djano anonymous lockout can be installed with pip:

```bash
pip install django-anon-lockout
```

Then add `anon_lockout` to `INSTALLED_APPS`. It can go in any order.

```python
INSTALLED_APPS = [
    ...,
    anon_lockout,
]
```

Finally migrate the models:

```bash
python manage.py migrate
```

## Usage

Django Anonymous Lockout operates without signals, which means that you will specifically have to call the handler for it to work. The handler is specified in [`handlers.py`](./anon_lockout/handlers.py) (`handle_attempt`). It takes in the ip, wheter the attempt was failed or not and which resource was attempted accessed.

In your code, you would typically check if the password is correct and then call `handle_attempt` with the correct arguments. `handle_attempt` will return `True` if the attempt leads to a lockout, or the user (ip and resource) is already locked out. This means that even though a user might have "authenticated" correctly, if the ip is locked out, it will still not allow the user to see the resource.

To get the IP of an request, you can for instance use this snippet:

```python
def get_ip(request: HttpRequest):
    """Returns the ip (hashed) of the given request."""

    user_ip: str = request.META.get("HTTP_X_FORWARDED_FOR")
    ip: str = ""
    if user_ip:
        ip = user_ip.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return hashlib.sha256(ip.encode("utf-8")).hexdigest()
```

This snippet is also included in `utils`.

### Example

Assuming you have a simple form with the field "password".

`views.py`:

```python
def my_endpoint(request, resource_id):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            if correct_password(password):
                locked = handle_attempt(get_ip(request), failed=False, resource="resource")
                if not locked:
                    return redirect(request, "see-resource")
            else:
                locked = handle_attempt(get_ip(request), failed=True, resource="resource")
                # do more handling here
            if locked:
                form.add_error("password", "Locked out")
    else:
        form = MyForm()
    context = {
      "form": form,
    }
    return render(request, "anon_login.html", context)
```

A working, but very simple example is in [`tests/views.py`](./tests/views.py).

## Configuration

There are 3 settings that you can override:

`LOCKOUT_DURATION`: Decides how long a user is locked out for. Default is 1 day.

`LOCKOUT_THRESHOLD`: Decides how many attempts **in a row** that has to fail for a lockout to occur. Default is 5.

`LOCKOUT_RESET_TIME`: This setting decides how long between two attempts by the same user is needed for the attempt counter to reset. If for instance you set this to 10 minutes, then if a user fails an access to a resource, then assuming the user does not try to access the same resource within 10 minutes, the next time the same user accesses the resource, the counter is reset to 0 failed attempts in a row. Default is 30 minutes.

## Tests

There are a few tests that makes sure the basic funtionality works. These can be run by:

```bash
python manage.py test tests.tests
```

Note: for this to work you would have to clone this repo. It does not work if it is included in `INSTALLED_APPS`.
