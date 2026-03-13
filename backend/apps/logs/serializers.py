from rest_framework import serializers
from django.utils import timezone
from .models import WeeklyLog, LogComment


class LogCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    author_role = serializers.CharField(source='author.role',      read_only=True)

    class Meta:
        model  = LogComment
        fields = ['id', 'author', 'author_name', 'author_role', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'author_name', 'author_role', 'created_at', 'updated_at']


class WeeklyLogSerializer(serializers.ModelSerializer):
    """Read serializer — full detail including comments."""

    student_name = serializers.CharField(source='student.full_name', read_only=True)
    comments     = LogCommentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = WeeklyLog
        fields = [
            'id', 'placement', 'student', 'student_name',
            'week_number', 'week_start', 'week_end',
            'activities', 'learning', 'challenges', 'next_week',
            'status', 'status_display', 'comments',
            'submitted_at', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'student', 'student_name', 'submitted_at', 'created_at', 'updated_at']


class WeeklyLogCreateSerializer(serializers.ModelSerializer):
    """Used by student to create or update a draft log."""

    class Meta:
        model  = WeeklyLog
        fields = [
            'week_number', 'week_start', 'week_end',
            'activities', 'learning', 'challenges', 'next_week',
        ]

    def validate(self, data):
        start = data.get('week_start')
        end   = data.get('week_end')
        if start and end and end < start:
            raise serializers.ValidationError({'week_end': 'Week end must be on or after week start.'})
        return data


class WeeklyLogSubmitSerializer(serializers.Serializer):
    """Empty body — action endpoint to move draft → submitted."""
    pass


class WeeklyLogReviewSerializer(serializers.Serializer):
    """
    Workplace supervisor: approve or reject a submitted log,
    optionally adding a comment in the same action.
    """

    ACTION_CHOICES = [('approve', 'Approve'), ('reject', 'Reject')]

    action  = serializers.ChoiceField(choices=ACTION_CHOICES)
    comment = serializers.CharField(required=False, allow_blank=True)


class LogCommentCreateSerializer(serializers.ModelSerializer):
    """Create a standalone comment on a log."""

    class Meta:
        model  = LogComment
        fields = ['comment']