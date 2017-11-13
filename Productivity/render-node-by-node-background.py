# renders all selected Write nodes one by one, based in their first/last frame limits
def renderSelected():
    nodes = nuke.selectedNodes('Write')

    # sort by render order
    nodes.sort(key=lambda x: x['render_order'].value())

    # disable proxy
    proxy = nuke.root()['proxy'].value()
    nuke.root()['proxy'].setValue(False)

    # render!
    ranges1 = nuke.FrameRanges()
    ranges2 = nuke.FrameRanges()
    nodes1 = []
    nodes2 = []
    c = len(nodes)

    for i, node in enumerate(nodes):
        f = int(node['first'].value())
        l = int(node['last'].value())
        range = nuke.FrameRange('%d-%d' % (f,l))
        if i % 2 == 0:
            ranges1.add(range)
            nodes1.append(node)
        else:
            ranges2.add(range)
            nodes2.append(node)
    
    path = '/Applications/Nuke11.0v2/NukeX11.0v2 Non-commercial.app'
    nuke.executeBackgroundNuke(path, nodes1, ranges1, ['main'], {})
    nuke.executeBackgroundNuke(path, nodes2, ranges2, ['main'], {})
    
    # set proxy back to original value
    nuke.root()['proxy'].setValue(proxy)

renderSelected()
