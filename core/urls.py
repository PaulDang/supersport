"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from cart.views import cart_view

urlpatterns = [
    path("", RedirectView.as_view(url="/main/")),
    path("", include("user.urls")),
    path("", include("dashboard.urls")),
    path("", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("main/", include("product.urls")),
    path("cart/", include("cart.urls")),
    path("<str:username>/cart/", cart_view, name="user_cart"),
    path("", include("order.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
