# naoutil

A project containing useful utility code for NAO developers (mostly in
python). Includes support for i18n and JSON serialisation of arbitrary
classes

## NaoEnvironment
NaoEnvironment provides a convenient way to access ALProxy instances
(ALMemory, ALMotion etc) without having to manually create them. It also
provides access to logging. The intent is to create an instance by calling
the make_environment() function passing in a reference to a choreographe
box. It's then possible to get the following functionality
* logging, via the log() method
* the path to the resources dir (assuming that the "resources" dir is at the sa e level as the src dir under which naoutil is located) using the resources_dir() method.
* the name of the current language using, curent_language()
* the 2-letter ISO code of the current language via current_language_code()
* localised test strings from property files using the localized_text() method and passing in the base name of the properties file and a key

<pre lang="python">
env = make_environment(choreographe_box)
lc = env.current_language_code()
env.log("Current language is " + lc)
env.memory.getData("ALMemory location")
# this assumes the resources dir contains a properties with a basene of
# defaults, such as defaults_XX.properties or defaults_XX.json where
# XX is a 2-letter ISO language code and that these files have the key "hello"
lt  = env.localized_text("defaults", "hello")
</pre>


## i18n
Choreographe boxes that allow text to be retrieved from files for easier management of i18n issues - main aim is to allow clean separation of code and "user visible" strings or other data that depends on the current language of the robot and so aid in translating NAO applications.

The idea is that all localised files are stored in a standard directory at the same level as behaviour.xar (I use resources). Each filename is composed of 3 pieces:

* basename - any name you choosce
* the two letter ISO code for the language of the text in the file
* an extension .properties for properties files and .txt for plain text files used for the random text functions

This code supports three operations
* getting a localised string from a properties file
* retrieving a random string from a text file (one string per line) and retrieving a random string from a property in a properties file (in this case a single string is split using a separator character and one of the split strings is chosen at random) or a JSON file (in which case the JSON file can encode the values as a list)
* basic support for java format property files using a modifed version of jprops (from https://github.com/mgood/jprops)

The idea behind the random text is that there are often places in a NAO app where you want NAO to say something but it gets a bit boring if he always says the same thing so this provide an easy solution and there is no need to change the choreographe or python code to add more options.

For example here is what a java properties file might look like:

<pre>
hello=Hello
attractAttention=Excuse me!/Oy! You over there!/Hey! I want to talk to you./Human, I wish to talk to you./You will be interrogated! Please!
</pre>

and here's the same content in JSON format

<pre lang="javascript"><code>
{
   "hello" : "Hello",
   "attractAttention" : [
       "Excuse me!",
       "Oy! You over there!",
       "Hey! I want to talk to you.",
       "Human, I wish to talk to you.",
       "You will be interrogated! Please!"
   ]
}
</code></pre>

The code will transparently use JSON or java properties format as long as properties files have a .properties extension and JSON files have a .json extension.

There are two ways to use this code:

###1) python
Look at the unit tests to get a better idea of how this works.

<pre lang="python"><code>
import util.i18n as i18n
# get the value of the property "hello" property in English from the 
# basename "defaults"
hello_value = i18n.get_property(self.resources_path, "defaults", "en", "hello")

# get a list of strings (options for random text) from the basename "defaults"
# in chinese from the property "attractAttention" separated by "/"
options = i18n.read_text_options(self.resources_path, "defaults", "zh", "attractAttention", "/")

# read the options from the plain text file with basename "example" in French
options = i18n.read_text_options(self.resources_path, "example", "fr")
</code></pre>

###2) Choreographe boxes</span>
**Localized Text Property**

* resourceDir - directory where files are located relative to behaviour.xar, I prefer "resources"
* resourceFile - basename (without language code or extension) of file to load
* resourceProperty - the name of the property to select from the properties file

**Random Localized Text**

Picks a random string from a text or properties file. Takes four parameters

* resourceDir - directory where files are located relative to behaviour.xar, I prefer "resources"
* resourceFile - basename (without language code or extension) of file to load
* resourceProperty - blank if using a plain text file otherwise the name of the property to select from the properties file
* resourceSeparator - separator to use when splitting strings from a property. If blank defaults to / Has no effect when reading plain text files


The project contains some example uses of these boxes.

In this project I've combined use of choreographe for the boxes and eclipse/pydev to manage the python code outside of choreographe. The eclipse project is inside the choreographe one and I've followed the maven directory structure so that the main python code is in src/main/python and the unit tests are in src/test/python. You'll need to include at least the src/main dir in your projects for the choreographe boxes to work

## JSON
Provides functions to_json_string(), to_json_file() and from_json_string(),
from_json_file() that allow arbitrary classes to be converted to/from JSON providing that they implement 2 helper functions. The classes may also need to implement the __eq__function and name if these aren't defined in sub-classes. The two functions below demonstrate this. JsonTestBase is a class with no data but which can be serialised and deserialised so you get back a class of the same type, JsonWithData is a more interesting data-bearing class.

<pre lang="python"><code>
class JsonTestBase(object):
    def __init__(self):
        super(JsonTestBase, self).__init__()
    
    def name(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # used to support JSON serialisation of custom classes
    def to_json(self):
        return { }

    # used to enable this class & sub types to be reconstituted from JSON
    @classmethod
    def from_json(klass, json_object):
        return klass()

class JsonWithData(JsonTestBase):
    def __init__(self, source, sensorData):
        super(JsonWithData, self).__init__()
        self.source = source
        self.sensorData = sensorData

    # used to support JSON serialisation of custom classes
    def to_json(self):
        return { 'source' : self.source,
                 'sensorData' : self.sensorData}

b = JsonWithData('foo', { 'a': 123, 'b' : 456})
json = to_json_string(b)
rev = from_json_string(json)
</code></pre>

## Broker
Provide an easy-to-create ALBroker. It auto-detects the IP/port of a NaoQi available somewhere on the network. This makes it possible for a developper to distribute behaviours creating their own broker without having to care about providing valid IPs/ports info.

It can be used in two different ways. The first is using the broker.create() method. It returns a context manager. This mean you can use it with a 'with' statement:

<pre lang="python"><code>
from naoutil import broker

with broker.create('MyBroker') as myBroker:
    ... # Code running inside the broker.

... # Outside of the with-block the broker is automatically shutdown. Even in case of an exception in your code (which will be raised back to you).
</code></pre>

Or you can use the Broker class of the broker module:

<pre lang="python"><code>
from naoutil import broker

myBroker = broker.Broker('MyBroker')
... # Code running inside the broker.
myBroker.shutdown()
</code></pre>

You can also provide the same parameters the original ALBroker class has, except here they are optional (and named):

* broker_ip: The IP on which the broker will listen. Be careful, listening only on 127.0.0.1 when your broker is not running on the robot will prevent you from subscribing to ALMemory events.
* broker_port: 0 let the broker find itself a free port.
* nao_id: An "ID" corresponding to a NAO robot. It can be an IP address, or a Bonjour/Avahi address, or a hostname, or a robot name (case sensitive).
* nao_port: Port used by the NaoQi process.

If you don't provide one of this parameter, it will be auto-detected. This means you could for instance just give nao_id='nao.local' or nao_id='nao'. It will resolve itself the nao_port, broker_ip and broker_port.


The auto-detection algorithm uses Bonjour/Avahi through DBus to find available NaoQis. It should be fine in most cases (ie. having only one robot at home, or running a broker directly on the robot itself).
The detection procedure goes as follow:

* If a nao_id is provided but not a nao_port,
  * If the nao_id correspond to an Avahi entry, get the nao_port and resolve the IP of the robot.
  * If there is no NaoQi with this ID on Avahi, it uses the default port, '9559', and the provided ID as a network address.
* If a nao_id is not provided,
  * If Avahi returns a NaoQi running locally on the machine, uses it.
  * Otherwise, get the first NaoQi Avahi can find.
  * If no NaoQi can be found by Avahi, use the default 'nao.local' IP address and '9559' port.
* If no broker_ip is given, try to find the IP of the network card routing to the detected nao IP.
* If no broker_port is given, use 0 (let the broker find itself a free port).

## ALModule
A wrapper around ALModule is provided in the naoutil package. It adds two significant features.

First, you don't need to declare your ALModule in the globals of your script. Neither you need to set the name of this global equal to the module name. This wrapper will do it all for you. Therefore, you can create new ALModule anywhere you want in your code: inside functions, modules, classes, etc.

Second, you don't need to provide a module name. The wrapper will create it for you, based on the fully qualified name of your sub-class.

<pre lang="python"><code>
from noaoutil import ALModule

class MyModule(ALModule):
    def __init__(self):
        ALModule.__init__(self)
        # Or
        ALModule.__init__(self, 'module_name')
        
def myFunction()
    aModule = MyModule()
    
myFunction()
</code></pre>

## Memory callbacks
This feature allows you to make callbacks on ALMemory events or micro-events without having to make-up a module for that. You just need to provide the event name and a callback function. The callback function can also be a python lambda.

<pre lang="python"><code>
from naoutil import memory

# Run inside a behaviour environment (ie. choregraphe box) or inside a self created broker.

def myEventCallback(dataName, value, message):
    print 'Event', dataName, value, message

memory.subscribeToEvent('RightBumperPressed', myEventCallback)
raw_input("Press ENTER to stop subscribing to RightBumperPressed\n")
memory.unsubscribeToEvent('RightBumperPressed')
</code></pre>

Available methods are:

* Events
  * subscribeToEvent(dataName, callback)
  * unsubscribeToEvent(dataname)
* Micro-events
  * subscribeToMicroEvent(dataName, callback, cbMessage='')
  * unsubscribeToMicroEvent(dataName)

