import numpy as np
import pyglet
import pymunk
import pymunk.pyglet_util
from pymunk.vec2d import Vec2d
from enum import IntEnum


DISPAY_MARGIN = 10
ARENA_SIZE = 600

window = pyglet.window.Window(ARENA_SIZE+DISPAY_MARGIN*2, ARENA_SIZE+DISPAY_MARGIN*2, vsync=False)
space = pymunk.Space()
draw_options = pymunk.pyglet_util.DrawOptions()
running = True


class TwoWheelVehicleRobotSimulator(object):
    COLLISION_TYPE = IntEnum("COLLISION_TYPE", "OBJECT VEHICLE LEFT_SENSOR RIGHT_SENSOR FEED")

    # simulation setting parameters
    VEHICLE_RADIUS = 20
    SENSOR_ANGLE = np.pi * 45 / 180
    SENSOR_RANGE = 80
    SENSOR_NOISE = 0
    MOTOR_NOISE = 1.0
    FEED_COLOR = (0, 0, 0)
    FEED_ACTIVE_COLOR = (255, 0, 0)
    FEED_EATING_TIME = 100

    def __init__(self, controll_func, obstacle_num=5, obstacle_radius=30, feed_num=0, feed_radius=5):
        super(TwoWheelVehicleRobotSimulator, self).__init__()
        self.__controll_func = controll_func
        self.__left_sensor_val = 0
        self.__right_sensor_val = 0
        self.__feed_sensor_val = False
        self.__feed_touch_counter = {}

        space.gravity = 0, 0

        # arena
        walls = [pymunk.Segment(space.static_body, (DISPAY_MARGIN, DISPAY_MARGIN), (ARENA_SIZE+DISPAY_MARGIN, DISPAY_MARGIN), 0),
                 pymunk.Segment(space.static_body, (ARENA_SIZE+DISPAY_MARGIN, DISPAY_MARGIN), (ARENA_SIZE+DISPAY_MARGIN, ARENA_SIZE+DISPAY_MARGIN), 0),
                 pymunk.Segment(space.static_body, (ARENA_SIZE+DISPAY_MARGIN, ARENA_SIZE+DISPAY_MARGIN), (DISPAY_MARGIN, ARENA_SIZE+DISPAY_MARGIN), 0),
                 pymunk.Segment(space.static_body, (DISPAY_MARGIN, ARENA_SIZE+DISPAY_MARGIN), (DISPAY_MARGIN, DISPAY_MARGIN), 0)]
        for w in walls:
            w.collision_type = self.COLLISION_TYPE.OBJECT
            w.friction = 0.2
        space.add(walls)

        # vehicle
        mass = 1
        self.vehicle_body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, self.VEHICLE_RADIUS))
        self.vehicle_body.position = ARENA_SIZE/2+DISPAY_MARGIN, ARENA_SIZE/2+DISPAY_MARGIN
        vehicle_s = pymunk.Circle(self.vehicle_body, self.VEHICLE_RADIUS)
        vehicle_s.friction = 0.2
        vehicle_s.collision_type = self.COLLISION_TYPE.VEHICLE
        space.add(self.vehicle_body, vehicle_s)

        # left sensor
        sensor_l_s = pymunk.Segment(self.vehicle_body, (0, 0), (self.SENSOR_RANGE * np.cos(self.SENSOR_ANGLE), self.SENSOR_RANGE * np.sin(self.SENSOR_ANGLE)), 0)
        sensor_l_s.sensor = True
        sensor_l_s.collision_type = self.COLLISION_TYPE.LEFT_SENSOR
        handler_l = space.add_collision_handler(self.COLLISION_TYPE.LEFT_SENSOR, self.COLLISION_TYPE.OBJECT)
        handler_l.pre_solve = self.__left_sensr_handler
        handler_l.separate = self.__left_sensr_separate_handler
        space.add(sensor_l_s)

        # right sensor
        sensor_r_s = pymunk.Segment(self.vehicle_body, (0, 0), (self.SENSOR_RANGE * np.cos(-self.SENSOR_ANGLE), self.SENSOR_RANGE * np.sin(-self.SENSOR_ANGLE)), 0)
        sensor_r_s.sensor = True
        sensor_r_s.collision_type = self.COLLISION_TYPE.RIGHT_SENSOR
        handler_r = space.add_collision_handler(self.COLLISION_TYPE.RIGHT_SENSOR, self.COLLISION_TYPE.OBJECT)
        handler_r.pre_solve = self.__right_sensr_handler
        handler_r.separate = self.__right_sensr_separate_handler
        space.add(sensor_r_s)

        # obstacles
        OBSTACLE_RADIUS = 30
        for a in (np.linspace(0, np.pi*2, obstacle_num, endpoint=False) + np.pi/2):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = (DISPAY_MARGIN+ARENA_SIZE/2+ARENA_SIZE*0.3*np.cos(a), DISPAY_MARGIN+ARENA_SIZE/2+ARENA_SIZE*0.3*np.sin(a))
            shape = pymunk.Circle(body, obstacle_radius)
            shape.friction = 0.2
            shape.collision_type = self.COLLISION_TYPE.OBJECT
            space.add(shape)

        for i in range(feed_num):
            body = pymunk.Body(1, 1)
            body.position = DISPAY_MARGIN + feed_radius + np.random.rand(2) * (ARENA_SIZE - feed_radius*2)
            shape = pymunk.Circle(body, feed_radius)
            shape.sensor = True
            shape.color = self.FEED_COLOR
            shape.collision_type = self.COLLISION_TYPE.FEED
            handler = space.add_collision_handler(self.COLLISION_TYPE.VEHICLE, self.COLLISION_TYPE.FEED)
            handler.pre_solve = self.__feed_touch_handler
            handler.separate = self.__feed_separate_handler
            space.add(body, shape)
            self.__feed_touch_counter[shape] = 0


    def run(self):
        print()
        print("[space] start/pause")
        pyglet.clock.schedule_interval(self.__update, 1/60)
        pyglet.app.run()


    def __update(self, dt):
        if not running:
            return
        self.vehicle_body.velocity = (0, 0)
        self.vehicle_body.angular_velocity = 0
        if self.__controll_func is not None:
            sensor_data = {
                "left_distance": self.__left_sensor_val,
                "right_distance": self.__right_sensor_val,
                "feed_touching": self.__feed_sensor_val
            }
            #velocity_l, velocity_r = self.__controll_func(self.__left_sensor_val, self.__right_sensor_val)
            velocity_l, velocity_r = self.__controll_func(sensor_data)
            velocity_l += self.MOTOR_NOISE * np.random.randn()
            velocity_r += self.MOTOR_NOISE * np.random.randn()
            self.vehicle_body.apply_impulse_at_local_point((velocity_l*self.vehicle_body.mass, 0), (0, self.VEHICLE_RADIUS))
            self.vehicle_body.apply_impulse_at_local_point((velocity_r*self.vehicle_body.mass, 0), (0, -self.VEHICLE_RADIUS))
        lf = self.__get_lateral_velocity() * self.vehicle_body.mass
        self.vehicle_body.apply_impulse_at_local_point(-lf)
        space.step(1/60)


    def __feed_touch_handler(self, arbiter, space, data):
        feed = arbiter.shapes[1]
        feed.color = self.FEED_ACTIVE_COLOR
        self.__feed_touch_counter[feed] += 1
        self.__feed_sensor_val = True
        if (self.__feed_touch_counter[feed] > self.FEED_EATING_TIME):
            feed.body.position = DISPAY_MARGIN + feed.radius/2 + np.random.rand(2) * (ARENA_SIZE - feed.radius)
        return True


    def __feed_separate_handler(self, arbiter, space, data):
        feed = arbiter.shapes[1]
        feed.color = self.FEED_COLOR
        self.__feed_touch_counter[feed] = 0
        self.__feed_sensor_val = False
        return True


    def __left_sensr_handler(self, arbiter, space, data):
        p = arbiter.contact_point_set.points[0]
        distance = self.vehicle_body.world_to_local(p.point_b).get_length()
        self.__left_sensor_val = 1 - distance / self.SENSOR_RANGE
        self.__left_sensor_val += self.SENSOR_NOISE * np.random.randn()
        return True


    def __left_sensr_separate_handler(self, arbiter, space, data):
        self.__left_sensor_val = 0
        return True


    def __right_sensr_handler(self, arbiter, space, data):
        p = arbiter.contact_point_set.points[0]
        distance = self.vehicle_body.world_to_local(p.point_b).get_length()
        self.__right_sensor_val = 1 - distance / self.SENSOR_RANGE
        self.__right_sensor_val += self.SENSOR_NOISE * np.random.randn()
        return True


    def __right_sensr_separate_handler(self, arbiter, space, data):
        self.__right_sensor_val = 0
        return True


    def __get_lateral_velocity(self):
        v = self.vehicle_body.world_to_local(self.vehicle_body.velocity + self.vehicle_body.position)
        rn = Vec2d(0, -1)
        return v.dot(rn) * rn


@window.event
def on_draw():
    pyglet.gl.glClearColor(255,255,255,255)
    window.clear()
    space.debug_draw(draw_options)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        global running
        running = not running
