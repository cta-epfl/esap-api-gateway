class StagingRouter:

    route_app_labels = {'staging'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read staging models go to staging database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'staging'

    def db_for_write(self, model, **hints):
        """
        Writes always go to staging.
        """
        return 'staging'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the staging apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the staging apps only appear in the
        'staging' database.
        """
        if app_label in self.route_app_labels:
            return db == 'staging'
        return None