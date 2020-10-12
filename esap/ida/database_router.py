class IdaRouter:

    route_app_labels = {'ida'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read ida models go to ida database.
        """
        if model._meta.app_label in self.route_app_labels:
            # return 'ida'
            return 'default'

    def db_for_write(self, model, **hints):
        """
        Writes always go to ida.
        """
        #return 'ida'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the ida apps is
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
        Make sure the ida apps only appear in the
        'ida' database.
        """
        if app_label in self.route_app_labels:
            #return db == 'ida'
            return db == 'default'

        return None
