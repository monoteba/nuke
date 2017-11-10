# renders all selected Write nodes one by one, sorted by render order and using first/last frame of the write node to determine the range to render.

def renderSelected():
    nodes = nuke.selectedNodes('Write')

    # sort by render order
    nodes.sort(key=lambda x: x['render_order'].value())

    # disable proxy
    proxy = nuke.root()['proxy'].value()
    nuke.root()['proxy'].setValue(False)

    # empty tuple for storing frame start/end/incr
    t = ()  # only used in executeMultiple()

    # render!
    c = len(nodes)
    for i, node in enumerate(nodes):
        f = int(node['first'].value())
        l = int(node['last'].value())
        
        # execute node
        nuke.execute(node, f, l, 1)
        print("\n%d of %d, %s is done" % (i+1, c, node.name()))
        
        t = t + ((f, l, 1),)  # only used in executeMultiple()

    # execute multiple write nodes (writeNodes, ranges)
    # nuke.executeMultiple(tuple, tuple(tuple, tuple, tuple,))
    #nuke.executeMultiple(nodes, t)

    # set proxy back to original value
    nuke.root()['proxy'].setValue(proxy)

renderSelected()
