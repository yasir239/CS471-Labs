from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Avg, Max, Min, Sum, Count
from apps.bookmodule.forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages


from .models import *

# Create your views here.

def index(request):

    return render(request, "bookmodule/index.html")





def list_books(request):

    return render(request, 'bookmodule/list_books.html')



def viewbook(request):

    return render(request, 'bookmodule/one_book.html')



def aboutus(request):

    return render(request, 'bookmodule/aboutus.html')


def link(request):
    return render(request, 'bookmodule/links.html')


def format(request):
    return render(request, 'bookmodule/fomat.html')

def listing(request):
    return render(request, 'bookmodule/lists.html')



def tables(request):
    return render(request, 'bookmodule/tables.html')
    
    
def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]
    
def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        # now filter
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): 
                contained = True
            if not contained and isAuthor and string in item['author'].lower():
                contained = True
            if contained: 
                newBooks.append(item)
        return render(request, "bookmodule/bookList.html",{'books':newBooks})
    return render(request, "layouts/base.html")


def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='Continuous')
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})


def lookup_query(request):
    mybooks=books=Book.objects.filter(author__isnull =False).filter(title__icontains='a').filter(edition__gte = 0).exclude(price__lte = 0.0)[:10]
    if len(mybooks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')
    
    
def task1(request):
    books = Book.objects.filter(Q(price__lte=50))
    
    return render(request,'bookmodule/task1.html',{'books':books})
    
def task2(request):
    books = Book.objects.filter(Q(edition__gt=2) &(Q(title__icontains='qu') | Q(author__icontains='qu')))

    return render(request,'bookmodule/task2.html',{'books':books})


def task3(request):
    books = Book.objects.filter(~Q(edition__gt=2) &(~Q(title__icontains='qu') | ~Q(author__icontains='qu')))

    return render(request,'bookmodule/task2.html',{'books':books})


def task4(request):
    books = Book.objects.all().order_by('title')

    return render(request,'bookmodule/task2.html',{'books':books})


def task5(request):
    books = Book.objects.aggregate(
        total_books= Count('id'),
        total_price= Sum('price'),
        avg_price= Avg('price'),
        max_price= Max('price'),
        min_price= Min('price')
    )

    return render(request,'bookmodule/task5.html',{'books':books})


def task6(request):
    city_counts = Student.objects.values('adress__city').annotate(num_students=Count('id')).order_by('adress__city')
    return render(request,'bookmodule/task6.html',{'city_counts':city_counts})



def listbooks(request):
    books =Book.objects.all()
    return render(request,'bookmodule/listbooks.html',{'books':books})
    
    
def addbook(request):
    if request.method=='POST':
        title=request.POST.get('title')
        author=request.POST.get('author')
        price=request.POST.get('price')
        edition=request.POST.get('edition')
        newBook=Book.objects.create(title=title,author=author,price=price,edition=edition)
        newBook.save()
        return redirect('books.listbooks')
        
    return render(request,'bookmodule/addbook.html')

def addBookByForm(request):
    form = BookForm()
    if request.method=='POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.listbooks')
    return render(request,'bookmodule/addBookByForm.html',{'form':form})


           
    


def editbook(request,bID):
    book = Book.objects.get(id=bID)
    if request.method=='POST':
        title=request.POST.get('title')
        author=request.POST.get('author')
        price=request.POST.get('price')
        edition=request.POST.get('edition')
        book.title=title
        book.author=author
        book.price=price
        book.edition=edition
        book.save()
        return redirect('books.listbooks')
    return render(request,'bookmodule/editbook.html',{'book':book})


def editBookByForm(request,bID):
    book = Book.objects.get(id=bID)
    if request.method=='POST':
        form = BookForm(request.POST,instance=book)
        if form.is_valid:
            form.save()
        return redirect('books.listbooks')
    form = BookForm(instance=book)
    return render(request,'bookmodule/addBookByForm.html',{'form':form})


def deleteBook(request,bID):
    book = Book.objects.get(id=bID)
    book.delete()
    return redirect('books.listbooks')
        



def listStudent(request):
    students =Student.objects.all()
    return render(request,'bookmodule/listStudent.html',{'students':students})      
        
def addStudent(request):
    form=StudentForm()
    if request.method=='POST':
        form=StudentForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('students.listStudent')
    return render(request,'bookmodule/addStudent.html',{'form':form})
        
        

def editStudent(request,bID):
    student = Student.objects.get(id=bID)
    if request.method=='POST':
        form = StudentForm(request.POST,instance=student)
        if form.is_valid:
            form.save()
            return redirect('students.listStudent')
    form = StudentForm(instance=student)
    return render(request,'bookmodule/addStudent.html',{'form':form})
    
            
def deleteStudent(request,bID):
    student = Student.objects.get(id=bID)
    student.delete()
    return redirect('students.listStudent')
    



def listStudent2(request):
    if request.user.is_authenticated:
        students =Student2.objects.all()
        return render(request,'bookmodule/listStudentM.html',{'students':students})
    else:
        return redirect(register)      
        
def addStudent2(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=StudentForm2(request.POST)
            if form.is_valid():
                form.save()
                return redirect('students.listStudent2')
        else:
            form=StudentForm2()
            return render(request,'bookmodule/addStudent.html',{'form':form})
    else:
        return redirect(register)      
        
        

def editStudent2(request,bID):
    if request.user.is_authenticated:
        student = Student2.objects.get(id=bID)
        if request.method=='POST':
            form = StudentForm2(request.POST,instance=student)
            if form.is_valid():
                form.save()
                return redirect('students.listStudent2')
        form = StudentForm2(instance=student)
        return render(request,'bookmodule/addStudent.html',{'form':form})
    else:
        return redirect(register)      
        
            
def deleteStudent2(request,bID):
    if request.user.is_authenticated:
        student = Student2.objects.get(id=bID)
        student.delete()
        return redirect('students.listStudent2')
    else:
        return redirect(register)      
    
    
    
def addBookWithCover(request):
    if request.method=='POST':
        form = BookCoverForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            books =BookCover.objects.all()
            return render(request,'bookmodule/listBooksCovers.html',{'books':books})
        else:
            print(form.errors)
        
    form = BookCoverForm(None)
    return render(request,'bookmodule/addbookcover.html',{'form':form})
    



def homepage(request):
    return redirect(listStudent2)





def register(request):
    form =SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            
            login(request, user)
            messages.success(request, "You Have Successfully Registered!")
            return redirect(homepage)
        else:
            messages.error(request, form.error_messages)
    return render(request,'bookmodule/register.html',{'form':form})
    
    
    
def logoutuser(request):
    logout(request)
    messages.success(request,"You have been logged out")
    return redirect(register)


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect(homepage)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'bookmodule/login.html')


def lab12task1(request):
    return render(request,'bookmodule/lab12task1.html')



def lab12task2(request):
    return render(request,'bookmodule/lab12task2.html')



def lab12task3(request):
    return render(request,'bookmodule/lab12task3.html')



def lab12task4(request):
    return render(request,'bookmodule/lab12task4.html')


    