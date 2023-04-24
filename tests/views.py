from django.shortcuts import render
from django.http import HttpRequest
from tests.forms import SimpleForm
from anon_lockout.handlers import handle_attempt


def index(request: HttpRequest):
    if request.method == "POST":
        form = SimpleForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] == "password":
                locked = handle_attempt(request, False, "index")
                text = "Logged in"
            else:
                locked = handle_attempt(request, True, "index")
                text = "Not logged in"
            if locked:
                form.add_error("password", "You are locked out.")

    else:
        form = SimpleForm()
        text = "Try to log in"
    return render(request, "index.html", {"form": form, "text": text})
