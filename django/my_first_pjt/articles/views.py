from django.shortcuts import rediect, render
from .models import Article

# Create your views here.
def index(request):
    return render(request, 'index.html')
        # 탬플릿을 랜더해서 리턴할수있다

def articles(request):
    articles = Article.objects.all().order_by("-created_at")
    context = {
        "articles": articles,
    }
    return render(request, 'articles.html', context)

def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {"article": article}
    return render(request, "article_detail.html", context)


def data_throw(request):
    return render(request, 'data_throw.html')

def new(request):
    return render(request, 'new.html')

def create(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    Article.objects.create(title=title, content=content)
    return rediect("articles")

def data_catch(request):
    data = request.GET.get("message")
    context = {
        'data': data,
    }
    return render(request, 'data_catch.html', context)


