def sequence():    
    writeNodes = nuke.selectedNodes('Write')
    writeNodes.sort(key=lambda x: x.name())

    l = len(writeNodes)
    
    if l <= 0:
        return

    oFirst = int(writeNodes[0]['first'].value())
    oLast = int(writeNodes[l-1]['last'].value())
    
    clips = []

    for i, node in enumerate(writeNodes):
        node['selected'].setValue(False)

        clip = nuke.createNode('TimeClip')
        clip.setName("clip_" + node.name())

        first = int(node['first'].value())
        last = int(node['last'].value())
        
        clip['first'].setValue(first)
        clip['last'].setValue(last)
        clip['origfirst'].setValue(oFirst)
        clip['origlast'].setValue(oLast)
        
        clip.setInput(0, node)
        clips.append(clip)

    app = nuke.createNode('AppendClip')    

    for i, clip in enumerate(clips):
        clip['selected'].setValue(False)
        app.setInput(i, clip)

    app['selected'].setValue(True)
    write = nuke.createNode('Write')
    write.setInput(0, app)


sequence()
