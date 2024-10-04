from django.shortcuts import redirect


def go_to_api_root(request):
    return redirect("/store/")
