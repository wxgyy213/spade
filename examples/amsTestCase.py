import os
import sys
import time
import unittest

sys.path.append('..'+os.sep+'trunk')
sys.path.append('..')

import spade

host = "127.0.0.1"

class MyAgent(spade.Agent.Agent):

	def _setup(self):
            self.search = None
            
class SearchBehav(spade.Behaviour.OneShotBehaviour):
    
        def __init__(self, s):
            self.s = s
            spade.Behaviour.OneShotBehaviour.__init__(self)

        def _process(self):

            aad = spade.AMS.AmsAgentDescription()
            aad.setAID(spade.AID.aid(self.s+"@"+host,["xmpp://"+self.s+"@"+host]))
            self.myAgent.search = self.myAgent.searchAgent(aad)



class BasicTestCase(unittest.TestCase):
    
    def setUp(self):

    	self.a = MyAgent("a@"+host, "secret")
    	self.a.start()
    	self.b = MyAgent("b@"+host, "secret")
    	self.b.start()
    	
    def tearDown(self):
        self.a.stop()
        self.b.stop()
        
    def testSearchMe(self):
        self.a.addBehaviour(SearchBehav("a"), None)
        counter = 0
        while self.a.search == None and counter < 20:
            time.sleep(1)
            counter +=1
            
        if len(self.a.search)>1:  self.fail("Too many agents found")
        if len(self.a.search)==0: self.fail("No agents found")    

        self.assertEqual(self.a.search[0]["fipa:aid"]["fipa:name"], "a@"+host)
        
    def testSearchOther(self):
        self.a.addBehaviour(SearchBehav("b"), None)
        counter = 0
        while self.a.search == None and counter < 20:
            time.sleep(1)
            counter +=1

        if len(self.a.search)>1:  self.fail("Too many agents found")
        if len(self.a.search)==0: self.fail("No agents found")

        self.assertEqual(self.a.search[0]["fipa:aid"]["fipa:name"], "b@"+host)        

if __name__ == "__main__":
    unittest.main()


