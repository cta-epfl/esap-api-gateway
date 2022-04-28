class BatchRouter:

    route_app_labels = {'batch'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read batch models go to batch database.
        """
        if model._meta.app_label in self.route_app_labels:
            # return 'batch'
            return 'default'

    def db_for_write(self, model, **hints):
        """
        Writes always go to batch.
        """
        #return 'batch'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the batch apps is
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
        Make sure the batch apps only appear in the
        'batch' database.
        """
        if app_label in self.route_app_labels:
            #return db == 'batch'
            return db == 'default'

        return None
