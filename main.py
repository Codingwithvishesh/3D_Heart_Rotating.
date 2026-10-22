import math
import random
import sys
import pygame

# Initialize Pygame
pygame.init()

# Setup Display
WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("3D Rotating Particle Heart")
clock = pygame.time.Clock()
FPS = 60

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2 - 20

# Color Palette (Vibrant Blood-Red & Neon Glow)
COLOR_CORE = (255, 20, 60)
COLOR_SHELL = (230, 0, 45)
COLOR_AURA = (255, 90, 140)


def heart_surface_point(u, v):
    """
    Parametric 3D Heart Surface Equation.
    Generates an accurate, anatomically recognizable 3D volumetric heart shape.
    u in [0, pi], v in [-pi, pi]
    """
    # Distinct cardiac shape profile
    x = 16 * (math.sin(u) ** 3) * math.sin(v)
    y = -(13 * math.cos(u) - 5 * math.cos(2 * u) - 2 * math.cos(3 * u) - math.cos(4 * u))
    z = 16 * (math.sin(u) ** 3) * math.cos(v) * 0.45  # Depth contour
    return x, y, z


def generate_stable_heart(total_points=3500):
    """
    Pre-computes fixed particle positions so that particles do NOT jitter or recreate.
    """
    particles = []

    # 1. Outer Well-Defined Surface (Sharp heart contour)
    for _ in range(int(total_points * 0.55)):
        u = random.uniform(0, math.pi)
        v = random.uniform(-math.pi, math.pi)
        x, y, z = heart_surface_point(u, v)
        # Subtle organic variance
        x += random.gauss(0, 0.15)
        y += random.gauss(0, 0.15)
        z += random.gauss(0, 0.15)
        particles.append((x, y, z, 'shell', random.uniform(0.8, 1.2)))

    # 2. Dense Solid Interior (Gives depth and volume)
    for _ in range(int(total_points * 0.35)):
        u = random.uniform(0, math.pi)
        v = random.uniform(-math.pi, math.pi)
        interior_ratio = (random.random()) ** 0.5  # Uniform interior density
        x, y, z = heart_surface_point(u, v)
        x *= interior_ratio
        y *= interior_ratio
        z *= interior_ratio
        particles.append((x, y, z, 'core', random.uniform(0.9, 1.1)))

    # 3. Soft Outer Halo Sparkles
    for _ in range(int(total_points * 0.10)):
        u = random.uniform(0, math.pi)
        v = random.uniform(-math.pi, math.pi)
        halo_scale = random.uniform(1.05, 1.25)
        x, y, z = heart_surface_point(u, v)
        x = x * halo_scale + random.gauss(0, 0.4)
        y = y * halo_scale + random.gauss(0, 0.4)
        z = z * halo_scale + random.gauss(0, 0.4)
        particles.append((x, y, z, 'aura', random.uniform(0.5, 0.9)))

    return particles


def rotate_y(x, y, z, angle):
    """Rotate around vertical Y-axis (fixed pivot)"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a


def rotate_x(x, y, z, angle):
    """Slight tilt towards camera for 3D depth perception"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return x, y * cos_a - z * sin_a, y * sin_a + z * cos_a


def main():
    particles = generate_stable_heart(3600)

    angle_y = 0.0
    tilt_x = 0.18  # Fixed aesthetic downward tilt
    scale_factor = 20.0
    camera_dist = 70.0
    rotation_speed = 0.9  # Smooth constant rotation

    running = True
    clock_time = 0.0

    while running:
        dt = clock.tick(FPS) / 1000.0
        clock_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Continuous smooth single-axis rotation in place
        angle_y += rotation_speed * dt

        # Smooth rhythmic contraction & expansion (stable origin)
        pulse = 1.0 + 0.06 * (math.sin(clock_time * 4.0) ** 4)

        # Clear background completely each frame to eliminate frame-lag
        screen.fill((5, 5, 8))

        # Project all 3D points
        render_queue = []
        for px, py, pz, ptype, psize in particles:
            # Scale around stationary center
            sx = px * pulse
            sy = py * pulse
            sz = pz * pulse

            # Apply rotations
            rx, ry, rz = rotate_y(sx, sy, sz, angle_y)
            rx, ry, rz = rotate_x(rx, ry, rz, tilt_x)

            # Perspective transformation
            depth = camera_dist + rz
            if depth <= 1:
                continue
            persp = camera_dist / depth

            screen_x = int(CENTER_X + rx * scale_factor * persp)
            screen_y = int(CENTER_Y + ry * scale_factor * persp)

            render_queue.append((rz, screen_x, screen_y, persp, ptype, psize))

        # Depth Sorting (Painter's Algorithm: render farthest first)
        render_queue.sort(key=lambda item: item[0])

        # Draw particles
        for rz, sx, sy, persp, ptype, psize in render_queue:
            if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                brightness = max(0.25, min(1.0, (persp - 0.5) * 1.6))

                if ptype == 'core':
                    col = (
                        int(COLOR_CORE[0] * brightness),
                        int(COLOR_CORE[1] * brightness),
                        int(COLOR_CORE[2] * brightness)
                    )
                    rad = max(1, int(2.2 * persp * psize))
                elif ptype == 'shell':
                    col = (
                        int(COLOR_SHELL[0] * brightness),
                        int(COLOR_SHELL[1] * brightness),
                        int(COLOR_SHELL[2] * brightness)
                    )
                    rad = max(1, int(1.8 * persp * psize))
                else:  # aura
                    col = (
                        int(COLOR_AURA[0] * brightness * 0.8),
                        int(COLOR_AURA[1] * brightness * 0.8),
                        int(COLOR_AURA[2] * brightness * 0.8)
                    )
                    rad = 1

                pygame.draw.circle(screen, col, (sx, sy), rad)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
