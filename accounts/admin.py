from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('id','Id_No', 'first_name', 'last_name', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)# degisebilir
    fieldsets = (
        (None, {'fields': ('Id_No', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'city', 'district', 'phone')}),
        ('Permissions', {'fields': ( 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('Id_No', 'first_name', 'last_name', 'email', 'city', 'district', 'phone', 'password1', 'password2', 'is_staff', 'is_active',)}
        ),
    )
    search_fields = ('Id_No', 'email', 'first_name', 'last_name')
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(MyUser, MyUserAdmin)
