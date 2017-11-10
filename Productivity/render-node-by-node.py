# renders all selected Write nodes one by one, based in their first/last frame limits
import time


def renderSelected():
    nodes = nuke.selectedNodes('Write')

    # sort by render order
    nodes.sort(key=lambda x: x.name())

    # disable proxy
    proxy = nuke.root()['proxy'].value()
    nuke.root()['proxy'].setValue(False)

    # render!
    c = len(nodes)
    print('\nRender %d nodes' % (c))
    for i, node in enumerate(nodes):
        t = time.time()
        f = int(node['first'].value())
        l = int(node['last'].value())
        nuke.execute(node, f, l)
        lapse = time.time() - t
        print('%d/%d: %s rendered in %.2f seconds' % (i+1, c, node.name(), lapse))


    # set proxy back to original value
    nuke.root()['proxy'].setValue(proxy)

renderSelected()
