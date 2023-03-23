*** Settings ***
Library    ats.robot.pyATSRobot
Library     unicon.robot.UniconRobot
Library    genie.libs.robot.GenieRobot


*** Test Cases ***

Connect to device
    use genie testbed "testbed.yaml"
    connect to all devices

Verify OSPF Neighbors
    verify count "3" "ospf neighbors" on device "R1"
    verify count "3" "ospf neighbors" on device "R2"
    verify count "2" "ospf neighbors" on device "R3"
    verify count "2" "ospf neighbors" on device "R4"
    verify count "2" "ospf neighbors" on device "R5"

Disconnect from device
    disconnect from all devices