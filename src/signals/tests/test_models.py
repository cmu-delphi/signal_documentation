from django.core.exceptions import ValidationError
from django.test import TestCase

from signals.tests.factories import SignalFactory


class SignalModelTest(TestCase):
    def setUp(self):
        self.signal = SignalFactory()

    def test_signal_str(self):
        self.assertEqual(str(self.signal), self.signal.name)

    def test_signal_base_validation(self):
        self.signal.base = None
        with self.assertRaises(ValidationError):
            self.signal.clean()
        base = SignalFactory()
        self.signal.base = base
        self.signal.clean()
        self.assertEqual(self.signal.base, base)
