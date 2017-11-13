import time
import nuke

class RenderNodesBackgroundSequentially:
	def __init__(self):
		self.path = '/Applications/Nuke11.0v2/NukeX11.0v2 Non-commercial.app'  # nuke.EXE_PATH
		self.nodes = None
		self.pids = {}
		self.pids_done = {}
		self.pids_time = {}
		self.proxy = None
		self.concurrent_jobs = 2
		self.daemon = True

	def after_render(self, context=None):
		pid = context['id']
		
		# if stopped prematurely
		if not self.pids_done[pid]:
			print 'Cancelled %d, stopping all queued!' % (pid)
			del self.pids[pid]
			del self.pids_done[pid]
			self.nodes = None
			
			if not self.pids:
				self.remove_callbacks()
				
			return
		
		name = self.pids[pid]
		t  = time.time() - self.pids_time[pid]
		print 'Done rendering: %s, pid: %d, time: %.2f sec' % (name, pid, t)
		
		del self.pids[pid]
		del self.pids_done[pid]
		
		# render next
		if self.nodes and len(self.pids) < self.concurrent_jobs:
			self.render_next()
		elif not self.pids:
    		self.remove_callbacks()
    		
    def after_frame(self, context=None):
    	if context['frameProgress'] == context['numFrames']:
    		self.pids_done[context['id']] = True
		
		
	def render_next(self):
		if not self.nodes:
			return
		
		node = self.nodes[0]
		del self.nodes[0]  # it's taken, so remove it
		
		f = int(node['first'].value())
		l = int(node['last'].value())
		ranges = nuke.FrameRanges()
		ranges.add(nuke.FrameRange('%d-%d' % (f,l)))
		
		pid = nuke.executeBackgroundNuke(self.path, [node], ranges, ['main'], {})
		self.pids[pid] = node.name()
		self.pids_done[pid] = False
		self.pids_time[pid] = time.time()
		
		print 'Started rendering: %s, pid: %d' % (node.name(), pid)
	
	def start_render(self):
		print '\n'
		
		# get and sort selected write nodes
		self.nodes = nuke.selectedNodes('Write')
		self.nodes.sort(key=lambda x: x['render_order'].value())
		
		# disable proxy
		self.proxy = nuke.root()['proxy'].value()
    	nuke.root()['proxy'].setValue(False)
    	
    	nuke.addAfterBackgroundRender(self.after_render)
    	nuke.addAfterBackgroundFrameRender(self.after_frame)
    	nuke.addOnScriptClose(self.remove_callbacks)
    	
    	# start x number of background processes
    	for i in range(min(self.concurrent_jobs, len(self.nodes))):
    		self.render_next()
    
    def remove_callbacks(self):
    	nuke.root()['proxy'].setValue(self.proxy)
    	nuke.removeAfterBackgroundRender(self.after_render)
    	nuke.removeAfterBackgroundFrameRender(self.after_frame)
    	nuke.removeOnScriptClose(self.remove_callbacks)

    		
render_node = RenderNodesBackgroundSequentially()
render_node.start_render()
