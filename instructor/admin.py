from django.contrib import admin

from instructor.models import User,Category,Course,Module
# Register your models here.

admin.site.register(User)

admin.site.register(Category)

class CourseAdmin(admin.ModelAdmin):

    exclude=('owner',)

    def save_model(self, request, obj, form, change):

        if not change:
            obj.owner=request.user
        return super().save_model(request, obj, form, change)



admin.site.register(Course,CourseAdmin)
