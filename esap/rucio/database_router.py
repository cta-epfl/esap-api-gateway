class RucioRouter:

    route_app_labels = {'rucio'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read rucio models go to rucio database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'rucio'

    def db_for_write(self, model, **hints):
        """
        Writes always go to rucio.
        """
        return 'rucio'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the rucio apps is
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
        Make sure the rucio apps only appear in the
        'rucio' database.
        """
        if app_label in self.route_app_labels:
            return db == 'rucio'
        return None