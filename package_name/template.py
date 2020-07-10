class Template:
    """example class"""

    def __init__(self, name):
        """initial function

        Args:
            name (str): name
        """
        self.name = name

    @staticmethod
    def add(a, b):
        """The sum function of two numbers

        Args:
            a (float): param1
            b (float): param2

        Returns:
            float: calculate result

        Example:
            >>> template.add(1, 2)
            3
        """
        c = a + b
        return c
