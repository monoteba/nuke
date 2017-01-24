# renders all selected Write nodes one by one, based in their first/last frame limits
for node in nuke.selectedNodes('Write'):
    print "\nRendering " + node['file'].value()
    if nuke.execute(node, int(node['first'].value()), int(node['last'].value())):
        print "CANCEL!"
        break
    print "...Done!"
