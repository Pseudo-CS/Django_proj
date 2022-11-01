from django.shortcuts import redirect, render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site  
#from .token import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes, force_str 


# Create your views here.
# Django views are Python functions that takes http requests and returns http response


def all_emp(request):
    emps = Employee.objects.all()
    paginator = Paginator(emps,5)
    page = request.GET.get('page')
    empsFinal = paginator.get_page(page)
    context = {                     # data in html requests always move in either XML/json
        'emps': empsFinal,
        'pag' : paginator
    }
    return render(request, 'index.html', context) # renders html page along with the json data

def emai(user, hash, current_site):
    email = user.email
    subject, from_email, to = 'welcome', 'sazkikai@gmail.com', email
    htmly = get_template('email.html')

    html_content = htmly.render({'domain': current_site.domain,'code': hash, 'uid':urlsafe_base64_encode(force_bytes(str(user.id)))})
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return
    # messages.success(request, f'Your account has been created ! You are now able to log in')

def add_emp(request):   # we are using the same function to render the html page and to handle the post request
    if request.method == 'POST':
        first_name = request.POST['first_name'] # to access the data in the POST  request
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        email = request.POST['email']

        phone = int(request.POST['phone'])
        dept = Department.objects.get(name=request.POST['dept'])
        role = Role.objects.get(name=request.POST['role'])
        new_emp = Employee(first_name= first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, email=email, dept = dept, role = role, hire_date = datetime.now())
        current_site = get_current_site(request)
        hash = 'boomer' #account_activation_token.make_token(new_emp)
        emai(user=new_emp, hash=hash, current_site=current_site)
        print('------------------')
        print(new_emp.id)
        new_emp.save()  # to save entry to sql db 
        return redirect('/')

    elif request.method=='GET':
        context = {
            'departments' : Department.objects.all(),
            'roles' : Role.objects.all()
        }
        return render(request, 'add_emp.html', context)
    else:
        return HttpResponse("An Exception Occured! Employee Has Not Been Added")
    
        
def activate(request, uidb64, token):
    print(urlsafe_base64_decode(uidb64))  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = Employee.objects.get(pk=uid)
        print('the user is valid?:'+user)  
    except Exception as e: print(e)

    if user is not None: #and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  


def remove_emp(request):
    print('removing employee')    
    emp_to_be_removed = Employee.objects.get(id=request.GET.get('id',''))
    emp_to_be_removed.delete()

    return redirect('/')


def filter_emp(request):
    if request.method == 'GET':
        name = request.GET.get('srch', '')
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))

        context = {
            'emps': emps
        }
        return render(request, 'index.html', context)

    else:
        return HttpResponse('An Exception Occurred')

def update_emp(request):
    if request.method == 'POST':
        post = request.POST
        emp_id = post['emp_id']
        emp = Employee.objects.get(id=emp_id)
        
        if post['first_name']:
            emp.first_name = post['first_name'] # to access the data in the POST  request
        if post['last_name']:
            emp.last_name = post['last_name']
        if post['salary']:
            emp.salary = int(post['salary'])
        if post['bonus']:
            emp.bonus = int(post['bonus'])
        if post['phone']:
            emp.phone = int(post['phone'])
        if post['dept']:
            emp.dept = Department.objects.get(name=post['dept']) 
        if post['role']:
            emp.role = Role.objects.get(name=post['role'])
        emp.save()

        return redirect('/')

    elif request.method == 'GET':
        emp = Employee.objects.get(id=request.GET.get('id',''))
        context = {
            'emp_id' : emp.id,
            'first_name' : emp.first_name,
            'last_name' : emp.last_name,
            'salary' : emp.salary, 
            'dept' : emp.dept,
            'role' : emp.role,
            'bonus' : emp.bonus, 
            'phone' : emp.phone,
            'departments' : Department.objects.all(),
            'roles' : Role.objects.all()
        }
        return render(request, 'update_emp.html', context)
    else:
        return HttpResponse('An Exception Occurred')


def spotify(request):
    return render(request, 'spotify.html')