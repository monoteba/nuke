def sequence():    
    # get input values
    writeNodes = nuke.selectedNodes('Write')
    writeNodes.sort(key=lambda x: x.name())

    l = len(writeNodes)
    name = writeNodes[0]['name'].value()
    filePath = "L:/VR/OUTPUT/CLIPS_FOR_SOUND/LS/" + name.split('_')[0] + ".mp4"
    
    
    if l <= 0:
        return

    oFirst = int(writeNodes[0]['first'].value())
    oLast = int(writeNodes[l-1]['last'].value())
    
    clips = []
    xp = 0
    yp = 0

    # create time clips 
    for i, node in enumerate(writeNodes):
        node['selected'].setValue(False)
        x = node['xpos'].value() + 200
        y = node['ypos'].value()

        clip = nuke.createNode('TimeClip')
        clip.setName("clip_" + node.name())
        clip['xpos'].setValue(x)
        clip['ypos'].setValue(y)

        first = int(node['first'].value())
        last = int(node['last'].value())
        
        clip['first'].setValue(first)
        clip['last'].setValue(last)
        clip['origfirst'].setValue(oFirst)
        clip['origlast'].setValue(oLast)
        
        clip.setInput(0, node)
        clips.append(clip)
        if (i == l - 1):
            xp = x
            yp = y + 50
    
    # append time clips
    app = nuke.createNode('AppendClip')
    app['xpos'].setValue(xp)
    app['ypos'].setValue(yp)

    for i, clip in enumerate(clips):
        clip['selected'].setValue(False)
        app.setInput(i, clip)

    app['selected'].setValue(True)
    
    # create write node and set input to append node
    write = nuke.createNode('Write', 'tile_color 4278190335 postage_stamp True')
    write.setInput(0, app)
    write['file'].setValue(filePath)
    write['colorspace'].setValue('Gamma2.2')
    write['meta_codec'].setValue('avc1') # H.264
    write['first'].setValue(oFirst)
    write['last'].setValue(oLast)
    write['use_limit'].setValue(True)
    write['xpos'].setValue(xp)
    write['ypos'].setValue(yp + 200)


sequence()
