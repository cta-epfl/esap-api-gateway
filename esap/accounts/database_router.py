class AccountsRouter:

    route_app_labels = {'accounts'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read accounts models go to accounts database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'accounts'

    def db_for_write(self, model, **hints):
        """
        Writes always go to accounts.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'accounts'


    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a both involved models are in the accounts
        app.
        """
        if (
            obj1._state.db in self.route_app_labels and
            obj2._state.db in self.route_app_labels
        ):
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the accounts apps only appear in the
        'accounts' database.
        """
        if app_label in self.route_app_labels:
            return db == 'accounts'
        return False
