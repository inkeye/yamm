from unittest import TestCase, main

from yamm import Chain


class ChainTest(TestCase):
    def test_order(self):
        chain0 = Chain({(1,): {2: 1}, (2,): {1: 1}})
        chain1 = Chain({(1, 2): {2: 1}, (2, 3): {3: 1}, (3, 1): {1: 1}})
        chain2 = Chain({(1, 2, 1): {2: 1}, (2, 1, 2): {1: 1}})
        self.assertEqual(chain0.order, 1)
        self.assertEqual(chain1.order, 2)
        self.assertEqual(chain2.order, 3)

    def test_equal(self):
        test = Chain({(1,): {1: 1, 2: 1}, (2,): {1: 1}})
        check = Chain({(2,): {1: 1}, (1,): {2: 1, 1: 1}})
        self.assertEqual(test, check)

    def test_vary1(self):
        test = Chain({})
        test.vary_weight((1,), 1)
        check = Chain({(1,): {1: 1}})
        self.assertEqual(test, check)

    def test_vary2(self):
        test = Chain({(1,): {1: 1}})
        test.vary_weight((1,), 1)
        check = Chain({(1,): {1: 2}})
        self.assertEqual(test, check)

    def test_vary3(self):
        test = Chain({(1,): {1: 1}})
        test.vary_weight((1,), 2)
        check = Chain({(1,): {1: 1, 2: 1}})
        self.assertEqual(test, check)

    def test_vary_delete(self):
        test = Chain({(1,): {1: 1}})
        test.vary_weight((1,), 1, -1)
        check = Chain({})
        self.assertEqual(test, check)

    def test_from_data1(self):
        test = Chain.from_data([1, 2, 1, 1])
        check = Chain({(1,): {1: 1, 2: 1, None: 1}, (2,): {1: 1}})
        self.assertEqual(test, check)

    def test_from_data2(self):
        test = Chain.from_data([1, 2, 1, 1], 2)
        check = Chain({(1, 2): {1: 1}, (2, 1): {1: 1}, (1, 1): {None: 1}})
        self.assertEqual(test, check)

    def test_merge(self):
        chain0 = Chain({(1,): {2: 1}, (2,): {1: 1}})
        chain1 = Chain({(1,): {2: 1}, (3,): {1: 1}})
        test = chain0.merge(chain1)
        check = Chain({(1,): {2: 2}, (2,): {1: 1}, (3,): {1: 1}})
        self.assertEqual(test, check)

    def test_step(self):
        chain = Chain({(1,): {1: 1, 2: 1}, (2,): {1: 1}})
        test = chain.step((2,))
        check = 1
        self.assertEqual(test, check)

    def test_walk(self):
        chain = Chain({(1,): {2: 1}, (2,): {3: 1}, (3,): {None: 1}})
        test = chain.walk((1,))
        check = (1, 2, 3)
        for t, c in zip(test, check):
            self.assertEqual(t, c)

    def test_walk_until(self):
        chain = Chain({(1,): {1: 1, 2: 1}, (2,): {1: 1}})
        test = len(chain.walk_until((1,), 8))
        check = 8
        self.assertEqual(test, check)

    def test_distribute1(self):
        dic = {1: 3, 2: 3, 3: 3}
        gen = Chain.distribute(dic)
        test = [next(gen) for i in range(9)]
        check = [1, 2, 3, 1, 2, 3, 1, 2, 3]
        self.assertEqual(test, check)

    def test_distribute2(self):
        dic = {1: 9, 2: 6, 3: 3}
        gen = Chain.distribute(dic)
        test = [next(gen) for i in range(18)]
        check = [1, 2, 1, 3, 2, 1, 1, 2, 1, 3, 2, 1, 1, 2, 3, 1, 2, 1]
        self.assertEqual(test, check)

    def test_walk_deterministic1(self):
        chain = Chain({(1,): {2: 1}, (2,): {3: 1}, (3,): {None: 1}})
        chain.make_deterministic_map()
        test = list(chain.walk_deterministic_until((1,), 3))
        check = (1, 2, 3)
        for t, c in zip(test, check):
            self.assertEqual(t, c)

    def test_walk_deterministic2(self):
        chain = Chain({(1,): {2: 1}, (2,): {3: 1}, (3,): {None: 1}})
        chain.make_deterministic_map()
        test1 = list(chain.walk_deterministic_until((1,), 2))
        test2 = list(chain.walk_deterministic_until((3,), 2))
        check1 = (1, 2)
        check2 = (3, None)
        for t, c in zip(test1, check1):
            self.assertEqual(t, c)
        for t, c in zip(test2, check2):
            self.assertEqual(t, c)


if __name__ == "__main__":
    main()
