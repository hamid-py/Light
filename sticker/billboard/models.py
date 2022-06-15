from django.db import models

from result.models import CustomUser


class GroupMessage(models.Model):
    inbound = 'IN'
    outbound = 'OUT'
    crm = 'CRM'
    all = 'ALL'
    marjouee = 'MJ'
    group_type = (
        (inbound, 'inbound'),
        (outbound, 'outbound'),
        (crm, 'crm'),
        (marjouee, 'marjouee'),
        (all, 'all')
    )
    group_type = models.CharField(choices=group_type, max_length=3)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_type


class Category(models.Model):
    training = 'TR'
    news = 'NE'
    category_type = (
        (training, 'training'),
        (news, 'news')

    )
    category_type = models.CharField(choices=category_type, max_length=2)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_type


class Configuration(models.Model):
    font_size = models.PositiveIntegerField(default=20)
    color = models.CharField(max_length=10, default='black')
    text_align = models.CharField(max_length=10, default='justify')
    background_color = models.CharField(max_length=10, default='white')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'(font_size{self.font_size},color{self.color},' \
               f'text_align{self.text_align},background_color{self.background_color})'


class Message(models.Model):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    group_message = models.ForeignKey(GroupMessage, on_delete=models.CASCADE, name='group_message')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, name='category')
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE, name='configuration')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=500)
    image = models.ImageField(blank=True, upload_to='image')

    def __str__(self):
        return f'message:{self.content}'
