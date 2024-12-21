from django.shortcuts import redirect, render
from .models import Article
from .forms import ArticleForm

# Create your views here.
def index(request):
    return render(request, 'articles/index.html')
        # 탬플릿을 랜더해서 리턴할수있다

def articles(request):
    articles = Article.objects.all().order_by("-created_at")
    context = {
        "articles": articles,
    }
    return render(request, 'articles/articles.html', context)

def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {"article": article}
    return render(request, "articles/article_detail.html", context)



def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            # 데이터를 지정하고
            article = form.save()
            # 다른곳으로 리다이렉트
            return redirect("aritles:article_detail", article.pk)
    else: 
        form = ArticleForm()

    context = {"form": form}
    return render(request, "articles/create.html", context)



def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect("articles:article_detail", article.pk)

    else:
        form = ArticleForm(instance=article)
    
    context = {
        "form": form,
        "article": article,
    }
    return render(request, "articles/update.html", context)



def delete(request, pk):
    if request.method == "POST":
        article = Article.objects.get(pk=pk)
        article.delete()
        return redirect("articles:articles")
    return redirect("articles:article_detail", pk)

def data_throw(request):
    return render(request, 'articles/data_throw.html')


def data_catch(request):
    data = request.GET.get("articles/message")
    context = {
        'data': data,
    }
    return render(request, 'articles/data_catch.html', context)



