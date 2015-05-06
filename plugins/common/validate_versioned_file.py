import pyblish.api
import re
import sys

@pyblish.api.log
class ValidateVersionWorkfile(pyblish.api.Validator):
    """Validates whether workFile is versioned and makes sure that version number of write nodes matches version of the
    work file
    """

    families = ['workFile']
    hosts = ['*']
    version = (0, 1, 0)

    host = sys.executable.lower()

    def process_instance(self, instance):
        current_file = instance.context.data('current_file')

        version = None
        version = int(self.version_get(current_file, 'v')[1])

        instance.context.set_data('version', value=version)
        new_workfile = self.version_up(current_file)
        instance.context.set_data('new_workfile', value=new_workfile)

        if not version:
            msg = 'Your workfile is not versioned!'
            raise Exception(msg)



    def version_get(self, string, prefix, suffix = None):
        """Extract version information from filenames.  Code from Foundry's nukescripts.version_get()"""

        if string is None:
           raise ValueError, "Empty version string - no match"

        regex = "[/_.]"+prefix+"\d+"
        matches = re.findall(regex, string, re.IGNORECASE)
        if not len(matches):
            msg = "No \"_"+prefix+"#\" found in \""+string+"\""
            raise ValueError, msg
        return (matches[-1:][0][1], re.search("\d+", matches[-1:][0]).group())


    def version_set(self, string, prefix, oldintval, newintval):
        """Changes version information from filenames. Code from Foundry's nukescripts.version_set()"""

        regex = "[/_.]"+prefix+"\d+"
        matches = re.findall(regex, string, re.IGNORECASE)
        if not len(matches):
            return ""

        # Filter to retain only version strings with matching numbers
        matches = filter(lambda s: int(s[2:]) == oldintval, matches)

        # Replace all version strings with matching numbers
        for match in matches:
            # use expression instead of expr so 0 prefix does not make octal
            fmt = "%%(#)0%dd" % (len(match) - 2)
            newfullvalue = match[0] + prefix + str(fmt % {"#": newintval})
            string = re.sub(match, newfullvalue, string)
        return string


    def version_up(self, string):

        try:
            (prefix, v) = self.version_get(string, 'v')
            v = int(v)
            file = self.version_set(string, prefix, v, v+1)
        except:
            raise ValueError, 'Unable to version up File'

        return file
