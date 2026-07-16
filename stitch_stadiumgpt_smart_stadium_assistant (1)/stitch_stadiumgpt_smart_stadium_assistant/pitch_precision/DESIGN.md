---
name: Pitch Precision
colors:
  surface: '#101415'
  surface-dim: '#101415'
  surface-bright: '#363a3b'
  surface-container-lowest: '#0b0f10'
  surface-container-low: '#191c1e'
  surface-container: '#1d2022'
  surface-container-high: '#272a2c'
  surface-container-highest: '#323537'
  on-surface: '#e0e3e5'
  on-surface-variant: '#b9cbb9'
  inverse-surface: '#e0e3e5'
  inverse-on-surface: '#2d3133'
  outline: '#849584'
  outline-variant: '#3b4b3d'
  surface-tint: '#00e476'
  primary: '#f0ffee'
  on-primary: '#003919'
  primary-container: '#00ff85'
  on-primary-container: '#007137'
  inverse-primary: '#006d35'
  secondary: '#b5c8e3'
  on-secondary: '#203247'
  secondary-container: '#36485e'
  on-secondary-container: '#a4b7d1'
  tertiary: '#f3fcff'
  on-tertiary: '#00363f'
  tertiary-container: '#93ebff'
  on-tertiary-container: '#006c7b'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#61ff97'
  primary-fixed-dim: '#00e476'
  on-primary-fixed: '#00210c'
  on-primary-fixed-variant: '#005227'
  secondary-fixed: '#d2e4ff'
  secondary-fixed-dim: '#b5c8e3'
  on-secondary-fixed: '#091c31'
  on-secondary-fixed-variant: '#36485e'
  tertiary-fixed: '#a5eeff'
  tertiary-fixed-dim: '#00daf8'
  on-tertiary-fixed: '#001f25'
  on-tertiary-fixed-variant: '#004e5a'
  background: '#101415'
  on-background: '#e0e3e5'
  surface-variant: '#323537'
typography:
  display-lg:
    fontFamily: Montserrat
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-md:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-margin: 24px
  gutter: 16px
  section-gap: 48px
---

## Brand & Style

The design system is engineered to evoke the high-octane atmosphere of a FIFA World Cup final under the floodlights. It targets a global audience of fans, analysts, and organizers who require a premium, data-rich experience that feels both futuristic and authoritative.

The aesthetic leans heavily into **Glassmorphism** and **Corporate Modern** styles. It utilizes deep, immersive backgrounds to simulate the "stadium night" effect, allowing vibrant accent colors to pop with neon-like intensity. The interface relies on visual depth created through blurred transparencies, suggesting a sophisticated heads-up display (HUD) that is clean, energetic, and unapologetically professional.

## Colors

The palette is anchored by **Pitch Green**, a high-vibrancy accent used strictly for primary actions, success states, and key data highlights. The foundation is **Deep Stadium Blue**, providing a low-light environment that reduces eye strain and enhances the "premium" feel. 

- **Primary (Pitch Green):** Used for CTA buttons, active states, and winning streaks.
- **Secondary (Stadium Blue):** The primary background canvas and deep layering color.
- **Tertiary (Electric Cyan):** Used for secondary data visualizations, such as heatmaps or secondary buttons.
- **Neutral:** A range of crisp whites and cool grays (Slate 200-400) for legible typography and iconography.

All "Surface" elements utilize semi-transparent glass textures to maintain a sense of space and modern tech sophistication.

## Typography

This design system uses a dual-typeface strategy to balance impact with utility. 

**Montserrat** is used for headlines and display text. Its geometric construction and bold weights command attention, echoing the grandeur of stadium signage. **Inter** is the workhorse for all functional text, body copy, and data labels. Its high legibility at small sizes ensures that complex match statistics and player data remain clear.

For data-heavy dashboards, use the `label-md` style with uppercase transformations to create a professional, "spec-sheet" aesthetic.

## Layout & Spacing

The system follows a **Fluid Grid** model based on an 8px square rhythm. 

- **Desktop:** 12-column grid with 24px gutters and 64px side margins.
- **Tablet:** 8-column grid with 16px gutters and 32px side margins.
- **Mobile:** 4-column grid with 16px gutters and 16px side margins.

Content should be grouped into cards with significant internal padding (24px to 32px) to allow the "glass" background to breathe. Use "Section Gap" spacing to clearly separate distinct data modules like Live Scores vs. Tournament Brackets.

## Elevation & Depth

Depth is not communicated through traditional shadows, but through **Tonal Layering** and **Backdrop Blurs**.

1.  **Level 0 (Pitch):** Solid Deep Stadium Blue background.
2.  **Level 1 (Field):** 8% White glass overlay with a 12px backdrop blur. This is the standard card background.
3.  **Level 2 (Float):** 12% White glass overlay with a 20px backdrop blur and a soft, 20% opacity primary-tinted glow (0px 10px 30px rgba(0, 255, 133, 0.1)). Used for active cards or hovered elements.
4.  **Level 3 (Overlays):** 16% White glass overlay with a 40px backdrop blur for modals and floating action buttons.

All glass elements must feature a 1px inner border (stroke) using `glass_border` to define the edges against the dark background.

## Shapes

The shape language is sophisticated and modern, utilizing generous corner radii to offset the technical "dark mode" feel.

- **Standard Cards:** Use `rounded-2xl` (1rem / 16px).
- **Primary Buttons & Action Elements:** Use `rounded-xl` (0.75rem / 12px).
- **Status Tags & Chips:** Fully pill-shaped (rounded-full) to provide visual variety against the structured grid.
- **Data Visualization Bars:** Rounded caps on all bar charts and heatmaps to maintain the soft-tech aesthetic.

## Components

### Buttons
- **Primary:** Pitch Green background with Deep Blue text. No border. High-gloss shine effect on hover.
- **Secondary:** Glassy background with White text and a 1px White border at 20% opacity.
- **Floating Action Button (FAB):** Circular, Pitch Green, elevated with a soft Pitch Green glow.

### Cards
- Always semi-transparent with backdrop-blur. 
- Headers within cards should have a subtle bottom border (1px, 10% white) to separate title from data.

### Input Fields
- Dark, recessed backgrounds (rgba(0,0,0,0.2)) with subtle 1px borders.
- On focus, the border transitions to Pitch Green with a faint outer glow.

### Data Visualizations
- **Heatmaps:** Use a gradient scale from Deep Blue (cold) to Pitch Green (hot) to Electric Cyan (peak).
- **Progress Bars:** Pitch Green for the fill, with a subtle pulse animation for "Live" data points.

### Chips & Badges
- Small, uppercase text. 
- Use semi-transparent fills for "Live" match status with a small, pulsing green dot icon.