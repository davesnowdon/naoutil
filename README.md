# naoutil

A project containing useful utility code for NAO developers (mostly in
python). Includes support for i18n and JSON serialisation of arbitrary
classes

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

# get a list of strings (options for random text) from the basename
 "defaults"
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
Provides functions to_json() and from_json() that allow arbitrary classes to be converted to/from JSON providing that they implement 2 helper functions. The classes may also need to implement the __eq__function and name if these aren't defined in sub-classes. The two functions below demonstrate this. JsonTestBase is a class with no data but which can be serialised and deserialised so you get back a class of the same type, JsonWithData is a more interesting data-bearing class.

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
</code></pre>


