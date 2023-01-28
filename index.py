import pygame
from communicate import sendMovement, sendSound

pygame.init()

DEADZONE = 0.05
def deadzone(val: float):
    if (abs(val) < DEADZONE):
        return 0
    return min(1, val)

def main():
    running = True
    joystick = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                if not joystick:
                    joystick = pygame.joystick.Joystick(event.device_index)
            if event.type == pygame.JOYBUTTONDOWN:
                sendSound(event.button)
            if event.type == pygame.JOYDEVICEREMOVED:
                running = False

        if joystick:
            sendMovement(deadzone(joystick.get_axis(0)), deadzone(joystick.get_axis(1)),  deadzone(joystick.get_axis(2)))



if __name__ == "__main__":
    main()
    pygame.quit()