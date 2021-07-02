from django.db import models


class EsapQuerySchema(models.Model):
    schema_name = models.CharField("Schema Name", max_length=50)

    def __unicode__(self):
        return self.schema_name

    def __str__(self):
        return self.schema_name

    class Meta:
        verbose_name = "Query Schema"
        verbose_name_plural = "Query Schemas"
        app_label = "accounts"


class EsapComputeResource(models.Model):
    resource_name = models.CharField("Resource Name", max_length=50)
    resource_type = models.CharField("Resource Type", max_length=50)
    resource_url = models.URLField("Resource URL")

    # resource_metadata = models.JSONField("Resource Metadata")
    # OR SUBCLASS??

    def __unicode__(self):
        return self.resource_name

    def __str__(self):
        return self.resource_name

    class Meta:
        verbose_name = "Compute Resource"
        verbose_name_plural = "Compute Resources"
        app_label = "accounts"


class EsapSoftwareRepository(models.Model):
    repository_name = models.CharField("Repository Name", max_length=50)
    repository_type = models.CharField("Repository Type", max_length=50)
    repository_url = models.URLField("Repository URL")
    # resource_metadata = models.JSONField("Resource Metadata")

    def __unicode__(self):
        return self.repository_name

    def __str__(self):
        return self.repository_name

    class Meta:
        verbose_name = "Software Repository"
        verbose_name_plural = "Software Repositories"
        app_label = "accounts"


class EsapUserProfile(models.Model):
    user_name = models.CharField("Username", max_length=50, primary_key=True)
    full_name = models.CharField("Full Name", max_length=100, null=True)
    user_email = models.EmailField("User Email")
    uid = models.CharField("uid", default="uid", max_length=255, null=True)
    oidc_id_token = models.TextField(null=True, blank=True)
    oidc_access_token = models.TextField(null=True, blank=True)

    query_schema = models.ForeignKey(
        to=EsapQuerySchema,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Preferred Query Schema",
        default=None,
    )
    software_repositories = models.ManyToManyField(
        to=EsapSoftwareRepository, verbose_name="Software Repositories", blank=True
    )
    compute_resources = models.ManyToManyField(
        to=EsapComputeResource, verbose_name="Compute Resources", blank=True
    )

    # nv:15jun2021, moved to EsapShoppingItem to reverse the relationship for 1-to-many
    # shopping_cart = models.ManyToManyField(
    #     to=EsapShoppingItem, verbose_name="Shopping Cart", blank=True,
    # )

    def __unicode__(self):
        return self.user_name

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        app_label = "accounts"


class EsapShoppingItem(models.Model):
    item_data = models.JSONField("Item Data")

    user_profile = models.ForeignKey(
        to=EsapUserProfile,
        related_name="shopping_cart",
        on_delete=models.CASCADE,
        verbose_name="User Profile",
        null=True,
        blank=True,
        default=None
    )

    def __unicode__(self):
        return "ShoppingItem"

    def __str__(self):
        return str(self.item_data)

    class Meta:
        verbose_name = "Selected Item"
        verbose_name_plural = "Selected Items"
        app_label = "accounts"

