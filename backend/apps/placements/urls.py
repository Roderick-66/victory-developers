from django.urls import path
from .views import (
    PlacementListCreateView,
    PlacementDetailView,
    MyPlacementView,
    WorkplacePlacementsView,
    AcademicPlacementsView,
)

urlpatterns = [
    # Admin
    path('',                        PlacementListCreateView.as_view(), name='placement-list-create'),
    path('<int:pk>/',               PlacementDetailView.as_view(),     name='placement-detail'),

    # Student
    path('my/',                     MyPlacementView.as_view(),         name='my-placement'),

    # Workplace supervisor
    path('my-students/',            WorkplacePlacementsView.as_view(), name='workplace-placements'),

    # Academic supervisor
    path('my-academic-students/',   AcademicPlacementsView.as_view(),  name='academic-placements'),
]