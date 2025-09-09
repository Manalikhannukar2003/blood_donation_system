from django.shortcuts import render,redirect,get_object_or_404
from .models import Donor, Request
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required


#donor list
def donor_list(request):
    donors = Donor.objects.all()
    return render(request, "donor_list.html", {"donors": donors})

#request list
def request_list(request):
    requests = Request.objects.all()
    return render(request, "request_list.html", {"requests": requests})
    
#about us
def about_us(request):
    return render(request,"about_us.html")

#home page
def home(request):
    if request.user.is_authenticated:
        # User is logged in
        print("Logged in as:", request.user.username)
    else:
        # User is not logged in
        print("User is not logged in")

    return render(request, 'home.html')



#register
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect("register")

    return render(request, "register.html")


#login page
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate using username (if using email as username, adjust below)
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  # log the user in
            return redirect('home')     # redirect to homepage URL name
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    
    return render(request, 'login.html')


    
#requestor
@login_required(login_url='register')   # redirect to login page if not logged in
def requestor(request):
    message = ""

    if request.method == "POST":
        patient_name = request.POST.get("patient_name")
        blood_group = request.POST.get("blood_group")
        hospital_name = request.POST.get("hospital_name")
        contact = request.POST.get("contact")
        email = request.POST.get("email")

        # Check donor availability
        donors = Donor.objects.filter(blood_group=blood_group)
        if donors.exists():
            status = "Approved"
        else:
            status = "Rejected"

        # Save request
        Request.objects.create(
            patient_name=patient_name,
            blood_group=blood_group,
            hospital_name=hospital_name,
            contact=contact,
            email=email,
            status=status,
        )

        message = "Your request has been saved successfully!"

    return render(request, "requestor.html", {
        'message': message,
        'user_authenticated': request.user.is_authenticated
    })


  #my requests  
@login_required(login_url='login')
def my_requests(request):
    # get the latest request of the logged-in user
    req = Request.objects.filter(email=request.user.email).last()

    donors = []
    if req and req.status == "Approved":
        donors = Donor.objects.filter(blood_group=req.blood_group)

    context = {
        "requestor": req,
        "donors": donors,
    }
    return render(request, "my_requests.html", context)


 #donor detail
def donor_detail(request, name):
    # Get donor by name
     donor = get_object_or_404(Donor, name=name)

     return render(request, "donor_detail.html", {"donor": donor})


#become donor
@login_required(login_url='register')  # redirect to login page if not logged in
def become_donor(request):
    message = ""

    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        blood_group = request.POST.get('blood_group')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        last_donation = request.POST.get('last_donation')

        Donor.objects.create(
            name=name,
            age=age,
            blood_group=blood_group,
            contact=contact,
            email=email,
            last_donation=last_donation
        )
        message = "Your donor details have been saved successfully!"

    
    return render(request, 'become_donor.html', {
        'message': message,
        'user_authenticated': request.user.is_authenticated
    })


#logout
def logout_view(request):
    logout(request)            #This clears the session and logs out the user
    return redirect('home')  # redirect back to home page


# from django.shortcuts import render
# from .ml_model import train_model, predict_donors

# def donor_ai_view(request):
#     requested_bg = request.GET.get("blood_group", "A+")  # default A+

#     model = train_model(requested_bg)
#     predictions = predict_donors(model, requested_bg) if model else []

#     return render(request, "donor_ai.html", {
#         "predictions": predictions,
#         "requested_bg": requested_bg
#     })


# from django.shortcuts import render
# from .ml.blood_group_prediction import predict_next_donor  # ML function

# def dashboard(request):
#     df = predict_next_donor()  # Run ML code
#     data = df.to_dict(orient='records') if not df.empty else []
#     return render(request, "dashboard.html", {"data": data})

# from django.shortcuts import render
# from .models import Donor
# from .ml.blood_group_prediction import predict_next_donor  # ML function

# def dashboard(request):
#     # Count donors by blood group
#     blood_counts = {}
#     for donor in Donor.objects.all():
#         group = donor.blood_group
#         blood_counts[group] = blood_counts.get(group, 0) + 1

#     # Run ML prediction (returns a dictionary)
#     predictions = predict_next_donor(blood_counts)

#     # Convert into list of dicts for easy template looping
#     data = []
#     for group, pred in predictions.items():
#         data.append({
#             "group": group,
#             "predicted": pred
#         })

#     return render(request, "dashboard.html", {"data": data})


from django.shortcuts import render
from .ml.blood_group_prediction import predict_next_donor

def dashboard(request):
    df = predict_next_donor()  # returns DataFrame with blood_group & probability
    data = df.to_dict(orient="records") if not df.empty else []

    # Prepare separate lists for JS
    blood_groups = [row['blood_group'] for row in data]
    probabilities = [row['probability'] for row in data]

    return render(request, "dashboard.html", {
        "blood_groups": blood_groups,
        "probabilities": probabilities
    })




