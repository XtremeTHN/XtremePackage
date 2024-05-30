from modules.arguments import ParseArgs, InstallArguments

def introspect(object_):
    for x in dir(object_):
        if x.startswith("__"):
            continue
        
        attr = getattr(object_, x)
        print(x, attr)

res = ParseArgs()

introspect(res)
introspect(res.install)