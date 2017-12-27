import numpy as np
import pyglet
import pymunk
import pymunk.pyglet_util
from pymunk.vec2d import Vec2d
import ipdb

feed_touch_counter = {}

DISPAY_MARGIN = 10
arena_size = 600
vehicle_radius = 20

COLLISION_TYPE_OBJECT = 1
COLLISION_TYPE_VEHICLE = 2
COLLISION_TYPE_LEFT_SENSOR = 3
COLLISION_TYPE_RIGHT_SENSOR = 4
COLLISION_TYPE_FEED = 5

SENSOR_ANGLE = np.pi * 45 / 180
SENSOR_RANGE = 80

running = True

SENSOR_NOISE = 0
MOTOR_NOISE = 1.0

FEED_COLOR = (0, 0, 0)
FEED_ACTIVE_COLOR = (255, 0, 0)

FEED_EATING_TIME = 100

class TwoWheelVehicleRobotSimulator(object):
    def __init__(self, controll_func, obstacle_num=5, obstacle_radius=30, feed_num=0, feed_radius=5):
        super(TwoWheelVehicleRobotSimulator, self).__init__()
        self.controll_func = controll_func
        self.left_sensor_val = 0
        self.right_sensor_val = 0
        self.feed_sensor_val = False

        space.gravity = 0, 0

        # arena
        walls = [pymunk.Segment(space.static_body, (DISPAY_MARGIN, DISPAY_MARGIN), (arena_size+DISPAY_MARGIN, DISPAY_MARGIN), 0),
                 pymunk.Segment(space.static_body, (arena_size+DISPAY_MARGIN, DISPAY_MARGIN), (arena_size+DISPAY_MARGIN, arena_size+DISPAY_MARGIN), 0),
                 pymunk.Segment(space.static_body, (arena_size+DISPAY_MARGIN, arena_size+DISPAY_MARGIN), (DISPAY_MARGIN, arena_size+DISPAY_MARGIN), 0),
                 pymunk.Segment(space.static_body, (DISPAY_MARGIN, arena_size+DISPAY_MARGIN), (DISPAY_MARGIN, DISPAY_MARGIN), 0)]
        for w in walls:
            w.collision_type = COLLISION_TYPE_OBJECT
            w.friction = 0.2
        space.add(walls)

        # vehicle
        mass = 1
        self.vehicle_body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, vehicle_radius))
        self.vehicle_body.position = arena_size/2+DISPAY_MARGIN, arena_size/2+DISPAY_MARGIN
        vehicle_s = pymunk.Circle(self.vehicle_body, vehicle_radius)
        vehicle_s.friction = 0.2
        vehicle_s.collision_type = COLLISION_TYPE_VEHICLE
        space.add(self.vehicle_body, vehicle_s)

        # left sensor
        sensor_l_s = pymunk.Segment(self.vehicle_body, (0, 0), (SENSOR_RANGE * np.cos(SENSOR_ANGLE), SENSOR_RANGE * np.sin(SENSOR_ANGLE)), 0)
        sensor_l_s.sensor = True
        sensor_l_s.collision_type = COLLISION_TYPE_LEFT_SENSOR
        handler_l = space.add_collision_handler(COLLISION_TYPE_LEFT_SENSOR, COLLISION_TYPE_OBJECT)
        handler_l.pre_solve = self.left_sensr_handler
        handler_l.separate = self.left_sensr_separate_handler
        space.add(sensor_l_s)

        # right sensor
        sensor_r_s = pymunk.Segment(self.vehicle_body, (0, 0), (SENSOR_RANGE * np.cos(-SENSOR_ANGLE), SENSOR_RANGE * np.sin(-SENSOR_ANGLE)), 0)
        sensor_r_s.sensor = True
        sensor_r_s.collision_type = COLLISION_TYPE_RIGHT_SENSOR
        handler_r = space.add_collision_handler(COLLISION_TYPE_RIGHT_SENSOR, COLLISION_TYPE_OBJECT)
        handler_r.pre_solve = self.right_sensr_handler
        handler_r.separate = self.right_sensr_separate_handler
        space.add(sensor_r_s)

        # obstacles
        OBSTACLE_RADIUS = 30
        for a in (np.linspace(0, np.pi*2, obstacle_num, endpoint=False) + np.pi/2):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = (DISPAY_MARGIN+arena_size/2+arena_size*0.3*np.cos(a), DISPAY_MARGIN+arena_size/2+arena_size*0.3*np.sin(a))
            shape = pymunk.Circle(body, obstacle_radius)
            shape.friction = 0.2
            shape.collision_type = COLLISION_TYPE_OBJECT
            space.add(shape)

        for i in range(feed_num):
            body = pymunk.Body(1, 1)
            body.position = DISPAY_MARGIN + feed_radius + np.random.rand(2) * (arena_size - feed_radius*2)
            shape = pymunk.Circle(body, feed_radius)
            shape.sensor = True
            shape.color = FEED_COLOR
            shape.collision_type = COLLISION_TYPE_FEED
            handler = space.add_collision_handler(COLLISION_TYPE_VEHICLE, COLLISION_TYPE_FEED)
            handler.pre_solve = self.feed_touch_handler
            handler.separate = self.feed_separate_handler
            space.add(body, shape)

            feed_touch_counter[shape] = 0


    def run(self):
        pyglet.clock.schedule_interval(self.__update, 1/60)
        pyglet.app.run()

    def __update(self, dt):
        if not running:
            return
        self.vehicle_body.velocity = (0, 0)
        self.vehicle_body.angular_velocity = 0
        if self.controll_func is not None:
            sensor_data = {
                "left_touch": self.left_sensor_val,
                "right_touch": self.right_sensor_val,
                "feed_touching": self.feed_sensor_val
            }
            #velocity_l, velocity_r = self.controll_func(self.left_sensor_val, self.right_sensor_val)
            velocity_l, velocity_r = self.controll_func(sensor_data)
            velocity_l += MOTOR_NOISE * np.random.randn()
            velocity_r += MOTOR_NOISE * np.random.randn()
            self.vehicle_body.apply_impulse_at_local_point((velocity_l*self.vehicle_body.mass, 0), (0, vehicle_radius))
            self.vehicle_body.apply_impulse_at_local_point((velocity_r*self.vehicle_body.mass, 0), (0, -vehicle_radius))
        lf = self.get_lateral_velocity() * self.vehicle_body.mass
        self.vehicle_body.apply_impulse_at_local_point(-lf)
        space.step(1/60)

    def feed_touch_handler(self, arbiter, space, data):
        feed = arbiter.shapes[1]
        feed.color = FEED_ACTIVE_COLOR
        feed_touch_counter[feed] += 1
        self.feed_sensor_val = True
        if (feed_touch_counter[feed] > FEED_EATING_TIME):
            feed.body.position = DISPAY_MARGIN + feed.radius/2 + np.random.rand(2) * (arena_size - feed.radius)
        return True

    def feed_separate_handler(self, arbiter, space, data):
        feed = arbiter.shapes[1]
        feed.color = FEED_COLOR
        feed_touch_counter[feed] = 0
        self.feed_sensor_val = False
        return True

    def left_sensr_handler(self, arbiter, space, data):
        p = arbiter.contact_point_set.points[0]
        distance = self.vehicle_body.world_to_local(p.point_b).get_length()
        self.left_sensor_val = 1 - distance / SENSOR_RANGE
        self.left_sensor_val += SENSOR_NOISE * np.random.randn()
        return True

    def left_sensr_separate_handler(self, arbiter, space, data):
        self.left_sensor_val = 0
        return True

    def right_sensr_handler(self, arbiter, space, data):
        p = arbiter.contact_point_set.points[0]
        distance = self.vehicle_body.world_to_local(p.point_b).get_length()
        self.right_sensor_val = 1 - distance / SENSOR_RANGE
        self.right_sensor_val += SENSOR_NOISE * np.random.randn()
        return True

    def right_sensr_separate_handler(self, arbiter, space, data):
        self.right_sensor_val = 0
        return True

    def get_lateral_velocity(self):
        v = self.vehicle_body.world_to_local(self.vehicle_body.velocity + self.vehicle_body.position)
        rn = Vec2d(0, -1)
        return v.dot(rn) * rn


window = pyglet.window.Window(arena_size+DISPAY_MARGIN*2, arena_size+DISPAY_MARGIN*2, vsync=False)
space = pymunk.Space()
draw_options = pymunk.pyglet_util.DrawOptions()

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
