from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class WorkplaceEvaluation(models.Model):
    """
    Performance evaluation submitted by a workplace supervisor for a student.
    Scored per criteria, max 10 per criterion.
    """

    placement    = models.ForeignKey(
                       'placements.Placement',
                       on_delete=models.CASCADE,
                       related_name='workplace_evaluations',
                   )
    supervisor   = models.ForeignKey(
                       settings.AUTH_USER_MODEL,
                       on_delete=models.CASCADE,
                       related_name='given_workplace_evaluations',
                       limit_choices_to={'role': 'workplace_supervisor'},
                   )

    # Evaluaticriteria (each 0-10)
    professionalism   = models.DecimalField(
                            max_digits=4, decimal_places=1,
                            validators=[MinValueValidator(0), MaxValueValidator(10)]
                        )
    technical_skills  = models.DecimalField(
                            max_digits=4, decimal_places=1,
                            validators=[MinValueValidator(0), MaxValueValidator(10)]
                        )
    communication     = models.DecimalField(
                            max_digits=4, decimal_places=1,
                            validators=[MinValueValidator(0), MaxValueValidator(10)]
                        )
    punctuality       = models.DecimalField(
                            max_digits=4, decimal_places=1,
                            validators=[MinValueValidator(0), MaxValueValidator(10)]
                        )

    overall_comment   = models.TextField(blank=True)
    submitted_at      = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        # One evaluation per placement per supervisor
        unique_together = ('placement', 'supervisor')
        ordering        = ['-submitted_at']

    @property
    def total_score(self):
        return (
            self.professionalism +
            self.technical_skills +
            self.communication +
            self.punctuality
        )

    @property
    def average_score(self):
        return self.total_score / 4

    def __str__(self):
        return f'Workplace eval — {self.placement.student.full_name}'


class AcademicEvaluation(models.Model):
    """
    Academic evaluation submitted by an academic supervisor for a student.
    """

    placement    = models.ForeignKey(
                       'placements.Placement',
                       on_delete=models.CASCADE,
                       related_name='academic_evaluations',
                   )
    supervisor   = models.ForeignKey(
                       settings.AUTH_USER_MODEL,
                       on_delete=models.CASCADE,
                       related_name='given_academic_evaluations',
                       limit_choices_to={'role': 'academic_supervisor'},
                   )

    # Evaluation criteria (each 0-10)
    quality_of_work   = models.DecimalField(
                            max_digits=4, decimal_places=1,
                            validators=[MinValueValidator(0), MaxValueValidator(10)]
                        )
    internship_report = models.DecimalField(
                            max_digits=4, decimal_places=1,
                            validators=[MinValueValidator(0), MaxValueValidator(10)]
                        )
    problem_solving   = models.DecimalField(
                            max_digits=4, decimal_places=1,
                            validators=[MinValueValidator(0), MaxValueValidator(10)]
                        )
    learning_outcomes = models.DecimalField(
                            max_digits=4, decimal_places=1,
                            validators=[MinValueValidator(0), MaxValueValidator(10)]
                        )

    overall_comment   = models.TextField(blank=True)
    submitted_at      = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('placement', 'supervisor')
        ordering        = ['-submitted_at']

    @property
    def total_score(self):
        return (
            self.quality_of_work +
            self.internship_report +
            self.problem_solving +
            self.learning_outcomes
        )

    @property
    def average_score(self):
        return self.total_score / 4

    def __str__(self):
        return f'Academic eval — {self.placement.student.full_name}'