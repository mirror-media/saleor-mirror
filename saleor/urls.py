from django.contrib import admin
from django.urls import path, include
# from apps.graphql.view import GraphQLView # GraphQL Playground
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from saleor.schema import schema

from saleor.settings import PLAYGROUND_ENABLED

if PLAYGROUND_ENABLED:
    from apps.graphql.view import GraphQLView # GraphQL Playground
else:
    from graphene_django.views import GraphQLView  # GraphiOL

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema))) if PLAYGROUND_ENABLED else path("graphql/", csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True))),
]

admin.site.site_header = "Saleor Dashboard"
admin.site.site_title = "Mirrormedia CRM"
admin.site.index_title = "Saleor Dashboard"
admin.site.site_url = "https://www.mirrormedia.mg/"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
