from os import system, makedirs
from shutil import copyfile
from time import sleep

from dogtail.config import config
from dogtail.utils import isA11yEnabled, enableA11y

from common_steps import App

if not isA11yEnabled():
    enableA11y(True)


def before_all(context):
    """
    Setup stuff
    Being executed before all features
    """

    try:
        # Skip dogtail actions to print to stdout
        config.logDebugToStdOut = False
        config.typingDelay = 0.2

        context.app_class = App('gnome-sound-recorder')

        context.screenshot_counter = 0
        context.save_screenshots = False
    except Exception as e:
        print('Error in before_all: %s' % e.message)


def before_tag(context, tag):
    try:
        # Copy screenshots
        if 'screenshot' in tag:
            context.save_screenshots = True
            context.screenshot_dir = '../sr_screenshots'
            makedirs(context.screenshot_dir)
    except Exception as e:
        print('Error in before_tag: %s' % str(e))


def after_step(context, step):
    try:
        if hasattr(context, 'embed'):
            # Embed screenshot if HTML report is used
            system('dbus-send --session --type=method_call ' +
                   "--dest='org.gnome.Shell.Screenshot' " +
                   "'/org/gnome/Shell/Screenshot' " +
                   'org.gnome.Shell.Screenshot.Screenshot ' +
                   'boolean:false boolean:false string:/tmp/screenshot.png')
            if context.save_screenshots:
                # Don't embed screenshot if this is a screenshot tour page
                name = '%s/screenshot_%s_%02d.png' % (
                    context.screenshot_dir,
                    context.current_locale,
                    context.screenshot_counter)

                copyfile('/tmp/screenshot.png', name)
                context.screenshot_counter += 1
            else:
                context.embed('image/png',
                              open('/tmp/screenshot.png', 'r').read())
    except Exception as e:
        print('Error in after_step: %s' % str(e))


def before_scenario(context, scenario):
    """ Cleanup previous settings and make sure we have test files in /tmp """
    try:
        # cleanup()
        print('before')
    except Exception as e:
        print('Error in before_scenario: %s' % e.message)


def after_scenario(context, scenario):
    """Teardown for each scenario
    Kill eog (in order to make this reliable we send sigkill)
    """
    try:
        # Stop the app
        context.app_class.kill()

        # Pause after the scenario
        sleep(1)
    except Exception as e:
        # Stupid behave simply crashes if an exception has occurred
        print('Error in after_scenario: %s' % e.message)
