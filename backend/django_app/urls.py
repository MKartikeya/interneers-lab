from django.contrib import admin
from django.urls import path
from django.http import JsonResponse, HttpResponse

def hello_world(request):
    names = request.GET.getlist('name')
    lang = request.GET.get('lang', 'en')

    names = ', '.join(names)
    if not names:
        names = 'World'
    
    if not names.isalpha():
        return HttpResponse('You must enter a valid name', status=400)
        # return JsonResponse({'message': 'You must enter a valid name'}, status
    user_agent = request.headers.get('User-Agent', 'Unknown')
    print(f'User-Agent: {user_agent}')
    print(request.headers)
    if lang == 'es':
        return HttpResponse(f'Hola, {names}!')
    elif lang == 'fr':
        return HttpResponse(f'Bonjour, {names}!')
    else:
        return HttpResponse(f'Hello, {names}!')
    return HttpResponse(f'Hello, {names}!')
    # return JsonResponse({'message': f'Hello, {name}!'})

def custom_404(request, exception):
    return HttpResponse('404 Not Found', status=404)
    # return JsonResponse({'message': 'I didn\'t put anything in this yet!'}, status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
]

handler404 = custom_404


