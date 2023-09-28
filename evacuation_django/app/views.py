from django.shortcuts import render

# Create your views here.
def index_page (request):
    # Подготовка данных. (в виде словаря)
    context = {}
    context['test'] = 'Test text'
    return render(request, 'index.html', context)

def test (request):
    # Подготовка данных. (в виде словаря)
    context = {}
    context['test'] = 'Test text'
    return render(request, 'test.html', context)