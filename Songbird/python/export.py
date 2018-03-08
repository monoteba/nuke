import nuke
import os

def export_selected():
    write_nodes = nuke.selectedNodes("Write")
    write_nodes.sort(key=lambda x: x["file"].value())

    # disable proxy
    proxy = nuke.root()["proxy"].value()
    nuke.root()["proxy"].setValue(False)

    for node in write_nodes:
        export_node(node)

    # set proxy back to original value
    nuke.root()["proxy"].setValue(proxy)


def export_node(node):
    file_path = node["file"].value()
    dir_name = os.path.dirname(file_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # find read node
    read_node = node.input(0)
    while (not read_node.Class() == "Read"):
        read_node = read_node.input(0)
        if not read_node:
            read_node = None
            break

    if not read_node:
        return

    first_frame = read_node["first"].value()
    last_frame = read_node["last"].value()

    # render!
    nuke.execute(node, first_frame, last_frame)

    # find tracker node
    tracker_node = node.input(0)
    while (not tracker_node.Class() == "Tracker4"):
        tracker_node = tracker_node.input(0)
        if not tracker_node:
            tracker_node = None
            break

    if not tracker_node:
        return

    # get anim curves
    anim_tx = tracker_node["translate"].animation(0)
    anim_ty = tracker_node["translate"].animation(1)

    # export x curve
    if not anim_tx.constant():
        with open(dir_name + "/move_x.txt", "w") as x_file:
            for f in range(first_frame, last_frame + 1):
                x_file.write("%.7f\n" % anim_tx.evaluate(f))

    # export y curve
    if not anim_ty.constant():
        with open(dir_name + "/move_y.txt", "w") as y_file:
            for f in range(first_frame, last_frame + 1):
                y_file.write("%.7f\n" % anim_ty.evaluate(f))