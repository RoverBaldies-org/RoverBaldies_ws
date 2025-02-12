import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Get package directories
    baldybot_description_share = get_package_share_directory('baldybot_description')
    gazebo_ros_share = get_package_share_directory('gazebo_ros')

    # Define the file paths
    urdf_path = os.path.join(baldybot_description_share, 'urdf', 'baldybot.urdf.xacro')
    rviz_config_path = os.path.join(baldybot_description_share, 'rviz', 'urdf_config.rviz')
    gazebo_launch_file = os.path.join(gazebo_ros_share, 'launch', 'gazebo.launch.py')

    # Node to publish the robot state using the URDF processed by xacro
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_path])
        }],
    )

    # Include the Gazebo launch file
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file)
    )

    # Node to spawn the robot entity in Gazebo using the robot_description topic
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=['-topic', 'robot_description', '-entity', 'baldybot']
    )

    # Node to launch RViz2 with the specified configuration
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]
    )

    # Create and return the LaunchDescription object with all nodes/actions
    return LaunchDescription([
        robot_state_publisher_node,
        gazebo_launch,
        spawn_entity,
        rviz2_node,
    ])
