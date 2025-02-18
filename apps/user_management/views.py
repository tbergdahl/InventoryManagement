from django.http import HttpResponse
from .models import CustomUser
def index(request):
    # Query all users
    all_users = CustomUser.objects.all()

    # Create a string to hold the user details
    user_details = "User Login Page<br><br>All Users:<br>"

    # Iterate through the users and add their details to the string
    for user in all_users:
        user_details += f"Username: {user.username}, Email: {user.email}, First Name: {user.first_name}, Last Name: {user.last_name}, UserType: {user.usertype}<br>"

    # Return the user details as an HTTP response
    return HttpResponse(user_details)