class QueryRouter:

    route_app_labels = {'query', 'auth', 'contenttypes', 'sessions', 'admin'}
    custom_router_app_labels = {'ida', 'rucio', 'accounts', 'staging'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label not in self.custom_router_app_labels:
            return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label not in self.custom_router_app_labels:
            return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the query apps is
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
        Make sure the query apps only appear in the
        'query' database.
        """
        if app_label in self.route_app_labels:
            return db == 'default'
        elif app_label in self.custom_router_app_labels:
            return db == app_label

        return None

