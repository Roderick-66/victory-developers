from django.urls import path
from .views import (
    WorkplaceEvaluationListCreateView,
    WorkplaceEvaluationDetailView,
    AcademicEvaluationListCreateView,
    AcademicEvaluationDetailView,
    StudentScoresView,
    AdminScoresOverviewView,
    AcademicScoresOverviewView,
)

urlpatterns = [
    # Student
    path('my-scores/',            StudentScoresView.as_view(),                  name='student-scores'),

    # Workplace supervisor
    path('workplace/',            WorkplaceEvaluationListCreateView.as_view(),  name='workplace-eval-list-create'),
    path('workplace/<int:pk>/',   WorkplaceEvaluationDetailView.as_view(),      name='workplace-eval-detail'),

    # Academic supervisor
    path('academic/',             AcademicEvaluationListCreateView.as_view(),   name='academic-eval-list-create'),
    path('academic/<int:pk>/',    AcademicEvaluationDetailView.as_view(),       name='academic-eval-detail'),
    path('academic/scores/',      AcademicScoresOverviewView.as_view(),         name='academic-scores-overview'),

    # Admin
    path('admin/scores/',         AdminScoresOverviewView.as_view(),            name='admin-scores-overview'),
]