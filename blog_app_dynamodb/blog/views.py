from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, View
from django.urls import reverse_lazy
import boto3
from datetime import datetime
import base64
from blog.models import Blog
from blog.forms import BlogForm
# Create your views here.


def encode(dt_string):
    dt_string = dt_string.encode('ascii')
    base64_bytes = base64.b64encode(dt_string)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


class dynamodbcrud:
    def __init__(self):
        self.table = boto3.resource(
            'dynamodb',
            aws_access_key_id='your_aws_access_key_id=',
            aws_secret_access_key='your_aws_secret_access_key',
            region_name='your_region_name',
        ).Table('your_dynamodb_table_name')

    def db_readall(self):
        response = self.table.scan()
        return response['Items']

    def db_create(self, blogid, title, body):
        response = self.table.put_item(
            Item={
                'blogid': blogid,
                'title': title,
                'body': body
            }
        )

    def db_getitem(self, blogid):
        response = self.table.get_item(
            Key={'blogid': blogid})
        return response['Item']

    def db_update(self, blogid, title, body):
        response = self.table.delete_item(
            Key={
                'blogid': blogid
            })
        response = self.table.put_item(
            Item={
                'blogid': blogid,
                'title': title,
                'body': body
            }
        )

    def db_delete(self, blogid):
        response = self.table.delete_item(
            Key={
                'blogid': blogid
            })


class Index(View):
    def get(self, request):
        instance = dynamodbcrud()
        ml = instance.db_readall()
        ctx = {'blog_list': ml}
        return render(request, 'blog/blog_list.html', ctx)


class Home(View):
    def get(self, request):
        return render(request, "blog/home.html")


class Detail(View):
    def get(self, request, pk):
        instance = dynamodbcrud()
        ml = instance.db_getitem(pk)
        ctx = {'blog': ml}
        return render(request, 'blog/blog_detail.html', ctx)


class Create(CreateView):
    template = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:all')

    def get(self, request):
        form = BlogForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        instance = dynamodbcrud()
        now = datetime.now()
        datetimes = now.strftime("%d/%m/%Y %H:%M:%S")
        blogid = encode(datetimes)
        title = str(request.POST['title'])
        body = str(request.POST['body'])
        instance.db_create(blogid, title, body)
        return redirect(self.success_url)


class Update(UpdateView):
    model = Blog
    # fields = ['title', 'content']
    template = 'blog/blog_update.html'
    success_url = reverse_lazy('blog:all')

    def get(self, request, pk):
        instance = dynamodbcrud()
        blog = instance.db_getitem(pk)
        # print(blog.title)
        ctx = {'title': blog['title'], 'content': blog['body']}
        # print(ctx)
        return render(request, self.template, ctx)

    def post(self, request, pk):
        instance = dynamodbcrud()
        title = str(request.POST['title'])
        body = str(request.POST['body'])
        instance.db_update(pk, title, body)
        return redirect(self.success_url)


class Delete(DeleteView):
    template = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:all')

    def get(self, request, pk):
        instance = dynamodbcrud()
        blog = instance.db_getitem(pk)
        ctx = {'title': blog['title'], 'content': blog['body']}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        instance = dynamodbcrud()
        instance.db_delete(pk)
        return redirect(self.success_url)
