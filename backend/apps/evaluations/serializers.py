from rest_framework import serializers
from .models import WorkplaceEvaluation, AcademicEvaluation


class WorkplaceEvaluationSerializer(serializers.ModelSerializer):
    supervisor_name  = serializers.CharField(source='supervisor.full_name', read_only=True)
    student_name     = serializers.CharField(source='placement.student.full_name', read_only=True)
    total_score      = serializers.DecimalField(max_digits=5, decimal_places=1, read_only=True)
    average_score    = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)

    class Meta:
        model  = WorkplaceEvaluation
        fields = [
            'id', 'placement', 'supervisor', 'supervisor_name', 'student_name',
            'professionalism', 'technical_skills', 'communication', 'punctuality',
            'overall_comment', 'total_score', 'average_score',
            'submitted_at', 'updated_at',
        ]
        read_only_fields = ['id', 'supervisor', 'supervisor_name', 'student_name',
                            'total_score', 'average_score', 'submitted_at', 'updated_at']


class WorkplaceEvaluationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = WorkplaceEvaluation
        fields = [
            'placement',
            'professionalism', 'technical_skills', 'communication', 'punctuality',
            'overall_comment',
        ]

    def validate_placement(self, placement):
        """Supervisor must be assigned to this placement."""
        request = self.context['request']
        if placement.workplace_supervisor != request.user:
            raise serializers.ValidationError(
                'You are not the workplace supervisor for this placement.'
            )
        return placement


class AcademicEvaluationSerializer(serializers.ModelSerializer):
    supervisor_name  = serializers.CharField(source='supervisor.full_name', read_only=True)
    student_name     = serializers.CharField(source='placement.student.full_name', read_only=True)
    total_score      = serializers.DecimalField(max_digits=5, decimal_places=1, read_only=True)
    average_score    = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)

    class Meta:
        model  = AcademicEvaluation
        fields = [
            'id', 'placement', 'supervisor', 'supervisor_name', 'student_name',
            'quality_of_work', 'internship_report', 'problem_solving', 'learning_outcomes',
            'overall_comment', 'total_score', 'average_score',
            'submitted_at', 'updated_at',
        ]
        read_only_fields = ['id', 'supervisor', 'supervisor_name', 'student_name',
                            'total_score', 'average_score', 'submitted_at', 'updated_at']


class AcademicEvaluationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AcademicEvaluation
        fields = [
            'placement',
            'quality_of_work', 'internship_report', 'problem_solving', 'learning_outcomes',
            'overall_comment',
        ]

    def validate_placement(self, placement):
        """Supervisor must be assigned to this placement."""
        request = self.context['request']
        if placement.academic_supervisor != request.user:
            raise serializers.ValidationError(
                'You are not the academic supervisor for this placement.'
            )
        return placement


class ScoresOverviewSerializer(serializers.Serializer):
    """
    Read-only combined scores for a placement — used by academic supervisor and admin.
    """
    student_name         = serializers.CharField()
    student_number       = serializers.CharField()
    company_name         = serializers.CharField()
    placement_status     = serializers.CharField()
    workplace_avg        = serializers.DecimalField(max_digits=4, decimal_places=2, allow_null=True)
    academic_avg         = serializers.DecimalField(max_digits=4, decimal_places=2, allow_null=True)
    combined_avg         = serializers.DecimalField(max_digits=4, decimal_places=2, allow_null=True)
    workplace_evaluation = WorkplaceEvaluationSerializer(allow_null=True)
    academic_evaluation  = AcademicEvaluationSerializer(allow_null=True)