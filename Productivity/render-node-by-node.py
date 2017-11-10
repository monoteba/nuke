# renders all selected Write nodes one by one, based in their first/last frame limits

def renderSelected():
    nodes = nuke.selectedNodes('Write')

    # sort by render order
    nodes.sort(key=lambda x: x['render_order'].value())

    # disable proxy
    proxy = nuke.root()['proxy'].value()
    nuke.root()['proxy'].setValue(False)

    # empty tuple for storing frame start/end/incr
    t = ()

    # render!
    c = len(nodes)
    for i, node in enumerate(nodes):
        f = int(node['first'].value())
        l = int(node['last'].value())
        nuke.execute(node, f, l, 1)
        print("%d of %d, %s is done" % (i, c, node.name()))
        t = t + ((f, l, 1),)

    # execute multiple write nodes (writeNodes, ranges)
    # nuke.executeMultiple(tuple, tuple(tuple, tuple, tuple,))
    #nuke.executeMultiple(nodes, t)

    # set proxy back to original value
    nuke.root()['proxy'].setValue(proxy)

renderSelected()

