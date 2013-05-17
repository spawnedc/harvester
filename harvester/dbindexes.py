from django.contrib.auth.models import User
from dbindexer.api import register_index

register_index(User, {
    'username': 'icontains',
    'email':'icontains',
    'first_name':'icontains',
    'last_name':'icontains'
})
