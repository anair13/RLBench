from typing import List
import numpy as np
from pyrep.objects.shape import Shape
from pyrep.objects.joint import Joint
from pyrep.objects.proximity_sensor import ProximitySensor
from rlbench.backend.task import Task
from rlbench.backend.conditions import DetectedCondition, NothingGrasped
from rlbench.backend.conditions import JointCondition


class OpenWineBottle(Task):

    def init_task(self) -> None:
        bottle_detector = ProximitySensor("bottle_detector")
        cap_detector = ProximitySensor("cap_detector")
        bottle = Shape('bottle')
        self.joint = Joint('joint')
        self.cap = Shape('cap')
        self.register_success_conditions(
            [DetectedCondition(bottle, bottle_detector),
             DetectedCondition(self.cap, cap_detector, negated=True),
             NothingGrasped(self.robot.gripper)])
        self.cap_turned_condition = JointCondition(
            self.joint, np.deg2rad(150))

    def init_episode(self, index: int) -> List[str]:
        self.cap_turned = False
        return ['open wine bottle',
                'screw open the wine bottle',
                'unscrew the bottle cap then remove it from the wine bottle']

    def variation_count(self) -> int:
        return 1

    def step(self) -> None:
        if not self.cap_turned:
            self.cap_turned = self.cap_turned_condition.condition_met()[0]
            if self.cap_turned:
                self.cap.set_parent(self.joint)
