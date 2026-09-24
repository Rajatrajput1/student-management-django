from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        start_year = attrs.get(
            "start_year",
            self.instance.start_year if self.instance else None
        )

        end_year = attrs.get(
            "end_year",
            self.instance.end_year if self.instance else None
        )

        if start_year is not None and end_year is not None:
            if end_year < start_year:
                raise serializers.ValidationError(
                    "End year must be greater than or equal to start year."
                )

        return attrs

    class Meta:
        model = Student
        fields = "__all__"