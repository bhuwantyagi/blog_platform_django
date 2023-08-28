# tests.py

import json
from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User
from blog.models import Post

class BlogAPITestCase(TestCase):

    @patch('blog.schema.create_token')
    def test_create_user(self, mock_create_token):
        mock_create_token.return_value = 'test_token'
        
        query = '''
        mutation {
          createUser(username: "testuser", email: "testuser@gmail.com", password: "testpassword") {
            user {
              username
            }
            token
          }
        }
        '''
        
        response = self.client.post('/graphql/', {'query': query})
        content = json.loads(response.content)
        
        self.assertTrue(content['data']['createUser']['user'])
        self.assertEqual(content['data']['createUser']['user']['username'], 'testuser')
        self.assertEqual(content['data']['createUser']['token'], 'test_token')

    @patch('jwt.decode')
    def test_create_post(self, mock_jwt_decode):
        mock_jwt_decode.return_value = {'user_id': 1}
        User.objects.create_user(username='test', password='test')

        query = '''
        mutation {
          createPost(token: "some_token", title: "New Post", content: "This is a new post") {
            post {
              title
            }
            success
            errors
          }
        }
        '''
        
        response = self.client.post('/graphql/', {'query': query})
        content = json.loads(response.content)
        
        self.assertTrue(content['data']['createPost']['success'])
        self.assertEqual(content['data']['createPost']['post']['title'], 'New Post')

    @patch('jwt.decode')
    def test_edit_post(self, mock_jwt_decode):
        user = User.objects.create_user(username='test', password='test')
        mock_jwt_decode.return_value = {'user_id': user.id}
        post = Post.objects.create(title='Existing Post', content='This is an existing post', author=user)

        query = f'''
        mutation {{
          editPost(token: "some_token", postId: {post.id}, title: "Edited Post") {{
            post {{
              title
            }}
            success
            errors
          }}
        }}
        '''

        response = self.client.post('/graphql/', {'query': query})
        content = json.loads(response.content)
        
        self.assertTrue(content['data']['editPost']['success'])
        self.assertEqual(content['data']['editPost']['post']['title'], 'Edited Post')

    @patch('jwt.decode')
    def test_delete_post(self, mock_jwt_decode):
        user = User.objects.create_user(username='test', password='test')
        mock_jwt_decode.return_value = {'user_id': user.id}
        post = Post.objects.create(title='Existing Post', content='This is an existing post', author=user)

        query = f'''
        mutation {{
          deletePost(token: "some_token", postId: {post.id}) {{
            success
            errors
          }}
        }}
        '''
        
        response = self.client.post('/graphql/', {'query': query})
        content = json.loads(response.content)

        self.assertTrue(content['data']['deletePost']['success'])

    # Test for invalid JWT token
    @patch('jwt.decode')
    def test_invalid_jwt_token(self, mock_jwt_decode):
        mock_jwt_decode.side_effect = Exception('Invalid Token')

        query = '''
        mutation {
          createPost(token: "invalid_token", title: "New Post", content: "This is a new post") {
            post {
              title
            }
            success
            errors
          }
        }
        '''
        
        response = self.client.post('/graphql/', {'query': query})
        content = json.loads(response.content)
        
        self.assertFalse(content['data']['createPost']['success'])
        self.assertEqual(content['data']['createPost']['errors'], 'Invalid Token')
        
