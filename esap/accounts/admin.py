from django.contrib import admin
from .models import (
    EsapQuerySchema,
    EsapComputeResource,
    EsapSoftwareRepository,
    EsapShoppingItem,
    EsapUserProfile,
)


class AccountsDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = "accounts"

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(AccountsDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(AccountsDBModelAdmin, self).formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(AccountsDBModelAdmin, self).formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )


admin.site.register(EsapQuerySchema, AccountsDBModelAdmin)
admin.site.register(EsapComputeResource, AccountsDBModelAdmin)
admin.site.register(EsapSoftwareRepository, AccountsDBModelAdmin)
admin.site.register(EsapShoppingItem, AccountsDBModelAdmin)
admin.site.register(EsapUserProfile, AccountsDBModelAdmin)
