# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name='user_index'),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     # basic index or health check
#     path('', views.index, name='user_index'),

#     # Authentication (generic)
#     # POST /api/users/auth/register/  -> tourist registration
#     # POST /api/users/auth/login/     -> login
#     path('auth/register/', views.RegisterView.as_view(), name='register'),
#     path('auth/login/', views.LoginView.as_view(), name='login'),

#     # Operator-specific (alias endpoints; same underlying logic but set role=operator)
#     # POST /api/users/operators/signup/
#     # POST /api/users/operators/login/
#     path('operators/signup/', views.OperatorRegisterView.as_view(), name='operator-register'),
#     path('operators/login/', views.OperatorLoginView.as_view(), name='operator-login'),

#     # Admin-only user management endpoints (optional; implement in views/admin router)
#     # path('admin/approvals/', views.OperatorApprovalListView.as_view(), name='operator-approval-list'),
# ]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name='user_index'),

#     # Operator-only authentication endpoints
#     # POST /api/users/operators/signup/
#     # POST /api/users/operators/login/
#     path('operators/signup/', views.OperatorRegisterView.as_view(), name='operator-register'),
#     path('operators/login/', views.OperatorLoginView.as_view(), name='operator-login'),
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "users"


router = DefaultRouter()
# registers endpoints under /operators/profile/
router.register(r'operators/profile', views.SupplierProfileViewSet, basename='operator-profile')

urlpatterns = [
    path('', views.index, name='user_index'),

    # Operator-only authentication endpoints
    path('operators/signup/', views.OperatorRegisterView.as_view(), name='operator-register'),
    path('operators/login/', views.OperatorLoginView.as_view(), name='operator-login'),

    # include viewset router urls at this path
    path('', include(router.urls)),
]
