from unittest import TestCase, main

from yamm import Chain


class ChainTest(TestCase):

    def test_from_data1(self):
        test = Chain.test_from_data([1, 2, 1, 1])
        check = {(1,): {1: 1, 2: 1},
                 (2,): {1: 1}}

        self.assertEqual(test, check)

    def test_from_data2(self):
        test = Chain.test_from_data([1, 2, 1, 1], 2)
        check = {(1, 2): {1: 1},
                 (2, 1): {1: 1}}

        self.assertEqual(test, check)

    def test_from_matrix(self):
        pass

    def test_step(self):
        chain = {(1,): {1: 1, 2: 1},
                 (2,): {1: 1}}
        test = chain.step(2)
        check = 1
        self.assertEqual(test, check)


if __name__ == '__main__':
    main()
