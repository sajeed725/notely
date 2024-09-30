from django.shortcuts import render

# Create your views here.
from rest_framework import generics,authentication,permissions

from notes.serializer import UserSerializer,TaskSerializer

from notes.models import User,Task

from rest_framework.response import Response

from notes.permissions import OwnerOnly

from rest_framework.views import APIView

class UserCreationView(generics.CreateAPIView):

    serializer_class=UserSerializer

    # def post(self,request,*args,**kwargs):

    #     serializer_instance=UserSerializer(data=request.data)

    #     if serializer_instance.is_valid():
            
    #         data=serializer_instance.validated_data

    #         User.objects.create_user(**data)

    #         return Response(data=serializer_instance.data)
    #     else:
    #         return Response(data=serializer_instance.errors)



class TaskListCreateView(generics.ListCreateAPIView):

    queryset=Task.objects.all()

    serializer_class=TaskSerializer

    # authentication_classes=[authentication.BasicAuthentication]

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):

        qs=Task.objects.filter(owner=self.request.user)

        if "category" in self.request.query_params:

            category_value=self.request.query_params.get("category")

            qs=qs.filter(category=category_value)

        if "priority" in self.request.query_params:

            priority_value=self.request.query_params.get("priority")

            qs=qs.filter(priority=priority_value)    

        return qs    
    

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset=Task.objects.all()

    serializer_class=TaskSerializer

    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]

from django.db.models import Count

class TaskSummaryApiView(APIView):

    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        qs=Task.objects.filter(owner=request.user)

        category_summary=qs.values("category").annotate(count=Count('category'))

        status_summary=qs.values("status").annotate(count=Count('status'))

        priority_summary=qs.values("priority").annotate(count=Count('priority'))
        
        task_count=qs.count()

        context={
            "category_summary":category_summary,
            "status_summary":status_summary,
            "priority_summary":priority_summary,
            "total_summary":task_count
        }

        return Response(data=context)
    

class CategorieListView(APIView):

    def get(self,request,*args,**kwargs):

        qs=Task.category_choices

        st={cat for tp in qs for cat in tp}

        return Response(data=st)