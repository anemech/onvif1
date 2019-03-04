from onvif import ONVIFCamera
from time import sleep

class ptzcam():
    def __init__(self):
        print 'IP camera initialization'
        self.mycam = ONVIFCamera('192.168.15.42', 80, 'admin', 'Supervisor')
        print 'Connected to ONVIF camera'
        # Create media service object
        self.media = self.mycam.create_media_service()
        print 'Created media service object'
        print
        # Get target profile
        self.media_profile = self.media.GetProfiles()[0]
        token = self.media_profile._token

    #PTZ controls  -------------------------------------------------------------
        print
        # Create ptz service object
        print 'Creating PTZ object'
        self.ptz = self.mycam.create_ptz_service()
        print 'Created PTZ service object'
        print

        #Get available PTZ services
        request = self.ptz.create_type('GetServiceCapabilities')
        Service_Capabilities = self.ptz.GetServiceCapabilities(request)
        print 'PTZ service capabilities:'
        print Service_Capabilities
        print

        #Get PTZ status
        status = self.ptz.GetStatus({'ProfileToken':token})
        print 'PTZ status:'
        print status
        print 'Pan position:', status.Position.PanTilt._x
        print 'Tilt position:', status.Position.PanTilt._y
        print 'Zoom position:', status.Position.Zoom._x
        print

        # Get PTZ configuration options for getting option ranges
        request = self.ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = self.media_profile.PTZConfiguration._token
        ptz_configuration_options = self.ptz.GetConfigurationOptions(request)
        print 'PTZ configuration options:'
        print ptz_configuration_options
        print

        self.requestc = self.ptz.create_type('ContinuousMove')
        self.requestc.ProfileToken = self.media_profile._token

        self.requesta = self.ptz.create_type('AbsoluteMove')
        self.requesta.ProfileToken = self.media_profile._token
        print 'Absolute move options'
        print self.requesta
        print

        self.requestr = self.ptz.create_type('RelativeMove')
        self.requestr.ProfileToken = self.media_profile._token
        print 'Relative move options'
        print self.requestr
        print

        self.requests = self.ptz.create_type('Stop')
        self.requests.ProfileToken = self.media_profile._token

        print 'Initial PTZ stop'
        print
        self.stop()

#Stop pan, tilt and zoom
    def stop(self):
        self.requests.PanTilt = True
        self.requests.Zoom = True
        print
        self.ptz.Stop(self.requests)
        print 'Stopped'

#Continuous move functions
    def perform_move(self, timeout):
        # Start continuous move
        ret = self.ptz.ContinuousMove(self.requestc)
        print 'Continuous move completed'
        # Wait a certain time
        sleep(timeout)
        # Stop continuous move
        self.stop()
        sleep(10)
        print

    def move_tilt(self, velocity, timeout):
        print 'Move tilt...', velocity
        self.requestc.Velocity.PanTilt._x = 0.0
        self.requestc.Velocity.PanTilt._y = velocity
        self.perform_move(timeout)

    def move_pan(self, velocity, timeout):
        print 'Move pan...', velocity
        self.requestc.Velocity.PanTilt._x = velocity
        self.requestc.Velocity.PanTilt._y = 0.0
        self.perform_move(timeout)

    def zoom(self, velocity, timeout):
        print 'Zoom...', velocity
        self.requestc.Velocity.Zoom._x = velocity
        self.perform_move(timeout)
		
    def move_abspantilt(self, pan, tilt, velocity):
        self.requesta.Position.PanTilt._x = pan
        self.requesta.Position.PanTilt._y = tilt
        self.requesta.Speed.PanTilt._x = velocity
        self.requesta.Speed.PanTilt._y = velocity
        print 'Absolute move to:', self.requesta.Position
        print 'Absolute speed:',self.requesta.Speed
        ret = self.ptz.AbsoluteMove(self.requesta)
        print 'Absolute move pan-tilt requested:', pan, tilt, velocity
        sleep(2.0)
        print 'Absolute move completed'

        print