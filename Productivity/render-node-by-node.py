# renders all selected Write nodes one by one, based in their first/last frame limits

# set proxy format to enabled/disable
nuke.root()['proxy'].setValue(False)

# sort by render order
nodes = nuke.selectedNodes('Write')
nodes.sort(key=lambda x: x['render_order'].value())

# render!
c = len(nodes)
for i, node in enumerate(nodes):
    print "\nRendering " + str(i+1) + "/" + str(c) + " (" + node['file'].value() + ")"
    nuke.execute(node, int(node['first'].value()), int(node['last'].value()))
    print "...Done!"
    
