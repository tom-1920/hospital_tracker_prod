class HospitalDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['hospital_a', 'hospital_b', 'hospital_c']:
            return f"{model._meta.app_label}_db"
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['hospital_a', 'hospital_b', 'hospital_c']:
            return f"{model._meta.app_label}_db"
        return 'default'
