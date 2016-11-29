for node in nuke.selectedNodes("Tracker4"):
    print node.name() + ' preview disabled.'
    node["zoom_window_behaviour"].setValue(4)
    node["zoom_window_filter_behaviour"].setValue(2)
    node["keyframe_display"].setValue(3)
