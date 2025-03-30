from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpResponse

def hello_world(request):
    names = request.GET.getlist('name')
    lang = request.GET.get('lang', 'en')

    if not all(name.isalpha() for name in names):
        return HttpResponse('You must enter a valid name', status=400)
    
    names = ', '.join(names)
    if not names:
        names = 'World'
    
    
    if lang == 'es':
        return HttpResponse(f'Hola, {names}!')
    elif lang == 'fr':
        return HttpResponse(f'Bonjour, {names}!')
    else:
        return HttpResponse(f'Hello, {names}!')

def custom_404(request, exception):
    return HttpResponse('404 Not Found', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('task2/',include('products.urls'))
]
