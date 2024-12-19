from django.shortcuts import redirect, render
from .models import Article
from .forms import ArticleForm

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
    forms = ArticleForm()
    context = {"forms": forms}
    return render(request, 'new.html', context)

def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            # 데이터를 지정하고
            article = form.save()
            # 다른곳으로 리다이렉트
            return redirect("article_detail", article.pk)
    else: 
        form = ArticleForm()
    
    return redirect("new")

    # title = request.POST.get("title")
    # content = request.POST.get("content")
    # article = Article.objects.create(title=title, content=content)
    # return redirect("article_detail", article.pk)

def edit(request, pk):
    article = Article.objects.get(pk=pk)
    context = {"article": article}
    return render(request, "edit.html", context)

def update(request, pk):
    title = request.POST.get("title")
    content = request.POST.get("content")    

    article = Article.objects.get(pk=pk)
    article.title =title
    article.content = content
    article.save()

    return redirect("article_detail", article.pk)

def delete(request, pk):
    if request.method == "POST":
        article = Article.objects.get(pk=pk)
        article.delete()
        return redirect("articles")


def data_catch(request):
    data = request.GET.get("message")
    context = {
        'data': data,
    }
    return render(request, 'data_catch.html', context)




