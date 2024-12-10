from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')
        # 탬플릿을 랜더해서 리턴할수있다
def users(request):
    return render(request, 'users.html')
    
def hello(request):

    tags = ['python', 'django', 'html', 'css']
    books = ["해변의 카프카", "노르웨이의 숲", "대화의 기술", "나미야 잡화점의 기적"]
    context = {
        'name': 'name',
        'tags': tags,
        'books': books,
    } 

def data_throw(request):
    return render(request, 'data-throw.html')

