# renders all selected Write nodes one by one, based in their first/last frame limits

nodes = nuke.selectedNodes('Write')

# sort by render order
nodes.sort(key=lambda x: x['render_order'].value())

# render!
for node in nodes:
    print "\nRendering " + node['file'].value()
    if nuke.execute(node, int(node['first'].value()), int(node['last'].value())):
        print "CANCEL!"
        break
    print "...Done!"

    
