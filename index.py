import pygame

pygame.init()

def main():
    joystick
    while joystick:
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                if not event.instance_id == 0:
                    continue
                joystick = pygame.joystick.Joystick(event.device_index)
            if event.type == pygame.JOYDEVICEREMOVED:
                if not event.instance_id == 0:
                    continue
                del joystick

        if joystick:
            print(f'{joystick.get_axis(0):>6.3f}, {joystick.get_axis(1):>6.3f}')

            hats = joystick.get_numhats()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)


if __name__ == "__main__":
    main()
    pygame.quit()