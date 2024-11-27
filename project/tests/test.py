import os.path
import unittest

from . import *
from ..package import pp, pphtml

class Tests(unittest.TestCase):

    html_processor = pphtml.Processor()

    def _infix(self, fn   :str, 
                     infix:str): return infix.join(os.path.splitext(fn))

    def _test(self, p:pp.Processor,fn:str):

        tfn = testfile_path(fn)
        ofn = self._infix(tfn, '-got')
        with open(testfile_path(fn)) as f:

            p.by_name(file_name=fn, ofile_name=ofn)

        with open(ofn) as of:

            with open(self._infix(tfn, '-expected')) as ef:

                self.assertEqual(of.read(), ef.read())  

    def test_1(self): self._test(pphtml.Processor(), fn='html1.md')
