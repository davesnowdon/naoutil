'''
Created on August 31, 2013

@author: AxelVoitier
@license: GNU LGPL v3

Test suite for naoutil.broker module.
'''
import unittest

import naoqi

from naoutil import avahi, broker

def mock_avahi_find_all_naos(ip_v6=False):
    '''
    Mockup function replacing find_all_naos in avahi module.
    The dataset has been taken during the UK Hackathon 2013.
    It should have:
    - Several robots in the list.
    - A nao.local robot.
    - A robot that is 'local' like if it was running on this robot itself
      (it actually has two local because of the two internet interface,
      eth and wifi). They should be at the end of the list because we prune them
      in one test.
    - A robot with an unusual port.
    '''
    return [ {'host_name': 'Pepper.local',
              'ip_address': '138.37.60.137',
              'local': False,
              'naoqi_port': 9559,
              'robot_name': 'Pepper',
              'favorite': False},
             {'host_name': 'naoFernando.local',
              'ip_address': '138.37.60.4',
              'local': False,
              'naoqi_port': 9559,
              'robot_name': 'naoFernando',
              'favorite': False},
             {'host_name': 'MacDave.local',
              'ip_address': '138.37.60.166',
              'local': False,
              'naoqi_port': 9559,
              'robot_name': 'MacDave',
              'favorite': False},
             {'host_name': 'nao.local',
              'ip_address': '138.37.60.85',
              'local': False,
              'naoqi_port': 9559,
              'robot_name': 'nao',
              'favorite': False},
             {'host_name': 'MBP15.local',
              'ip_address': '138.37.60.162',
              'local': False,
              'naoqi_port': 9559,
              'robot_name': 'MBP15',
              'favorite': False},
             {'host_name': 'mydell2.local',
              'ip_address': '138.37.60.170',
              'local': False,
              'naoqi_port': 9559,
              'robot_name': 'mydell2',
              'favorite': False},
             {'host_name': 'ALD-XXXX-LA.local',
              'ip_address': '138.37.60.160',
              'local': False,
              'naoqi_port': 57074,
              'robot_name': 'ALD-XXXX-LA',
              'favorite': False},
             {'host_name': 'Xor.local',
              'ip_address': '138.37.60.59',
              'local': False,
              'naoqi_port': 9559,
              'robot_name': 'Xor',
              'favorite': False},
             {'host_name': 'Vanilo.local',
              'ip_address': '138.37.60.116',
              'local': False,
              'naoqi_port': 9559,
              'robot_name': 'Vanilo',
              'favorite': False},
             {'host_name': 'zirup.local',
              'ip_address': '138.37.60.66',
              'local': True,
              'naoqi_port': 9559,
              'robot_name': 'zirup',
              'favorite': False},
             {'host_name': 'zirup.local',
              'ip_address': '169.254.95.24',
              'local': True,
              'naoqi_port': 9559,
              'robot_name': 'zirup',
              'favorite': False}]

class BaseResolveIpPort(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        avahi.find_all_naos = mock_avahi_find_all_naos
        # Used in test_default_params_local
        cls.fixture_local_robot = {'host_name': 'zirup.local',
                                   'ip_address': '138.37.60.66',
                                   'local': True,
                                   'naoqi_port': 9559,
                                   'robot_name': 'zirup',
                                   'favorite': False}
        # Used in test_unusual_port_with_id, test_unusual_port_with_id_and_port, test_id_ip_addr
        cls.fixture_unusual_port_robot = {'host_name': 'ALD-XXXX-LA.local',
                                          'ip_address': '138.37.60.160',
                                          'local': False,
                                          'naoqi_port': 57074,
                                          'robot_name': 'ALD-XXXX-LA',
                                          'favorite': False}
        cls.fixture_nao_local_robot = {'host_name': 'nao.local',
                                       'ip_address': '138.37.60.85',
                                       'local': False,
                                       'naoqi_port': 9559,
                                       'robot_name': 'nao',
                                       'favorite': False}
        # Used in test_unusual_port_forcing_port
        cls.fixture_nao_local_fake_port_robot = {'host_name': 'nao.local',
                                                 'ip_address': '138.37.60.85',
                                                 'local': False,
                                                 'naoqi_port': 7777, # Not like this in the dataset, on purpose
                                                 'robot_name': 'nao',
                                                 'favorite': False}
        # Used in test_default_params_first, test_id_host_name, test_id_robot_name
        cls.fixture_first_robot = {'host_name': 'Pepper.local',
                                   'ip_address': '138.37.60.137',
                                   'local': False,
                                   'naoqi_port': 9559,
                                   'robot_name': 'Pepper',
                                   'favorite': False}
        # Used in test_default_when_nothing
        cls.fixture_default_nao_local_robot = {'ip_address': 'nao.local', # Not in the dataset
                                               'naoqi_port': 9559}
        # Used in test_unknown_id
        cls.fixture_unknown_robot = {'ip_address': 'unknown', # Not in the dataset
                                     'naoqi_port': 9559}
        # Used in ResolveIpPortWithFavorite
        cls.fixture_favorite_robot = {'host_name': 'mydell2.local',
                                      'ip_address': '138.37.60.170',
                                      'local': False,
                                      'naoqi_port': 9559,
                                      'robot_name': 'mydell2',
                                      'favorite': True}
        
    @classmethod
    def tearDownClass(cls):
        reload(avahi)

    def compare_to_fixture(self, ip_port, fixture, msg=''):
        self.assertEqual(ip_port[0], fixture['ip_address'])#, 'The IP address is wrong. ' + msg)
        self.assertEqual(ip_port[1], fixture['naoqi_port'], 'The naoQi port is wrong. ' + msg)

class ResolveIpPort(BaseResolveIpPort):
    def test_default_params_local(self):
        ip_port = broker._resolve_ip_port()
        self.compare_to_fixture(ip_port, self.fixture_local_robot, 'We expect the local robot.')
        
    def test_unusual_port_with_id(self):
        myFix = self.fixture_unusual_port_robot
        ip_port = broker._resolve_ip_port(nao_id=myFix['host_name'])
        self.compare_to_fixture(ip_port, myFix, 'In test with only nao_id.')
        
    def test_unusual_port_with_id_and_port(self):
        myFix = self.fixture_unusual_port_robot
        ip_port = broker._resolve_ip_port(nao_id=myFix['host_name'], nao_port=myFix['naoqi_port'])
        self.compare_to_fixture(ip_port, myFix, 'In test with nao_id and nao_port.')
        
    def test_unusual_port_forcing_port(self):
        myFix = self.fixture_nao_local_fake_port_robot
        ip_port = broker._resolve_ip_port(nao_id=myFix['host_name'], nao_port=myFix['naoqi_port'])
        self.compare_to_fixture(ip_port, myFix, 'In test forcing the port.')
        
    def test_unknown_id(self):
        ip_port = broker._resolve_ip_port(nao_id='unknown')
        self.compare_to_fixture(ip_port, self.fixture_unknown_robot, 'We expect the unknown/9559 robot.')
        
    def test_id_ip_addr(self):
        myFix = self.fixture_unusual_port_robot
        ip_port = broker._resolve_ip_port(nao_id=myFix['ip_address'])
        self.compare_to_fixture(ip_port, myFix, 'In testing with ip address.')
        
    def test_id_host_name(self):
        myFix = self.fixture_first_robot
        ip_port = broker._resolve_ip_port(nao_id=myFix['host_name'])
        self.compare_to_fixture(ip_port, myFix, 'In testing with host name.')
        
    def test_id_robot_name(self):
        myFix = self.fixture_first_robot
        ip_port = broker._resolve_ip_port(nao_id=myFix['robot_name'])
        self.compare_to_fixture(ip_port, myFix, 'In testing with robot name.')
        
class ResolveIpPortEmpty(BaseResolveIpPort):
    def setUp(self):
        avahi.find_all_naos = lambda ip_v6=False: []
        
    def test_default_when_nothing(self):
        ip_port = broker._resolve_ip_port()
        self.compare_to_fixture(ip_port, self.fixture_default_nao_local_robot, 'We expect the nao.local/9559 robot.')
        
    def tearDown(self):
        avahi.find_all_naos = mock_avahi_find_all_naos
        
class ResolveIpPortNoLocal(BaseResolveIpPort):
    def setUp(self):
        avahi.find_all_naos = lambda ip_v6=False: mock_avahi_find_all_naos()[:-2]
        
    def test_default_params_first(self):
        ip_port = broker._resolve_ip_port()
        self.compare_to_fixture(ip_port, self.fixture_first_robot, 'We expect the first robot.')
        
    def tearDown(self):
        avahi.find_all_naos = mock_avahi_find_all_naos
        
class ResolveIpPortWithFavorite(BaseResolveIpPort):
    def setUp(self):
        all_naos = mock_avahi_find_all_naos()
        all_naos[5]['favorite'] = True
        avahi.find_all_naos = lambda ip_v6=False: all_naos
        
    def test_default_params_favorite(self):
        ip_port = broker._resolve_ip_port()
        self.compare_to_fixture(ip_port, self.fixture_favorite_robot, 'We expect the favorite robot.')
        
    def tearDown(self):
        avahi.find_all_naos = mock_avahi_find_all_naos
        
class GetLocalIp(unittest.TestCase):
    def test_localhost(self):
        local_ip = broker._get_local_ip('localhost')
        self.assertEqual(local_ip, '127.0.0.1')
        
class FakeBroker(object):
    def __init__(self, *args):
        self.args = args
        self.shutdown_called = False
        
    def shutdown(self):
        self.shutdown_called = True
        
class CreateBroker(BaseResolveIpPort):
    @classmethod
    def setUpClass(cls):
        naoqi.ALBroker = FakeBroker
        reload(broker)
        BaseResolveIpPort.setUpClass()
        avahi.find_all_naos = lambda ip_v6=False: [{'host_name': 'localhost', 'ip_address': 'localhost', 'naoqi_port': 7777, 'local': True, 'favorite': False}]
        
    @classmethod
    def tearDownClass(cls):
        BaseResolveIpPort.tearDownClass()
        reload(naoqi)
        
    def test_default_params(self):
        with broker.create('MyBroker') as my_broker:
            broker_args = my_broker.args
            self.assertEqual(broker_args[0], 'MyBroker')
            self.assertEqual(broker_args[1], '127.0.0.1')
            self.assertEqual(broker_args[2], 0)
            self.assertEqual(broker_args[3], 'localhost')
            self.assertEqual(broker_args[4], 7777)
        self.assertTrue(my_broker.shutdown_called)
        
    def test_nao_id(self):
        with broker.create('MyBroker', nao_id='localhost') as my_broker:
            broker_args = my_broker.args
            self.assertEqual(broker_args[0], 'MyBroker')
            self.assertEqual(broker_args[1], '127.0.0.1')
            self.assertEqual(broker_args[2], 0)
            self.assertEqual(broker_args[3], 'localhost')
            self.assertEqual(broker_args[4], 7777)
        self.assertTrue(my_broker.shutdown_called)
        
    def test_nao_id_and_port(self):
        with broker.create('MyBroker', nao_id='localhost', nao_port=8888) as my_broker:
            broker_args = my_broker.args
            self.assertEqual(broker_args[0], 'MyBroker')
            self.assertEqual(broker_args[1], '127.0.0.1')
            self.assertEqual(broker_args[2], 0)
            self.assertEqual(broker_args[3], 'localhost')
            self.assertEqual(broker_args[4], 8888)
        self.assertTrue(my_broker.shutdown_called)
        
    def test_broker_ip(self):
        with broker.create('MyBroker', broker_ip='123.123.123.123') as my_broker:
            broker_args = my_broker.args
            self.assertEqual(broker_args[0], 'MyBroker')
            self.assertEqual(broker_args[1], '123.123.123.123')
            self.assertEqual(broker_args[2], 0)
            self.assertEqual(broker_args[3], 'localhost')
            self.assertEqual(broker_args[4], 7777)
        self.assertTrue(my_broker.shutdown_called)
        
    def test_broker_port(self):
        with broker.create('MyBroker', broker_port=9999) as my_broker:
            broker_args = my_broker.args
            self.assertEqual(broker_args[0], 'MyBroker')
            self.assertEqual(broker_args[1], '127.0.0.1')
            self.assertEqual(broker_args[2], 9999)
            self.assertEqual(broker_args[3], 'localhost')
            self.assertEqual(broker_args[4], 7777)
        self.assertTrue(my_broker.shutdown_called)
        
    def test_all_params(self):
        with broker.create('MyBroker', '123.123.123.123', 9999, 'localhost', 7777) as my_broker:
            broker_args = my_broker.args
            self.assertEqual(broker_args[0], 'MyBroker')
            self.assertEqual(broker_args[1], '123.123.123.123')
            self.assertEqual(broker_args[2], 9999)
            self.assertEqual(broker_args[3], 'localhost')
            self.assertEqual(broker_args[4], 7777)
        self.assertTrue(my_broker.shutdown_called)

if __name__ == '__main__':
    unittest.main()

