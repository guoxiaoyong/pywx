import sys
import os
import glob
import imp

# Process text message content.
class ContentProc():
  def __init__(self):
    self._actions = []
    script_dir = os.path.abspath(os.path.dirname(__file__))
    action_dir = os.path.join(script_dir, 'content_proc')
    scripts = glob.glob(os.path.join(action_dir, '*.py'))
    for script in scripts:
      modname = os.path.basename(script).split('.')[0]
      mod = imp.load_source('ContextProc_' + modname, script)
      self._actions.append(eval('mod.' + modname))

  def proc(self, reqmsg):
    for action in self._actions:
      result = action(reqmsg):
      if result:
        return result


if __name__ == '__main__':
  content_proc = ContentProc()
  for modname in sys.modules.keys():
    if 'ContextProc_' in modname:
      print modname

  print '------------------------------'
  for action in content_proc._actions:
    print action
