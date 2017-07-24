import my_appapi as appapi
             
class motion_control(appapi.my_appapi):

  def initialize(self):
    # self.LOGLEVEL="DEBUG"
    self.motion_devices= {"sensor.office_sensor_burglar":
                             {"target":"input_boolean.officemotion",
                              "on_value":8,
                              "off_value":0,
                              "delay":300},
                          "sensor.master_burglar":
                             {"target":"input_boolean.mastermotion",
                              "on_value":8,
                              "off_value":0,
                              "delay":300},
                          "sensor.guest_sensor_burglar":
                             {"target":"input_boolean.guestmotion",
                              "on_value":8,
                              "off_value":0,
                              "delay":300},
                          "sensor.downstairs_hallway_sensor_burglar":
                             {"target":"input_boolean.dshallmotion",
                              "on_value":8,
                              "off_value":0,
                              "delay":300},
                          "sensor.den_sensor_burglar":
                             {"target":"input_boolean.denmotion",
                              "on_value":8,
                              "off_value":0,
                              "delay":1800},
                          "binary_sensor.media_room_sensor_sensor":
                             {"target":"input_boolean.mediamotion",
                              "on_value":"on",
                              "off_value":"off",
                              "delay":300},
                          "sensor.upstairs_sensor_burglar":
                             {"target":"input_boolean.upstairsmotion",
                              "on_value":8,
                              "off_value":0,
                              "delay":300}}
  
    self.log("motion_control App")
    for s_motion in self.motion_devices:
      self.log("setting state listener for {}".format(s_motion))
      self.listen_state(self.motion_handler,s_motion)
      self.log("current {} state = {} on_value={}".format(s_motion,self.get_state(s_motion),self.motion_devices[s_motion]["on_value"]))
      if str(self.get_state(s_motion))==str(self.motion_devices[s_motion]["on_value"]):
        self.log("{} already on, setting timeout listener".format(s_motion))
        self.turn_on(self.motion_devices[s_motion]["target"])
        #self.set_state(self.motion_devices[s_motion]["target"],attributes={"entity_picture":"/local/black_ink.png"})
        self.listen_state(self.motion_timeout,s_motion,
                          new=self.motion_devices[s_motion]["off_value"],
                          duration=self.motion_devices[s_motion]["delay"])
      else:
        self.log("{} is off".format(s_motion))
        self.turn_off(self.motion_devices[s_motion]["target"])
        #self.set_state(self.motion_devices[s_motion]["target"],attributes={"entity_picture":"/local/yellow_ink.png"})

        
    
  def motion_handler(self,entity, attribute, old, new, kwargs):
    if new!=old:
      self.log("Motion happened - {} - {}".format(entity,new))
      if str(new)==str(self.motion_devices[entity]["on_value"]):
        self.turn_on(self.motion_devices[entity]["target"])
        self.log("registering delayed state listener for {}".format(entity))
        self.listen_state(self.motion_timeout,entity,
                          new=str(self.motion_devices[entity]["off_value"]),
                          duration=self.motion_devices[entity]["delay"])

  def motion_timeout(self,entity, attribute, old, new, kwargs):
    self.log("timout occurred for {} - {}".format(entity,new))
    if str(new)==str(self.motion_devices[entity]["off_value"]):
      self.log("turning out light {}".format(self.motion_devices[entity]["target"]))
      self.turn_off(self.motion_devices[entity]["target"])

  
