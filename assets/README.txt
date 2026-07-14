Drop your pet artwork into this folder using these exact filenames.
Any image size/resolution works - animations.py resizes every frame
to 220x220 automatically. PNG with transparency recommended (the
window uses #ff00ff as the transparent color key, so avoid that exact
magenta in your art or it will appear invisible).

Required files:
  idle.png        - static pose while waiting for a Yes/Snooze click
  happy.png        - static pose shown after clicking "Yes"
  angry.png        - static pose shown after clicking "Remind Me In 5 Min"

  walk_in1.png      - 4-frame walk cycle played while the pet enters
  walk_in2.png        from off-screen (right side) to its resting spot
  walk_in3.png
  walk_in4.png

  walk_out1.png     - 4-frame walk cycle played while the pet exits
  walk_out2.png       back off-screen after you respond
  walk_out3.png
  walk_out4.png

Once all 9 files are here, run: python main.py
