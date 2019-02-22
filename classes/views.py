from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Classroom,Student
from .forms import ClassroomForm, StudentForm, SignupForm, SigninForm

def noaccess(request):
    return render(request, 'no-access.html')

def classroom_list(request):
	classroom = Classroom.objects.all()
	context = {
		"classrooms": classroom,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	students = classroom.students.all().order_by('name', '-exam_grade')
	context = {
		"classroom": classroom,
		"students":students,
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	if request.user.is_anonymous:
		return redirect('signin')
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			classroom = form.save(commit=False)
			classroom.teacher = request.user
			classroom.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user == Classroom.teacher):
		return redirect('no-access')
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user == classroom.teacher):
		messages.success(request, "Access Denied")
		return redirect('classroom-list')
	classroom.delete() 
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user_obj = form.save(commit=False)

            user_obj.set_password(user_obj.password)
            user_obj.save()

            login(request, user_obj)
            return redirect("classroom-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)


def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            my_username = form.cleaned_data['username']
            my_password = form.cleaned_data['password']
            user_obj = authenticate(username=my_username, password=my_password)
            if user_obj is not None:
                login(request, user_obj)
                return redirect('classroom-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")

def add_student(request, class_id):
	classroom = Classroom.objects.get(id=class_id)
	if not (request.user == classroom.teacher):
		messages.success(request, "Access Denied")
		return redirect('classroom-list')
	form = StudentForm()
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			student = form.save(commit=False)
			student.classroom = classroom
			student.save()
			messages.success(request, "Successfully Added a Student!")
			return redirect('classroom-detail', classroom_id=class_id)
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'add_student.html', context)

def student_update(request, student_id):
	student = Student.objects.get(id=student_id)
	if not (request.user == student.classroom.teacher):
		messages.success(request, "Access Denied")
		return redirect('classroom-list')
	form = StudentForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, instance = student)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Updated a Student!")
			return redirect('student_update.html', classroom_id=student.classroom_id)
			context = {
				"form":form,
				"classroom": Classroom,
				"student":student,

				 }
	return render(request, 'create.html', context)

def student_delete(request, student_id):
	student = Student.objects.get(id=student_id)
	if not (request.user == student.classroom.teacher):
		messages.success(request, "Access Denied")
		return redirect('classroom-list')
	class_id = student.classroom_id
	student.delete
	messages.success(request, "Successfully deleted  a Student!" )
	return redirect('classroom-detail', classroom_id=class_id)
    