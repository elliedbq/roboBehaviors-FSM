from setuptools import find_packages, setup

package_name = 'ros_behavior_fsm'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ellie',
    maintainer_email='ellie@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'collision_avoidance = ros_behavior_fsm.collision_avoidance:main',
            'go_straight = ros_behavior_fsm.go_straight:main',
            'wall_follower = ros_behavior_fsm.wall_follower:main'
        ],
    },
)
