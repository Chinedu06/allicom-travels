# from django.urls import path
# from . import views

# urlpatterns = [
#     # Public (tourist)
#     path("", views.ServiceListView.as_view(), name="service-list"),
#     path("<int:pk>/", views.ServiceDetailView.as_view(), name="service-detail"),

#     # Operator-only (service management)
#     path("my-services/", views.OperatorServiceListView.as_view(), name="operator-services"),
#     path("create/", views.ServiceCreateView.as_view(), name="service-create"),
#     path("<int:pk>/update/", views.ServiceUpdateView.as_view(), name="service-update"),
#     path("<int:pk>/delete/", views.ServiceDeleteView.as_view(), name="service-delete"),

#     # Packages endpoints
#     path("<int:service_id>/packages/", views.PackageListView.as_view(), name="package-list-for-service"),
#     path("<int:service_id>/packages/create/", views.PackageCreateView.as_view(), name="package-create-for-service"),
#     path("packages/<int:pk>/", views.PackageDetailView.as_view(), name="package-detail"),
#     path("packages/<int:pk>/update/", views.PackageUpdateView.as_view(), name="package-update"),
#     path("packages/<int:pk>/delete/", views.PackageDeleteView.as_view(), name="package-delete"),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     # Public (tourists)
#     # GET  /api/services/                -> list
#     # GET  /api/services/<pk>/           -> detail
#     path("", views.ServiceListView.as_view(), name="service-list"),
#     path("<int:pk>/", views.ServiceDetailView.as_view(), name="service-detail"),

#     # Operator-only (namespaced under operator/)
#     # POST /api/services/operator/create/
#     path("operator/my-services/", views.OperatorServiceListView.as_view(), name="operator-services"),
#     path("operator/create/", views.ServiceCreateView.as_view(), name="operator-service-create"),
#     path("operator/<int:pk>/update/", views.ServiceUpdateView.as_view(), name="operator-service-update"),
#     path("operator/<int:pk>/delete/", views.ServiceDeleteView.as_view(), name="operator-service-delete"),

#     # Packages endpoints (nested under service)
#     path("<int:service_id>/packages/", views.PackageListView.as_view(), name="package-list-for-service"),
#     path("<int:service_id>/packages/create/", views.PackageCreateView.as_view(), name="package-create-for-service"),

#     # packages can also be managed by id
#     path("packages/<int:pk>/", views.PackageDetailView.as_view(), name="package-detail"),
#     path("packages/<int:pk>/update/", views.PackageUpdateView.as_view(), name="package-update"),
#     path("packages/<int:pk>/delete/", views.PackageDeleteView.as_view(), name="package-delete"),
# ]

from django.urls import path
from . import views

urlpatterns = [
    # ============================
    # 🔹 Public Endpoints (Tourists)
    # ============================
    # GET  /api/services/              -> list all services
    # GET  /api/services/<pk>/         -> service details
    path("", views.ServiceListView.as_view(), name="service-list"),
    path("<int:pk>/", views.ServiceDetailView.as_view(), name="service-detail"),

    # ============================
    # 🔹 Operator Endpoints
    # ============================
    # GET  /api/services/operator/my-services/
    # POST /api/services/operator/create/
    # PUT  /api/services/operator/<id>/update/
    # DELETE /api/services/operator/<id>/delete/
    path("operator/my-services/", views.OperatorServiceListView.as_view(), name="operator-services"),
    path("operator/create/", views.ServiceCreateView.as_view(), name="operator-service-create"),
    path("operator/<int:pk>/update/", views.ServiceUpdateView.as_view(), name="operator-service-update"),
    path("operator/<int:pk>/delete/", views.ServiceDeleteView.as_view(), name="operator-service-delete"),

    # ============================
    # 🔹 Package Endpoints
    # ============================
    # GET  /api/services/<service_id>/packages/
    # POST /api/services/<service_id>/packages/create/
    # GET  /api/services/packages/<id>/
    # PUT  /api/services/packages/<id>/update/
    # DELETE /api/services/packages/<id>/delete/
    path("<int:service_id>/packages/", views.PackageListView.as_view(), name="package-list-for-service"),
    path("<int:service_id>/packages/create/", views.PackageCreateView.as_view(), name="package-create-for-service"),
    path("packages/<int:pk>/", views.PackageDetailView.as_view(), name="package-detail"),
    path("packages/<int:pk>/update/", views.PackageUpdateView.as_view(), name="package-update"),
    path("packages/<int:pk>/delete/", views.PackageDeleteView.as_view(), name="package-delete"),
]
