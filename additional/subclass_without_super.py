from base_class import BaseClass


class SubclassWithoutSuper(BaseClass):
    def __init__(self):
        # Brak wywołania super(), co powinno być zauważone przez DependencyMapper
        print("SubclassWithoutSuper initialized")

    def additional_method(self):
        print("Additional method of SubclassWithoutSuper")
