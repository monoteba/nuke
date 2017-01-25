# renders all selected Write nodes one by one, based in their first/last frame limits

# set proxy format to enabled/disable
nuke.root()['proxy'].setValue(False)

# sort by render order
nodes = nuke.selectedNodes('Write')
nodes.sort(key=lambda x: x['render_order'].value())

# render!
for node in nodes:
    print "\nRendering " + node['file'].value()
    nuke.execute(node, int(node['first'].value()), int(node['last'].value()))
    print "...Done!"

    
