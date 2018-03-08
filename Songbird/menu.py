import sequence

m = nuke.menu("Nuke")
m.addCommand('Songbird/Export Selected', lambda: export.export_selected() )