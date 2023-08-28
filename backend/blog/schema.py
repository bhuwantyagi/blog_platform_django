import graphene
from django.conf import settings
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User 
from .models import Post, PostComment
from .utils import create_token 
import jwt

class UserType(DjangoObjectType):
    class Meta:
        model = User

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class PostCommentType(DjangoObjectType):
    class Meta:
        model = PostComment

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))

    def resolve_all_posts(self, info):
        return Post.objects.all()

    def resolve_post_by_id(self, info, id):
        return Post.objects.get(id=id)

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        token = create_token(user)
        return CreateUser(user=user, token=token)

class CreatePost(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)
    success = graphene.Boolean()
    errors = graphene.String()

    def mutate(self, info, token, title, content):
        # Validate the token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload.get('user_id'))
        except Exception as e:
            return CreatePost(success=False, errors=str(e))

        # Create the post
        post = Post.objects.create(title=title, content=content, author=user)
        return CreatePost(post=post, success=True)


class EditPost(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)
        post_id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)
    success = graphene.Boolean()
    errors = graphene.String()

    def mutate(self, info, token, post_id, title=None, content=None):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload.get('user_id'))
        except Exception as e:
            return EditPost(success=False, errors=str(e))

        try:
            post = Post.objects.get(id=post_id, author=user)
            if title is not None:
                post.title = title
            if content is not None:
                post.content = content
            post.save()
            return EditPost(post=post, success=True)
        except Post.DoesNotExist:
            return EditPost(success=False, errors='Post does not exist')

class DeletePost(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)
        post_id = graphene.Int(required=True)

    success = graphene.Boolean()
    errors = graphene.String()

    def mutate(self, info, token, post_id):
        # print("/////////// for debug //////////////")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload.get('user_id'))
        except Exception as e:
            return DeletePost(success=False, errors=str(e))

        try:
            post = Post.objects.get(id=post_id, author=user)
            post.delete()
            return DeletePost(success=True)
        except Post.DoesNotExist:
            return DeletePost(success=False, errors='Post does not exist')

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()
    edit_post = EditPost.Field()
    delete_post = DeletePost.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
