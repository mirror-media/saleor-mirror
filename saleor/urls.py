from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, include
# from graphene_django.views import GraphQLView # GraphiOL
# from apps.graphql.view import GraphQLView # GraphQL Playground
from apps.common.views import HomeView, SignUpView, DashboardView, ProfileUpdateView, ProfileView

from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from saleor.schema import schema
from django.contrib.auth.decorators import login_required

from saleor.settings import PLAYGROUND_ENABLED

if PLAYGROUND_ENABLED:
    from apps.graphql.view import GraphQLView # GraphQL Playground
else:
    from graphene_django.views import GraphQLView  # GraphiOL

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # path('', HomeView.as_view(), name='home'),
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),
    #
    # path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    # path('profile/', ProfileView.as_view(), name='profile'),

    # Authentication 
    # path('register/', SignUpView.as_view(), name="register"),

    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema))) if PLAYGROUND_ENABLED else path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True))),

    # path('login/', auth_views.LoginView.as_view(
    #     template_name='common/login.html'
    #     ),
    #     name='login'
    # ),

]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
