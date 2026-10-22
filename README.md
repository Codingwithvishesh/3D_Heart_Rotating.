# 🫀 Smooth 3D Rotating Heart Simulation

A stable, optimized, zero-lag 3D Particle Heart animation built with Python and Pygame.

---

## 🚀 Key Improvements

- **Accurate 3D Heart Shape**: Computed using 3D parametric heart surface geometry ($u, v$ mapping) for an authentic volumetric heart structure.
- **Stationary Pivot Rotation**: Rotates smoothly on a fixed central axis without drifting or shaking.
- **Zero Lag / 60 FPS Fixed**: Optimized rendering loop with pre-cached vertex coordinates and hardware double-buffering.
- **Clean Depth Shading**: Dynamic depth-lighting and perspective scaling without visual artifacts.

---

## 📦 Quick Setup

1. Extract the ZIP folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python main.py
   ```

---

## 🎮 Controls

- `Esc`: Close window
