import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="AlienSpacing",
    options={"build.exe": {"packages:": ["pygame"],
                           "include_files": ["img/projectile1.png",
                                             "img/spritesheet/p1_spritesheet.png",
                                             "img/spritesheet/p1_spritesheet.txt",
                                             "img/spritesheet/spritesheet_jumper.png",
                                             "img/spritesheet/spritesheet_jumper.xml"]}},
    executables=executables
)
