from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("query/", views.query, name="query"),
    path("documents/", views.documents, name="documents"),
    path('document/<int:id>/', views.serve_document, name='serve_document'),
]
