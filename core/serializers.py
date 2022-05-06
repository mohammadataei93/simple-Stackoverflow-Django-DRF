from .models import Question, Answer
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_answers(self, obj):
        results = obj.answers.all()
        return AnswerSerializer(instance=results, many=True).data

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
