__author__ = 'john'

import unittest

from pyvarnish.parse_stats import VarnishGather, msg


class TestVarnishGather(unittest.TestCase):
    """"""
    def test_parse_xml(self):
        """Constructor"""
        server = "mytestserver"
        vg = VarnishGather(server)
        vg.parse_xml("test_data.xml")

        message = msg(vg.lines)

        self.assertEqual(message.strip(), open("test_message.txt").read())



if __name__ == '__main__':
    unittest.main()