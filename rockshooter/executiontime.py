class ExecutionTime:

	""" This class is used as a decorator.
		Frames here means that, the methods decorates with ExecutionTime decorator
		will be executed after the number of frames passed is equal zero.
		This is used like a timer!
	"""

	def __init__(self, frames):
		self.frames = frames 
		self.framesCountDown = frames

	def __call__(self, function):
		def decorator(*args, **kwargs):
			if (self.framesCountDown == 0):
				self.framesCountDown = self.frames
				function(*args, **kwargs)
			else:
				self.framesCountDown = self.framesCountDown - 1
		return decorator

