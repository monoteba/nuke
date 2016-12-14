# Offset selected Write nodes first and last value

offset = 1

for node in nuke.selectedNodes('Write'):
    node['first'].setValue(int(node['first'].value()) + offset)
    node['last'].setValue(int(node['last'].value()) + offset)
