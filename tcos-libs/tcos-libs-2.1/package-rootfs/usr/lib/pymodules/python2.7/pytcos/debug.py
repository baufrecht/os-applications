# First import the embed function
from IPython.terminal.embed import InteractiveShellEmbed

# Now create the IPython shell instance. 
ipshell = InteractiveShellEmbed(config=cfg, banner1=banner_msg, exit_msg=exit_msg)

# Wrap it in a function that gives me more context:
def ipsh():
    # frameinfo = getframeinfo(currentframe())
    # msg = 'Stopped at: ' + frameinfo.filename + ' ' +  str(frameinfo.lineno)
    if DEBUG == True:
        frame = inspect.currentframe().f_back
        msg = 'Stopped at {0.f_code.co_filename} at line {0.f_lineno}'.format(frame)

        # Go back one level! 
        # This is needed because the call to ipshell is inside the function ipsh()
        ipshell(msg,stack_depth=2)
