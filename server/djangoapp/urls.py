from django.urls import path
from .views import index, get_dealerships, about, contact, login_request, logout_request, registration_request, signup

from django.conf.urls.static import static
from django.conf import settings

app_name = 'djangoapp'
urlpatterns = [
    # Path for about view
    path('about/', about, name='about'),

    # Path for contact us view
    path('contact/', contact, name='contact'),

    # Path for registration
path('registration/', registration_request, name='registration'),

    # Path for login
path('login/', login_request, name='login'),


    # Path for logout
    path('logout/', logout_request, name='logout'),

    # Path for signup
    path('signup/', signup, name='signup'),


    # Path for the index view (get_dealerships)
    path('', get_dealerships, name='index'),

    # Path for dealer reviews view

    # Path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
