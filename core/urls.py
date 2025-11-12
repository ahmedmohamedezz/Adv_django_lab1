
from . import views
from django.urls import path

urlpatterns = [
    path("test_n_plus_1/", views.test_n_plus_1),
    path("test_qf/", views.test_qf),
    path("test_only_defer/", views.test_only_defer),
    path("test_values_values_list/", views.test_values_values_list),
    path("test_db_index_with_c_profile/", views.test_db_index_with_c_profile),
    path("test_connection_age/", views.test_connection_age),
]

# https://docs.google.com/document/d/1L8b8-z_6QcgjlnhYdItE8M9Shz0qh0EX/edit