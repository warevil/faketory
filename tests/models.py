class Sample:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class SampleChild(Sample):
    def __init__(self, name, email, age):
        super().__init__(name, email)
        self.age = age


class SampleDjango(SampleChild):
    def __init__(self, name, email, age, year):
        super().__init__(name, email, age)
        self.year = year

    def save(self):
        # We're mocking save by replacing year
        self.year = 3000


class SampleHasChild:
    def __init__(self, email, child):
        self.email = email
        self.child = child
