from django.db import models

# Create your models here.
class Users(models.Model):
    UserID=models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=50, blank=False)
    LastName = models.CharField(max_length=50)
    Password=models.CharField(max_length=50,blank=False)
    RoleID=models.IntegerField()
    Email = models.CharField(max_length=50,blank=False)
    PhoneNumber = models.CharField(max_length=50,blank=False)
    Status = models.SmallIntegerField()
    Gender= models.SmallIntegerField()
    Token=models.CharField(max_length=255)
    IsDeleted=models.BooleanField(default=False)
    class Meta:
        db_table = 'UserTable'
        