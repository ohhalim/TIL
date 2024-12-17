from django.shortcuts import render
from .models import Article

# Create your views here.
def index(request):
    return render(request, 'index.html')
        # 탬플릿을 랜더해서 리턴할수있다

def articles(request):
    articles = Article.objects.all()
    return render(request, 'articles.html')

def data_throw(request):
    return render(request, 'data_throw.html')


def data_catch(request):
    data = request.GET.get("message")
    context = {
        'data': data,
    }
    return render(request, 'data_catch.html', context)


