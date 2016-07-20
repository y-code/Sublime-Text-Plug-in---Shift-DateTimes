# -*- coding: utf-8 -*-

import sublime, sublime_plugin

import re
from datetime import datetime
from datetime import timedelta

class AddHourToDatetimesCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self._deltaDays = 0
        self._deltaHours = 1
        self._deltaMinutes = 0
        self._deltaSeconds = 0
    
    def run(self, edit):
        print("Command dastetime_edit started")
        self._edit = edit
        self._replace_all_datetime()
        print("Command dastetime_edit ended")

    def _get_file_content(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def _update_file(self, doc):
        self.view.replace(self._edit, sublime.Region(0, self.view.size()), doc)

    def _replace_all_datetime(self):
        doc = self._get_file_content()
        lines = doc.splitlines()
        result = []
        pattern0 = re.compile(u"([0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2})")
        pattern1 = re.compile(u"([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2})")
        pattern2 = re.compile(u"([0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2})")
        for line in lines:
            # print(line)
            match = pattern0.search(line)
            format = "%Y-%m-%d %H:%M:%S"
            if not match:
                match = pattern1.search(line)
                format = "%Y-%m-%dT%H:%M:%S"
            if not match:
                match = pattern2.search(line)
                format = "%d/%m/%Y %H:%M:%S"

            if match:
                d = match.group(0)
                print("* match: " + match.group(0))
                dt = datetime.strptime(d, format)
                dt += timedelta(days=self._deltaDays, hours=self._deltaHours, minutes=self._deltaMinutes, seconds=self._deltaSeconds)
                print("* converted data: " + dt.strftime(format))
                line = match.string[:match.start()] + dt.strftime(format) + match.string[match.end():]
                print("* output: " + line)
            
            result.append(line)
        
        line_ending = {
            "Windows" : "\r\n",
            "Unix"    : "\n",
            "CR"      : "\r"
        }[self.view.line_endings()]
        doc = line_ending.join(result)
        # print(doc)
        self._update_file(doc)


class SubHourToDatetimesCommand(AddHourToDatetimesCommand):
    def __init__(self, view):
        AddHourToDatetimesCommand.__init__(self, view)
        self._deltaDays = 0
        self._deltaHours = -1
        self._deltaMinutes = 0
        self._deltaSeconds = 0


class AddDayToDatetimesCommand(AddHourToDatetimesCommand):
    def __init__(self, view):
        AddHourToDatetimesCommand.__init__(self, view)
        self._deltaDays = 1
        self._deltaHours = 0
        self._deltaMinutes = 0
        self._deltaSeconds = 0


class SubDayToDatetimesCommand(AddHourToDatetimesCommand):
    def __init__(self, view):
        AddHourToDatetimesCommand.__init__(self, view)
        self._deltaDays = -1
        self._deltaHours = 0
        self._deltaMinutes = 0
        self._deltaSeconds = 0


class AddMinuteToDatetimesCommand(AddHourToDatetimesCommand):
    def __init__(self, view):
        AddHourToDatetimesCommand.__init__(self, view)
        self._deltaDays = 0
        self._deltaHours = 0
        self._deltaMinutes = 1
        self._deltaSeconds = 0


class SubMinuteToDatetimesCommand(AddHourToDatetimesCommand):
    def __init__(self, view):
        AddHourToDatetimesCommand.__init__(self, view)
        self._deltaDays = 0
        self._deltaHours = 0
        self._deltaMinutes = -1
        self._deltaSeconds = 0


class AddSecondToDatetimesCommand(AddHourToDatetimesCommand):
    def __init__(self, view):
        AddHourToDatetimesCommand.__init__(self, view)
        self._deltaDays = 0
        self._deltaHours = 0
        self._deltaMinutes = 0
        self._deltaSeconds = 1


class SubSecondToDatetimesCommand(AddHourToDatetimesCommand):
    def __init__(self, view):
        AddHourToDatetimesCommand.__init__(self, view)
        self._deltaDays = 0
        self._deltaHours = 0
        self._deltaMinutes = 0
        self._deltaSeconds = -1


