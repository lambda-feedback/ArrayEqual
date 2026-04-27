import unittest

try:
    from .evaluation import evaluation_function
except ImportError:
    from evaluation import evaluation_function


class TestEvaluationFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use evaluation_function() to check your algorithm works
    as it should.
    """

    def test_2D_empty_string_in_answer(self):
        response = [[1, 1], [1, 1]]
        answer = [["", ""], ["", ""]]

        self.assertRaises(
            Exception,
            evaluation_function,
            response,
            answer,
            {},
        )

    def test_2D_empty_string_in_response(self):
        response = [["", ""], ["", ""]]
        answer = [[1, 1], [1, 1]]

        response = evaluation_function(response, answer, {})

        self.assertEqual(response["is_correct"], False)
        self.assertEqual(response["feedback"], "Response has at least one empty field.")

    def test_no_tolerance_correct(self):
        response = [1, 2]
        answer = [1, 2]

        response = evaluation_function(response, answer, {})

        self.assertEqual(response.get("is_correct"), True)

    def test_no_tolerance_incorrect(self):
        response = [1, 2]
        answer = [1, 2.1]

        response = evaluation_function(response, answer, {})

        self.assertEqual(response.get("is_correct"), False)

    def test_atol_correct(self):
        response = [1, 2]
        answer = [1, 2.1]
        params = {"atol": 0.12}

        response = evaluation_function(response, answer, params)

        self.assertEqual(response.get("is_correct"), True)

    def test_atol_incorrect(self):
        response = [1, 2]
        answer = [1, 2.2]
        params = {"atol": 0.12}

        response = evaluation_function(response, answer, params)

        self.assertEqual(response.get("is_correct"), False)

    def test_rtol_correct(self):
        response = [1, 1.91]
        answer = [1, 2]
        params = {"atol": 0.1}

        response = evaluation_function(response, answer, params)

        self.assertEqual(response.get("is_correct"), True)

    def test_rtol_incorrect(self):
        response = [1, 1.8]
        answer = [1, 2]
        params = {"atol": 0.1}

        response = evaluation_function(response, answer, params)

        self.assertEqual(response.get("is_correct"), False)

    def test_2D_correct(self):
        response = [[1, 1], [1, 1]]
        answer = [[1, 1], [1, 1]]

        response = evaluation_function(response, answer, {})

        self.assertEqual(response.get("is_correct"), True)

    def test_2D_incorrect(self):
        response = [[1, 1], [1, 1]]
        answer = [[1, 1], [1, 0]]

        response = evaluation_function(response, answer, {})

        self.assertEqual(response.get("is_correct"), False)

    def test_2D_incorrect_with_custom_feedback(self):
        response = [[1, 1], [1, 1]]
        answer = [[1, 1], [1, 0]]

        response = evaluation_function(response, answer, {"feedback_for_incorrect_response": "Custom feedback"})

        self.assertEqual(response.get("is_correct"), False)
        self.assertEqual(response["feedback"], "Custom feedback")

#    def test_3D_correct(self):
#        response = [[[1, 1], [2, 1]], [[2, 1.2], [2, 2]]],
#        answer = [[[1, 1], [2, 1.1]], [[2, 1], [2, 2]]]
#        params = {"atol": 1}
#
#        response = evaluation_function(response, answer, params)
#
#        self.assertEqual(response.get("is_correct"), True)

    def test_answer_not_array_of_numbers(self):
        response = [[1, 1], [1, 1]]
        answer = [[1, 1], [1, "a"]]

        self.assertRaises(
            Exception,
            evaluation_function,
            response,
            answer,
            {},
        )

    def test_response_not_array_of_numbers(self):
        response = [[1, 1], [1, "a"]]
        answer = [[1, 1], [1, 0]]

        response = evaluation_function(response, answer, {})

        self.assertEqual(response.get("is_correct"), False)
        self.assertEqual(response["feedback"], "Only numbers are permitted.")

if __name__ == "__main__":
    unittest.main()
