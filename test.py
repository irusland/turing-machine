import io
import unittest
from os.path import join, isfile

import main
import sys
import os


def run(self, in_path, out_path):
    sys.stdout = io.StringIO()
    with open(in_path) as f:
        sys.stdin = f
        main.main()
    with open(out_path) as f:
        actual = sys.stdout.getvalue()
        expected = f.read()
        self.assertMultiLineEqual(actual, expected)


def get_test_names(path):
    names = set()
    for f in os.listdir(path):
        if isfile(join(path, f)):
            name, ext = os.path.splitext(f)
            names.add(join(path, name))
        else:
            names.update(get_test_names(join(path, f)))
    print(names)
    return names


def make_in_out_pair(name):
    in_path = f'{name}.in'
    out_path = f'{name}.out'
    return in_path, out_path


class MyTestCase(unittest.TestCase):
    def test(self):
        self.maxDiff = None
        path = 'tests'
        for name in get_test_names(path):
            i, o = make_in_out_pair(name)
            with self.subTest(name):
                run(self, i, o)

    def test_F(self):
        i = 'tests/F_power2/1.in'
        o = 'tests/F_power2/1.out'
        run(self, i, o)

    def test_E(self):
        i = 'tests/E_addition_tests/10+11.in'
        o = 'tests/E_addition_tests/10+11.out'
        run(self, i, o)


if __name__ == '__main__':
    unittest.main()
