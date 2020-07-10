import unittest

from package_name.template import Template

name = 'test'


class TestTemplateInit(unittest.TestCase):
    def test_attributes(self):
        """Test initialization of Template class"""
        model = Template(name)
        self.assertEqual(model.name, name)


class TestTemplate(unittest.TestCase):
    def setUp(self):
        self.model = Template(name)

    def test_add(self):
        """Test add"""
        value = self.model.add(1, 2)
        self.assertEqual(value, 3)


if __name__ == '__main__':
    unittest.main()
