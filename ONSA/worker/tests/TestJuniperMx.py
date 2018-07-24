# # tests/TestNsxEdges.py
# import unittest
# import sys
# sys.path.append('../lib/')
# from juniper import Handler, VcpeHandler, CpelessHandler

# class JuniperMxTestCase(unittest.TestCase):
# 	dev = None

# 	@classmethod
# 	def setUpClass(cls):
# 		handler = Handler.Handler.factory("irs","MX_VCPE", "10.120.78.190")
# 		dev, status = handler._open_conn()
# 		status = handler._lock_config(dev)

# 	@classmethod
# 	def tearDownClass(cls):
# 		status = handler._unlock_config(dev)
# 		status = handler._close_conn(dev)

# 	@unittest.skip("")
# 	def test_MxSetInterfaces(self):
# 		self.assertNotEqual(None, r_config)

# 	def test_MxSetStaticRoute(self):
# 		self.assertEqual(204, 204)

	
# if __name__ == '__main__':
# 	suite = unittest.TestSuite()
# 	suite = unittest.TestLoader().loadTestsFromTestCase(JuniperMxTestCase)
# 	unittest.TextTestRunner(verbosity=2).run(suite)
