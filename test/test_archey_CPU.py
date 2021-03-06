
import unittest
from unittest.mock import mock_open, patch

from archey.archey import CPU


class TestCPUEntry(unittest.TestCase):
    """
    Here, we mock the `open` call on `/proc/cpuinfo` with fake content.
    """
    @patch(
        'archey.archey.open',
        mock_open(
            read_data="""\
processor\t: 0
vendor_id\t: CPU-VENDOR-NAME
cpu family\t: X
model\t\t: YY
model name\t: CPU-MODEL-NAME
"""),
        create=True
    )
    def test_model_name_match_proc_cpuinfo(self):
        self.assertEqual(CPU().value, 'CPU-MODEL-NAME')

    """
    See issue #29 (ARM architectures).
    `/proc/cpuinfo` will not contain `model name` info.
    `lscpu` output will be used instead.
    """
    @patch(
        'archey.archey.open',
        mock_open(
            read_data="""\
processor\t: 0
vendor_id\t: CPU-VENDOR-NAME
cpu family\t: X
model\t\t: YY
"""),
        create=True
    )
    @patch(
        'archey.archey.check_output',
        return_value="""\
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              4
On-line CPU(s) list: 0-3
Thread(s) per core:  X
Core(s) per socket:  Y
Socket(s):           1
NUMA node(s):        1
Vendor ID:           CPU-VENDOR-NAME
CPU family:          Z
Model:               \xde\xad\xbe\xef
Model name:          CPU-MODEL-NAME-WITHOUT-PROC-CPUINFO
""")
    def test_model_name_match_lscpu(self, check_output_mock):
        self.assertEqual(CPU().value, 'CPU-MODEL-NAME-WITHOUT-PROC-CPUINFO')

    @patch(
        'archey.archey.open',
        mock_open(
            read_data="""\
processor\t: 0
vendor_id\t: CPU-VENDOR-NAME
cpu family\t: X
model\t\t: YY
model name\t: CPU  MODEL\t  NAME
"""),
        create=True
    )
    def test_spaces_squeezing(self):
        self.assertEqual(CPU().value, 'CPU MODEL NAME')


if __name__ == '__main__':
    unittest.main()
