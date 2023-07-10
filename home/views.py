from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.


class PublicBlogView(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by("?")
            if request.GET.get("search"):
                search = request.GET.get("search")
                blogs = blogs.filter(
                    Q(title__icontains=search) | Q(blog_text__icontains=search)
                )
            serializer = BlogSerializer(blogs, many=True)
            # page_number = request.GET.get("page", 1)
            # pagiantor = Paginator(blogs, 10)
            # serializer = BlogSerializer(pagiantor.page(page_number), partial=True)
            return Response(
                {"data": serializer.data, "message": "Blog fetched successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"data": str(e), "message": "Somthing Went Worng!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # MARK: -  Get request for getting all the blog post

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)
            if request.GET.get("search"):
                search = request.GET.get("search")
                blogs = blogs.filter(
                    Q(title__icontains=search) | Q(blog_text__icontains=search)
                )
            serializer = BlogSerializer(blogs, many=True)
            return Response(
                {"data": serializer.data, "message": "Blog fetched successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"data": str(e), "message": "Somthing Went Worng!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # MARK: -  Create new post for the blog.

    def post(self, request):
        try:
            data = request.data
            data["user"] = request.user.id
            print(request.user.id)
            print(data)
            serializer = BlogSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    {"data": serializer.errors, "message": "Somthing Went Worng!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                serializer.save()
                return Response(
                    {"data": serializer.data, "message": "Blog created successfully"},
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            return Response(
                {"data": str(e), "message": "Somthing Went Worng!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # MARK: -  Update the blog post with new post or some changes

    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get["uid"]).first()
            if not blog.exists():
                return Response(
                    {"data": {}, "message": "Invalid blog uid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                if request.user != blog.user:
                    return Response(
                        {"data": {}, "message": "you are not authorized to do this"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    serializer = BlogSerializer(blog, data=data, partial=True)
                    if not serializer.is_valid():
                        return Response(
                            {
                                "data": serializer.errors,
                                "message": "Somthing Went Worng!",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        serializer.save()
                        return Response(
                            {
                                "data": serializer.data,
                                "message": "Blog Updated successfully",
                            },
                            status=status.HTTP_200_OK,
                        )

        except Exception as e:
            return Response(
                {"data": str(e), "message": "Somthing Went Worng!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get["uid"]).first()
            if not blog.exists():
                return Response(
                    {"data": {}, "message": "Invalid blog uid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                if request.user != blog.user:
                    return Response(
                        {"data": {}, "message": "you are not authorized to do this"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    blog.delete()
                    return Response(
                        {
                            "data": {},
                            "message": "Blog deleted successfully",
                        },
                        status=status.HTTP_200_OK,
                    )

        except Exception as e:
            return Response(
                {"data": str(e), "message": "Somthing Went Worng!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
