import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import launch

################### user configure parameters for ros2 start ###################
xfer_format   = 0    # 0-Pointcloud2(PointXYZRTL), 1-customized pointcloud format
multi_topic   = 0    # 0-All LiDARs share the same topic, 1-One LiDAR one topic
data_src      = 0    # 0-lidar, others-Invalid data src
publish_freq  = 10.0 # freqency of publish, 5.0, 10.0, 20.0, 50.0, etc.
output_type   = 0
frame_id      = 'livox_frame'
lidar_topic   = 'livox/lidar'
imu_topic     = 'livox/imu'
lvx_file_path = '/home/livox/livox_test.lvx'
cmdline_bd_code = 'livox0000000001'

cur_path = os.path.split(os.path.realpath(__file__))[0] + '/'
cur_config_path = cur_path + '../config'
rviz_config_path = os.path.join(cur_config_path, 'display_point_cloud_ROS2.rviz')
user_config_path = os.path.join(cur_config_path, 'MID360_config.json')
################### user configure parameters for ros2 end #####################


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('publish_freq', default_value=str(publish_freq),
                              description='Frequency of publish (Hz)'),
        DeclareLaunchArgument('frame_id', default_value=frame_id,
                              description='Frame ID for point cloud messages'),
        DeclareLaunchArgument('lidar_topic', default_value=lidar_topic,
                              description='Topic name for lidar point cloud'),
        DeclareLaunchArgument('imu_topic', default_value=imu_topic,
                              description='Topic name for IMU data'),
        DeclareLaunchArgument('xfer_format', default_value=str(xfer_format),
                              description='Transfer format: 0-PointCloud2, 1-Custom'),
        DeclareLaunchArgument('multi_topic', default_value=str(multi_topic),
                              description='Multi topic mode: 0-single topic, 1-multi topic'),
        DeclareLaunchArgument('data_src', default_value=str(data_src),
                              description='Data source: 0-lidar'),
        DeclareLaunchArgument('output_data_type', default_value=str(output_type),
                              description='Output data type'),
        DeclareLaunchArgument('user_config_path', default_value=user_config_path,
                              description='Path to user config file'),
        DeclareLaunchArgument('cmdline_input_bd_code', default_value=cmdline_bd_code,
                              description='Command line input BD code'),
        DeclareLaunchArgument('lvx_file_path', default_value=lvx_file_path,
                              description='LVX file path'),
        
        Node(
            package='livox_ros_driver2',
            executable='livox_ros_driver2_node',
            name='livox_lidar_publisher',
            output='screen',
            parameters=[{
                "xfer_format": LaunchConfiguration('xfer_format'),
                "multi_topic": LaunchConfiguration('multi_topic'),
                "data_src": LaunchConfiguration('data_src'),
                "publish_freq": LaunchConfiguration('publish_freq'),
                "output_data_type": LaunchConfiguration('output_data_type'),
                "frame_id": LaunchConfiguration('frame_id'),
                "lidar_topic": LaunchConfiguration('lidar_topic'),
                "imu_topic": LaunchConfiguration('imu_topic'),
                "user_config_path": LaunchConfiguration('user_config_path'),
                "cmdline_input_bd_code": LaunchConfiguration('cmdline_input_bd_code'),
                "lvx_file_path": LaunchConfiguration('lvx_file_path'),
            }]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            arguments=['--display-config', rviz_config_path, '--fixed-frame', LaunchConfiguration('frame_id')]
        ),
        # launch.actions.RegisterEventHandler(
        #     event_handler=launch.event_handlers.OnProcessExit(
        #         target_action=livox_rviz,
        #         on_exit=[
        #             launch.actions.EmitEvent(event=launch.events.Shutdown()),
        #         ]
        #     )
        # )
    ])
