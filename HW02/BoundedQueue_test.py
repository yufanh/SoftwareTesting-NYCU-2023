import unittest
import BoundedQueue as BQ
"""  Base Choice Coverage (BCC)
Function	      Ch ID 	      Base	      Test Requirements	                  Infeasible TRs	      #TRs
BoundeQueue	      C1	          {5}	      {5}, {-5}, {0}		                                      3
enqueue	          C2, C3, C4      {T, T, T}	  {T, T, T} , {F, F, T}, {F, T, F}    {F, T, T}	              3
dequeue	          C5, C6	      {T, T}	  {T, T}, {F, F}	                  {T,F}, {F, T}	          2
is__empty	      C7	          {T}	      {T}, {F}		                                              2
is_full	          C8	          {F}	      {F}, {T}		                                              2
"""
class Test(unittest.TestCase):

    def test_BoundedQueue(self):
        # BoundeQueue c1 {5}
        test1_myBQ = BQ.BoundedQueue(5)
        with self.subTest():
            self.assertEqual(test1_myBQ.is_empty(), True)
            self.assertEqual(test1_myBQ.is_full(), False)

        # BoundeQueue c1 {-5}
        with self.subTest():
            with self.assertRaises(ValueError):
                test2_myBQ = BQ.BoundedQueue(-5)

        # BoundeQueue c1 {0}
        test3_myBQ = BQ.BoundedQueue(0)
        with self.subTest():
            self.assertEqual(test3_myBQ.is_empty(), True)
            self.assertEqual(test3_myBQ.is_full(), True)

    def test_enqueue(self):
        # enqueue C2, C3, C4  {T, T, T}
        test4_myBQ = BQ.BoundedQueue(2)
        test4_myBQ.enqueue("SoFtWaReTeStInG")
        with self.subTest():
            self.assertIn("SoFtWaReTeStInG", test4_myBQ.elements)

        # enqueue C2, C3, C4  {F, F, T}
        test5_myBQ = BQ.BoundedQueue(2)
        with self.subTest():
            with self.assertRaises(TypeError):
                test5_myBQ.enqueue(None)

        # enqueue C2, C3, C4  {F, T, F}
        test6_myBQ = BQ.BoundedQueue(2)
        test6_myBQ.enqueue("SoFtWaReTeStInG")
        test6_myBQ.enqueue("IcLaB")
        with self.subTest():
            with self.assertRaises(RuntimeError):
                test6_myBQ.enqueue("OsDi")


    def test_dequeue(self):
        # dequeue   C5, C6    {T, T}
        test7_myBQ = BQ.BoundedQueue(2)
        test7_myBQ.enqueue("SoFtWaReTeStInG")
        test7_myBQ.enqueue("IcLaB")
        with self.subTest():
                self.assertIn("SoFtWaReTeStInG", test7_myBQ.dequeue())

        # dequeue   C5, C6    {F, F}
        test8_myBQ = BQ.BoundedQueue(2)
        with self.subTest():
            with self.assertRaises(RuntimeError):
                test8_myBQ.dequeue()

    def test_is_empty(self):
        # is__empty C7  {T}
        test9_myBQ = BQ.BoundedQueue(2)
        with self.subTest():
            self.assertEqual(test9_myBQ.is_empty(), True)

        # is__empty C7  {F}
        test10_myBQ = BQ.BoundedQueue(2)
        test10_myBQ.enqueue("SoFtWaReTeStInG")
        test10_myBQ.enqueue("IcLaB")
        with self.subTest():
            self.assertEqual(test10_myBQ.is_empty(), False)

    def test_is_full(self):
        # is_full C8  {T}
        test11_myBQ = BQ.BoundedQueue(2)
        test11_myBQ.enqueue("SoFtWaReTeStInG")
        test11_myBQ.enqueue("IcLaB")
        with self.subTest():
            self.assertEqual(test11_myBQ.is_full(), True)

        # is_full C8  {F}
        test12_myBQ = BQ.BoundedQueue(2)
        with self.subTest():
            self.assertEqual(test12_myBQ.is_full(), False)

if __name__ == "__main__":
    unittest.main(verbosity=2)
    