from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Subject, Course
from .serializers import SubjectSerializer


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# view for users to enroll in courses
class CourseEnrollView(APIView):
    # user and password are sent by the client in the Authorization HTTP
    # header encoded with Base64.
    authentication_classes = (BasicAuthentication,)
    # Allows access to authenticated users only
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):   # only POST method allowed
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})
