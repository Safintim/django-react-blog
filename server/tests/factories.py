import factory


class BaseFactory(factory.Factory):
    class Meta:
        model = dict


class PostFactory(BaseFactory):
    title = factory.Faker('pystr')
    text = factory.Faker('pystr')
