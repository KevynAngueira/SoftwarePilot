''' 
Given a CSV file containing waypoint data,this Code implements a Wapoint mission on an anafi parrot sUAV. The code is adapted from a sample
program written by Kevyn Angueira.

John Chumley 28OCT2022

'''

from SoftwarePilot import SoftwarePilot
import sys
import csv


def getWaypointFiles():
    return sys.args[1:]


def traverseWaypointFile(filename, drone):
    with open(filename, 'r') as waypoint_file:
        # Creating a csv reader for the waypoint file
        waypoint_reader = csv.reader(waypoint_file)

        fields = next(waypoint_reader)

        for waypoint in waypoint_reader:
            latitude = waypoint[0]
            longitude = waypoint[1]
            '''
            Unsure if altitude is measured in meters or in feet
            Use top one if its in meters
            '''
            # altitude = waypoint[2]
            altitude = waypoint[2]/3.28084
            heading = waypoint[3]

            drone.piloting.move_to(latitude, longitude, altitude, heading=heading)
            drone.camera.media.take_photo()
            drone.camera.media.download_last_media()


if __name__ == "__main__":
    '''
    Unsure if altitude is measured in meters or in feet
    Use top one if its in meters
    '''
    # CLEARANCE_ALTITUDE = 3
    CLEARANCE_ALTITUDE = 10

    waypoint_files = getWaypointFiles()

    sp = SoftwarePilot()
    drone = sp.setup_drone("parrot_anafi", 1, "None")
    drone.connect()

    home = drone.get_drone_coordinates()

    drone.camera.media.setup_photo()
    # Yaw, Pitch, and Roll in degrees, change the numbers if the camera ain't looking down
    drone.camera.controls.set_alignment_offset(0, -90, 0)
    drone.piloting.takeoff()

    for file in waypoint_files:
        traverseWaypointFile(file, drone)

    drone.piloting.move_to(home[0], home[1], CLEARANCE_ALTITUDE)
    drone.piloting.land()
    drone.disconnect()
