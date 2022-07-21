import subscriptions
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from customer.views import *


urlpatterns = [
    path("", home, name="home"),
    path('admin/', admin.site.urls),
    path('testcookies/', cookie_session),
    path('deletecookies/', delete_cookie),
    path('estate/', include('House.urls')),
    path('customer/', include('customer.urls')),
    path('payment/', include('payment.urls')),
    path('basket/', include('basket.urls')),
    path('subscriptions/', include('subscriptions.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler500 = 'customer.views.error_500'
handler404 = 'customer.views.error_404'