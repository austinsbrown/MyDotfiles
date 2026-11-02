# Everblush palette (extracted from Miserable_Xfce, branch origin/Everblush)

Sources: Dotfiles/.Xresources, kitty/color.ini, .themes/Everblush (GTK), .themes/Everblush-xfwm,
Kvantum/Everblush, eww/eww.scss.

## Surfaces
| role                         | hex       | source |
|------------------------------|-----------|--------|
| background (windows, views)  | #181f21   | Xresources background, GTK bg/base |
| titlebar / panel / popups    | #21282a   | xfwm titlebar pixels, eww $background |
| surface / color0             | #22292b   | Xresources color0, Kvantum light |
| button / hover surface       | #2c3335   | xfwm prelight bg, GTK wm_button_hover_bg, Kvantum button |
| pressed surface              | #363d3f   | xfwm pressed bg |
| darkest / shadow-ish         | #131a1c   | Kvantum dark/mid |
| bright black / color8        | #3b4244   | Xresources color8, kitty selection bg |
| border                       | rgba(255,255,255,0.07) | GTK borders |

## Text
| role            | hex      |
|-----------------|----------|
| foreground      | #dadada  |
| text (views)    | #b3b9b8 (color7) / #afb4ba (GTK text) |
| bright white    | #bdc3c2  |
| titlebar text   | #bbbbbb  (xfwm themerc) |
| inactive text   | #dadada at ~50% |

## Accent
| role                      | hex      |
|---------------------------|----------|
| selection / accent        | #6695a3  (GTK selected_bg, eww $accent) |
| alt deep accent           | #41707e  (Kvantum highlight) |

## ANSI colors (normal / bright)
| name    | normal  | bright  |
|---------|---------|---------|
| black   | #22292b | #3b4244 |
| red     | #e06e6e | #ef7d7d |
| green   | #8ccf7e | #9bdead |
| yellow  | #e5c76b | #f4d67a |
| blue    | #67b0e8 | #6cb5ed |
| magenta | #c47fd5 | #ce89df |
| cyan    | #6da4cd | #67cbe7 |
| white   | #b3b9b8 | #bdc3c2 |

## Window-button language (xfwm Everblush-xfwm, 30x36 buttons, titlebar 36px, color #21282a)
Glyphs are made of 3x3 px square "dots" on a 10x10 grid (rendered at ~x11..18, y14..21):
- close:     4 dots (2x2 grid)          red    #e06e6e
- maximize:  3 dots (top-left, top-right, bottom-right) green #8ccf7e
- restore:   3 dots (top-left, bottom-left, bottom-right) green #8ccf7e
- minimize:  1 dot  (bottom-left)       yellow #e5c76b
- inactive window: same glyphs in #dadada
- hover: rounded square bg #2c3335 (x3..26, y6..29 ≈ 24x24, small radius) behind glyph
- pressed: same square in #363d3f
Button layout: title left-aligned, buttons on the right in order minimize, maximize, close. No app icon.
No visible borders; shadow opacity 75%.

## Fonts
Roboto (UI), JetBrainsMono Nerd Font (monospace).
