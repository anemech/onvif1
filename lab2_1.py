from onvif import ONVIFCamera
from time import sleep

class CamTest:
	def __init__(self,ip,port,user,passw):
		self.ip = ip
		self.port = port
		self.user = user
		self.passw = passw
		self.cam = ONVIFCamera(self.ip, self.port, self.user, self.passw)
	def Focus(self):
		media = self.cam.create_media_service() 	#creating media service
		profiles = media.GetProfiles() 				#getting profiles' info
		imaging = self.cam.create_imaging_service() #creating imaging service so we can work with focus
		token = profiles[0]._token   	        	#getting token from the first profile
		vs_token = media.GetVideoSources()[0]._token #getting videosources token

		print 'imaging status:'                     
		print imaging.GetStatus({'VideoSourceToken': vs_token}).FocusStatus20.Position #printing Imaging Status
		options = imaging.GetMoveOptions({'VideoSourceToken': vs_token})
		imaging.create_type('Move')					#creating new type of imaging
		#stopping imaging before start to disturb (if it was) previous moving and setting focus to manual
		imaging.Stop({'VideoSourceToken': vs_token})
		focus = imaging.SetImagingSettings({'VideoSourceToken': vs_token, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'MANUAL'}}})
		try:
			options.Continuous
			cont_mov = imaging.Move({'VideoSourceToken': vs_token,'Focus':{'Continuous': {'Speed': +0.5}}})					 
			sleep(2)
			imaging.Stop({'VideoSourceToken': vs_token})
			print 'imaging status(position):'  #getting current position
			print imaging.GetStatus({'VideoSourceToken': vs_token}).FocusStatus20.Position
		except AttributeError:                 #catching error
			print 'Continious Imaging is not supported'	 #setting autofocus mode back
		imaging.SetImagingSettings({'VideoSourceToken': vs_token, 'ImagingSettings': {'Focus': {'AutoFocusMode': 'AUTO'}}})
		return 'Test is done'
		
Inst = CamTest('192.168.15.43', 80, 'admin', 'Supervisor')
print Inst.Focus()