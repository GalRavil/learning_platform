from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Subject, Course
from .permissions import IsEnrolled
from .serializers import SubjectSerializer, CourseSerializer, \
    CourseWithContentsSerializer


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# # view for users to enroll in courses
# class CourseEnrollView(APIView):
# # user and password are sent by the client in the Authorization HTTP
#     # header encoded with Base64.
#     authentication_classes = (BasicAuthentication,)
#     # Allows access to authenticated users only
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, pk, format=None):   # only POST method allowed
#         course = get_object_or_404(Course, pk=pk)
#         course.students.add(request.user)
#         return Response({'enrolled': True})


# provides the read-only actions list() and retrieve()
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @detail_route(methods=['post'],
                  authentication_classes=[BasicAuthentication],
                  permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @detail_route(methods=['get'],
                  serializer_class=CourseWithContentsSerializer,
                  authentication_classes=[BasicAuthentication],
                  permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

